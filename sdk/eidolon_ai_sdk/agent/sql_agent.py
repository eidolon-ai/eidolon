import os
from abc import abstractmethod
from functools import cached_property
from typing import AsyncIterable, Literal, Optional, Union, Type

from jinja2 import Environment, StrictUndefined, Template
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine

from eidolon_ai_client.events import StartStreamContextEvent, ObjectOutputEvent, AgentStateEvent, EndStreamContextEvent
from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.apu.agent_io import SystemAPUMessage, UserTextAPUMessage
from eidolon_ai_sdk.apu.apu import APU
from eidolon_ai_sdk.system.reference_model import AnnotatedReference
from eidolon_ai_sdk.util.stream_collector import stream_manager, StreamCollector


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

    connection_string: str = "sqlite+pysqlite:///:memory:"
    engine_kwargs: dict = {}
    select_only: bool = False

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


class SqlAgentSpec(BaseModel):
    client: AnnotatedReference[SqlClient]
    apu: AnnotatedReference[APU]
    description: str
    system_prompt: str = "Please provide the SQL query you would like to execute"
    system_prompt_suffix: str = ""
    query_prompt: str = "{{ body }}"
    clarification_prompt: Optional[str] = "{{ body }}"
    summarization_prompt: Optional[str] = "Provide a summary of the results"
    execution_prompt: Optional[str] = "What query should be run?"
    error_prompt: str = "An error occurred executing the query \"{{ query }}\": {{ error }}"
    num_retries: int = 3

    _client: SqlClient
    _apu: APU
    _system_prompt: Template
    _query_prompt: Template
    _clarification_prompt: Optional[Template]
    _summarization_prompt: Optional[Template]
    _type: Type[Literal['execute', 'clarify', 'summary']]
    _error_prompt: Template

    def __init__(self):
        super().__init__()
        self._client = self.client.instantiate()
        self._apu = self.apu.instantiate()
        environment = Environment(undefined=StrictUndefined)
        self._error_prompt = environment.from_string(self.error_prompt)
        self._system_prompt = environment.from_string(self.system_prompt)
        self._query_prompt = environment.from_string(self.query_prompt)
        self._clarification_prompt = environment.from_string(
            self.clarification_prompt) if self.clarification_prompt else None
        self._summarization_prompt = environment.from_string(
            self.summarization_prompt) if self.summarization_prompt else None
        type_args = []
        if self._clarification_prompt:
            type_args.append(Literal["clarify"])
        if self.execution_prompt:
            type_args.append(Literal["execute"])
        if self.summarization_prompt:
            type_args.append(Literal["summary"])
        self._type = Union[tuple(type_args)]

    async def query(self, process_id, **kwargs):
        t = await self._apu.main_thread(process_id)
        await t.set_boot_messages(prompts=[SystemAPUMessage(prompt=self._system_prompt.render(protocol=self._client.protocol, **kwargs))])
        message = UserTextAPUMessage(prompt=self._query_prompt.render(protocol=self._client.protocol, **kwargs))
        async for e in self.cycle(t, message, self.num_retries, kwargs):
            yield e

    async def clarify(self, process_id, **kwargs):
        message = UserTextAPUMessage(prompt=self._clarification_prompt.render(protocol=self._client.protocol, **kwargs))
        t = await self._apu.main_thread(process_id)
        async for e in self.cycle(t, message, self.num_retries, kwargs):
            yield e

    async def cycle(self, thread, message, num_reties, kwargs):
        kwargs = dict(protocol=self._client.protocol, **kwargs)
        thinking_stream = thread.stream_request(
            prompts=[message],
            output_format=self._type
        )
        thinking_stream = StreamCollector(stream=thinking_stream)
        async for e in stream_manager(thinking_stream,
                                      StartStreamContextEvent(context_id='thinking', title='Thinking')):
            yield e
        resp = thinking_stream.get_content()[-1]
        if resp == "summary":
            async for event in thread.stream_request(
                    prompts=[UserTextAPUMessage(prompt=self._summarization_prompt.render(**kwargs))]):
                yield event
        elif resp == "clarify":
            async for event in thread.stream_request(
                    prompts=[UserTextAPUMessage(prompt=self._clarification_prompt.render(**kwargs))]):
                yield event
            yield AgentStateEvent(state='clarify')
        elif resp == "execute":
            gen_req = thread.stream_request(prompts=[UserTextAPUMessage(prompt=self._clarification_prompt.render(**kwargs))])
            gen_req = StreamCollector(stream=gen_req)
            async for e in stream_manager(gen_req, StartStreamContextEvent(context_id='generating_sql', title='Generating SQL')):
                yield e
            query = gen_req.get_content()[-1]
            try:
                async for row in self._client.execute(query):
                    yield ObjectOutputEvent(content=row)
            except Exception as e:
                if num_reties > 0:
                    yield StartStreamContextEvent(context_id='error', title='Error')
                    yield ObjectOutputEvent(content=dict(query=query, error=str(e)), context_id='error')
                    yield EndStreamContextEvent(context_id='error')
                    message = UserTextAPUMessage(prompt=self._error_prompt.render(error=str(e), query=query, **kwargs))
                    async for e in self.cycle(thread, message, num_reties - 1, kwargs):
                        yield e
                else:
                    raise e
        else:
            raise ValueError(f"Unexpected response from llm: {resp}")
