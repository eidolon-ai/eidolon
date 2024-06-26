from abc import abstractmethod
from functools import cached_property
from typing import AsyncIterable, Literal, Optional, cast

from fastapi import Body
from jinja2 import Environment, StrictUndefined, Template
from pydantic import BaseModel, model_validator
from sqlalchemy import text, make_url
from sqlalchemy.ext.asyncio import create_async_engine

from eidolon_ai_client.events import StartStreamContextEvent, ObjectOutputEvent, AgentStateEvent, EndStreamContextEvent
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


class SqlAlchemy(SqlClient):
    """
    A client for executing SQL queries using SQLAlchemy.
    See https://docs.sqlalchemy.org/ for connection configuration details.

    Performs cursory checks when `select_only` is set to True. Additionally ensure user is restricted to allowed permissions.
    """

    protocol: str = None
    connection_string: str = "sqlite+aiosqlite:///:memory:"
    engine_kwargs: dict = {}
    select_only: bool = False

    @model_validator(mode="after")
    def _set_protocol(self):
        if not self.protocol:
            self.protocol = make_url(self.connection_string).get_dialect().name
        return self

    @cached_property
    def _engine(self):
        return create_async_engine(self.connection_string, **self.engine_kwargs)

    async def execute(self, query: str) -> AsyncIterable[tuple]:
        async with self._engine.connect() as conn:
            text_query = text(query)
            if self.select_only and not text_query.is_select:
                raise ValueError("Only SELECT queries are allowed")
            resp = await conn.stream(text_query)
            async for row in resp:
                yield row


class SqlLogicUnit(LogicUnit):
    def __init__(self, client: SqlClient, apu: ProcessingUnitLocator, limit: int = 10):
        super().__init__(apu)
        self.client = client
        self.limit = limit

    @llm_function()
    async def peek(self, query: str) -> dict:
        """
        Execute a query and see return the first few rows of a query.
        """
        to_yield = self.limit
        rows = []
        async for row in self.client.execute(query):
            rows.append(row)
            if len(rows) >= to_yield:
                break

        return dict(rows=rows)


class SqlAgentSpec(BaseModel):
    client: AnnotatedReference[SqlClient]
    apu: AnnotatedReference[APU]
    description: str = "An agent for interacting with data. Can respond to queries provided in natural language."
    system_prompt: str = """
    You are a helpful assistant that is a sql expert and helps a user query a {{ protocol }} database and analyse the response.
    
    Use your tools to investigate the database with the goal of providing the user with the query that they need.
    
    Think carefully.
    """
    system_prompt_suffix: str = ""
    query_prompt: str = "{{ body }}"
    clarification_prompt: Optional[str] = "What clarifying information do you need? Phrase your response as an explicit question or several questions."
    error_prompt: str = "An error occurred executing the query \"{{ query }}\": {{ error }}"
    num_retries: int = 3


class AgentResponse(BaseModel):
    response_type: Literal['execute', 'clarify']
    query: Optional[str] = None


class SqlAgent(Specable[SqlAgentSpec]):
    _client: SqlClient
    _apu: APU
    _system_prompt: Template
    _query_prompt: Template
    _clarification_prompt: Optional[Template]
    _type: dict
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
        self._query_prompt = environment.from_string(self.spec.query_prompt)
        self._clarification_prompt = environment.from_string(
            self.spec.clarification_prompt) if self.spec.clarification_prompt else None
        query_response_type = dict(
            type="object",
            properties=dict(
                response_type=dict(const="execute"),
                query=dict(type="string")),
            required=["response_type", "query"]
        )
        if self._clarification_prompt:
            clarification_response_type = dict(
                type="object",
                properties=dict(response_type=dict(const="clarify")),
                required=["response_type"]
            )
            self._type = dict(anyOf=[query_response_type, clarification_response_type])
        else:
            self._type = query_response_type

    @register_program()
    async def query(self, process_id, body: str = Body("", media_type="text/plain")):
        kwargs = dict(body=body)

        t = await self._apu.main_thread(process_id)
        await t.set_boot_messages(
            prompts=[SystemAPUMessage(prompt=self._system_prompt.render(protocol=self._client.protocol, **kwargs))])
        message = UserTextAPUMessage(prompt=self._query_prompt.render(protocol=self._client.protocol, **kwargs))
        async for e in self.cycle(t, message, self.spec.num_retries):
            yield e

    @register_action("clarify")
    async def clarify(self, process_id, body: str = Body("", media_type="text/plain")):
        message = UserTextAPUMessage(prompt=body)
        t = await self._apu.main_thread(process_id)
        async for e in self.cycle(t, message, self.spec.num_retries):
            yield e

    async def cycle(self, thread, message, num_reties):
        last_event = None
        async for e in self.thinking(message, thread):
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
                async for row in self._client.execute(response.query):
                    yield ObjectOutputEvent(content=row)
                yield AgentStateEvent(state="terminated")
            except Exception as e:
                if num_reties > 0:
                    yield StartStreamContextEvent(context_id='error', title='Error')
                    yield ObjectOutputEvent(content=dict(query=response.query, error=str(e)), stream_context='error')
                    yield EndStreamContextEvent(context_id='error')
                    message = UserTextAPUMessage(prompt=self._error_prompt.render(error=str(e), query=response.query))
                    async for e in self.cycle(thread, message, num_reties - 1):
                        yield e
                else:
                    raise
        elif response.response_type == "clarify":
            prompt = UserTextAPUMessage(prompt=self._clarification_prompt.render(protocol=self._client.protocol))
            async for e in thread.stream_request(prompts=[prompt]):
                yield e
            yield AgentStateEvent(state="clarify")
        else:
            raise ValueError(f"Unexpected response type from llm: {response.type}")

    async def thinking(self, message, thread):
        thinking_stream = thread.stream_request(
            prompts=[message],
            output_format=self._type
        )
        async for e in stream_manager(thinking_stream,
                                      StartStreamContextEvent(context_id='thinking', title='Thinking')):
            yield e


class QueryError(Exception):
    def __init__(self, query, error):
        self.query = query
        self.error = error
        super().__init__(f"Error executing query {query}: {error}")
