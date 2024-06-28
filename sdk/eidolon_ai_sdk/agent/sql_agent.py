from abc import abstractmethod
from functools import cached_property
from typing import AsyncIterable, Literal, Optional, cast, Any, List, Self

from jinja2 import Environment, StrictUndefined, Template
from pydantic import BaseModel, model_validator, validator, Field
from sqlalchemy import text, make_url, Row, MetaData
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from eidolon_ai_client.events import StartStreamContextEvent, ObjectOutputEvent, AgentStateEvent, EndStreamContextEvent, \
    UserInputEvent, StringOutputEvent
from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.agent.agent import register_program, register_action
from eidolon_ai_sdk.apu.agent_io import SystemAPUMessage, UserTextAPUMessage
from eidolon_ai_sdk.apu.apu import APU
from eidolon_ai_sdk.apu.logic_unit import LogicUnit, llm_function
from eidolon_ai_sdk.apu.processing_unit import ProcessingUnitLocator
from eidolon_ai_sdk.system.reference_model import AnnotatedReference, Specable
from eidolon_ai_sdk.util.stream_collector import stream_manager


class SqlClient(BaseModel):
    protocol: str

    @abstractmethod
    def execute(self, query: str) -> AsyncIterable[tuple]:
        pass

    async def get_schema(self) -> dict:
        pass


class MetadataAttribute(BaseModel):
    name: str
    metadata: List[Self | str] = []
    remove_falsy_metadata: bool = True


class SqlAlchemy(SqlClient):
    """
    A client for executing SQL queries using SQLAlchemy.
    See https://docs.sqlalchemy.org/ for connection configuration details.

    Performs cursory checks when `select_only` is set to True. Additionally ensure user is restricted to allowed permissions.
    """

    protocol: str = None
    connection_string: str = Field("sqlite+aiosqlite:///:memory:", description="SQLAlchemy connection string. See https://docs.sqlalchemy.org/en/20/core/engines.html for more information.")
    engine_kwargs: dict = {}
    select_only: bool = False
    metadata: List[MetadataAttribute] = [MetadataAttribute(
        name="tables",
        atributes=[MetadataAttribute(
            name="columns",
            attributes=["name", "type", "nullable", "default", "autoincrement", "primary_key", "foreign_keys", "constraints"]
    )])]
    protocol: str = None

    @model_validator(mode="after")
    def _set_protocol(self):
        if not self.protocol:
            self.protocol = make_url(self.connection_string).get_dialect().name
        return self

    @cached_property
    def _engine(self) -> AsyncEngine:
        try:
            return create_async_engine(self.connection_string, **self.engine_kwargs)
        except InvalidRequestError as e:
            raise ValueError(f"Error creating engine due to invalid connection_string or engine_kwargs: {e}")

    def _md(self, obj, md_attrs: List[MetadataAttribute | str]):
        rtn = {}
        for md_attr in (MetadataAttribute(name=md) if isinstance(md, str) else md for md in md_attrs):
            key, value = md_attr.name, getattr(obj, md_attr.name, None)
            if value and md_attr.metadata:
                value = self._md(value, md_attr.metadata)
            if md_attr.remove_falsy_metadata and not value:
                continue
            else:
                rtn[key] = value
        return rtn

    def _md_wrapper(self, conn):
        metadata = MetaData()
        metadata.reflect(bind=conn)
        return self._md(metadata, self.metadata)

    async def get_schema(self) -> dict:
        async with self._engine.connect() as conn:
            return await conn.run_sync(self._md_wrapper)

    async def execute(self, query: str) -> AsyncIterable[tuple]:
        async with self._engine.connect() as conn:
            text_query = text(query)
            if self.select_only and not text_query.is_select:
                raise ValueError("Only SELECT queries are allowed")
            resp = await conn.stream(text_query)
            async for row in resp:
                yield [c for c in cast(Row[tuple[Any, ...]], row)]


class SqlAlchemyEngineError(Exception):
    pass


class SqlLogicUnit(LogicUnit):
    def __init__(self, client: SqlClient, apu: ProcessingUnitLocator):
        super().__init__(apu)
        self.client = client

    @llm_function()
    async def peek(self, query: str, row_limit: int = 10) -> dict:
        """
        Execute a query and see return the first few rows of a query.
        """
        rows = []
        async for row in self.client.execute(query):
            rows.append(row)
            if len(rows) >= row_limit:
                break

        return dict(rows=rows)


class SqlAgentSpec(BaseModel):
    client: AnnotatedReference[SqlClient]
    apu: AnnotatedReference[APU]
    description: str = "An agent for interacting with data. Can respond to queries provided in natural language."
    system_prompt: str = """
    You are a helpful assistant that is a sql expert and helps a user query a {{ protocol }} database and analyse the response.
    
    Here is the database schema:
    {{ metadata }}
    
    Use your as needed tools to investigate the database with the goal of providing the user with the query that they need.
    
    Think carefully.
    """
    user_prompt: str = "{{ message }}"
    clarification_prompt: str = "What clarifying information do you need? Phrase your response as an explicit question or several questions."
    response_prompt: str = "What is your response? Be explicit and concise."
    error_prompt: str = "An error occurred executing the query \"{{ query }}\": {{ error }}"
    num_retries: int = 3


class AgentResponse(BaseModel):
    response_type: Literal['execute', 'clarify', 'respond']
    query: Optional[str] = None


class SqlRequestBody(BaseModel):
    message: str
    allow_conversation: bool = True

class SqlAgent(Specable[SqlAgentSpec]):
    _client: SqlClient
    _apu: APU
    _system_prompt: Template
    _user_prompt: Template
    _clarification_prompt: Template
    _error_prompt: Template

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client = self.spec.client.instantiate()
        self._apu = self.spec.apu.instantiate()

        if hasattr(self._apu, "logic_units"):
            self._apu.logic_units.append(SqlLogicUnit(client=self._client, apu=cast(self._apu, ProcessingUnitLocator)))
        else:
            raise ValueError("APU does not have logic units")

        environment = Environment(undefined=StrictUndefined)
        self._error_prompt = environment.from_string(self.spec.error_prompt)
        self._system_prompt = environment.from_string(self.spec.system_prompt)
        self._user_prompt = environment.from_string(self.spec.user_prompt)
        self._clarification_prompt = environment.from_string(self.spec.clarification_prompt)
        self._response_prompt = environment.from_string(self.spec.response_prompt)

    @register_program()
    @register_action("idle")
    async def query(self, process_id, agent_state, body: SqlRequestBody):
        schema = await self._client.get_schema()
        kwargs = dict(**body.model_dump(), metadata=schema, protocol=self._client.protocol)
        t = await self._apu.main_thread(process_id)
        if agent_state == "initialized":
            await t.set_boot_messages(
                prompts=[SystemAPUMessage(prompt=self._system_prompt.render(**kwargs))])
        message = UserTextAPUMessage(prompt=self._user_prompt.render(**kwargs))
        yield UserInputEvent(input=body.message)
        async for e in self.cycle(t, message, self.spec.num_retries, body=body):
            yield e

    async def cycle(self, thread, message, num_reties, body: SqlRequestBody):
        last_event = None
        thinking_stream = thread.stream_request(
            prompts=[message],
            output_format=self.get_response_object(body)
        )
        async for e in stream_manager(thinking_stream, StartStreamContextEvent(context_id='thinking', title='Thinking')):
            if isinstance(e, ObjectOutputEvent):
                last_event = e
            yield e

        if not last_event:
            raise ValueError("No response from llm")
        try:
            response = AgentResponse(**last_event.content)
        except Exception:
            raise ValueError(f"Unexpected response from llm: {last_event}")
        if response.response_type == "execute":
            try:
                logger.info(f"Executing query: {response.query}")
                num_rows = 0
                async for row in self._client.execute(response.query):
                    yield ObjectOutputEvent(content=row)
                    num_rows += 1
                if num_rows == 0:
                    raise ValueError("No data returned from query")
                yield AgentStateEvent(state="idle") if body.allow_conversation else AgentStateEvent(state="terminated")
            except Exception as e:
                if num_reties > 0:
                    yield StartStreamContextEvent(context_id='error', title='Error')
                    yield ObjectOutputEvent(content=dict(query=response.query, error=str(e)), stream_context='error')
                    yield EndStreamContextEvent(context_id='error')
                    message = UserTextAPUMessage(prompt=self._error_prompt.render(error=str(e), query=response.query))
                    yield UserInputEvent(input=message.prompt)
                    async for e in self.cycle(thread, message, num_reties - 1, body=body):
                        yield e
                else:
                    if body.allow_clarification:
                        yield StringOutputEvent(content="I'm sorry, I'm having trouble executing a query. Can you provide more information?")
                        yield AgentStateEvent(state="idle")
                    else:
                        raise
        elif response.response_type == "clarify":
            prompt = UserTextAPUMessage(prompt=self._clarification_prompt.render(protocol=self._client.protocol))
            async for e in thread.stream_request(prompts=[prompt]):
                yield e
            yield AgentStateEvent(state="idle")
        elif response.response_type == "respond":
            prompt = UserTextAPUMessage(prompt=self._response_prompt.render(protocol=self._client.protocol))
            async for e in thread.stream_request(prompts=[prompt]):
                yield e
            yield AgentStateEvent(state="idle") if body.allow_conversation else AgentStateEvent(state="terminated")
        else:
            raise ValueError(f"Unexpected response type from llm: {response.response_type}")

    def get_response_object(self, body: SqlRequestBody):
        responses = [dict(
            type="object",
            description="Respond to the user with the data returned after executing the provided query",
            properties=dict(
                response_type=dict(const="execute"),
                query=dict(type="string")),
            required=["response_type", "query"],
        )]
        if body.allow_conversation:
            responses.append(dict(
                type="object",
                description="A response that directly answers the provided question.",
                properties=dict(
                    response_type=dict(const="respond"),
                ),
                required=["response_type"],
            ))
            responses.append(dict(
                type="object",
                description="More information is required from the user to answer the provided question.",
                properties=dict(response_type=dict(const="clarify")),
                required=["response_type"],
            ))

        if len(responses) > 1:
            return dict(anyOf=responses)
        elif len(responses) == 1:
            return responses[0]
        else:
            raise ValueError("No valid response types")  # this should not be possible due to validation in SqlRequestBody


class QueryError(Exception):
    def __init__(self, query, error):
        self.query = query
        self.error = error
        super().__init__(f"Error executing query {query}: {error}")
