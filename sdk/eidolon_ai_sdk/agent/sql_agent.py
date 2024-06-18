import os
from abc import abstractmethod
from functools import cached_property
from typing import AsyncIterable, Literal, Optional, Union, Type

import aiosqlite
import psycopg
from jinja2 import Environment, StrictUndefined, Template
from mysql.connector.aio import connect
from pydantic import BaseModel, ConfigDict, Field

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


class SqlLiteClient(SqlClient):
    protocol: Literal['sqlite3'] = 'sqlite3'
    model_config = ConfigDict(extra='allow')

    file: str

    async def execute(self, query: str):
        async with aiosqlite.connect(self.file, **self.model_extra) as db:
            async with db.execute(query) as cursor:
                async for row in cursor:
                    yield row


class MySqlClient(SqlClient):
    model_config = ConfigDict(extra='allow')
    protocol: Literal['mysql'] = 'mysql'

    host: Optional[str] = None
    user: Optional[str] = 'root'
    password: Optional[str] = Field(None,
                                    description='Password string or environment variable name. IE, MYSQL_PASSWORD or secret123')

    @cached_property
    def templated_password(self):
        if self.password:
            password = os.environ.get(self.password, None)
            if not password:
                logger.debug(f"Password environment variable not found, using password as is")
                return self.password
            else:
                return password
        else:
            return self.password

    async def execute(self, query: str):
        kwargs = {}
        if self.host is not None:
            kwargs['host'] = self.host
        if self.user is not None:
            kwargs['user'] = self.user
        if self.templated_password is not None:
            kwargs['password'] = self.templated_password
        async with await connect(**kwargs, **self.model_extra) as cnx:
            async with await cnx.cursor() as cur:
                await cur.execute(query)
                async for row in cur:
                    yield row


class PostgresClient(SqlClient):
    protocol: Literal['postgres'] = 'postgres'
    model_config = ConfigDict(extra='allow')

    conninfo: str = Field("",
                          description="psycopg.connect conninfo. Can be templated with envars using jinja templates. IE 'user=username password={{DB_PASSWORD}}'")

    @cached_property
    def templated_conninfo(self):
        return Environment(undefined=StrictUndefined).from_string(self.conninfo).render(**os.environ)

    async def execute(self, query: str):
        async with await psycopg.AsyncConnection.connect(self.conninfo, **self.model_extra) as aconn:
            async with aconn.cursor() as acur:
                async for record in acur:
                    yield record


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
