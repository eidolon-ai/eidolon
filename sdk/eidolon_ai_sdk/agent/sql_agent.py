import sqlite3
from os import environ
from sqlite3 import Connection, Cursor
from typing import AsyncIterable, Iterable, Any, Literal, Optional
from abc import ABC, abstractmethod

import aiosqlite
from pydantic import BaseModel, ConfigDict
from mysql.connector.aio import connect

from eidolon_ai_sdk.system.reference_model import AnnotatedReference


class SqlClient(BaseModel):
    protocol: str

    @abstractmethod
    def execute(self, query: str) -> AsyncIterable[tuple]:
        pass


class SqlLiteClient(SqlClient):
    protocol: Literal['sqlite3'] = 'sqlite3'
    file: str

    async def execute(self, query: str):
        async with aiosqlite.connect('example.db') as db:
            async with db.execute(query) as cursor:
                async for row in cursor:
                    yield row


class MySqlClient(SqlClient):
    model_config = ConfigDict(extra='allow')
    protocol: Literal['mysql'] = 'mysql'

    host: Optional[str] = None
    user: Optional[str] = 'root'
    password: Optional[str] = environ.get('MYSQL_PASSWORD', None)

    async def execute(self, query: str):
        kwargs = {}
        if self.host is not None:
            kwargs['host'] = self.host
        if self.user is not None:
            kwargs['user'] = self.user
        if self.password is not None:
            kwargs['password'] = self.password
        async with await connect(**kwargs, **self.model_extra) as cnx:
            async with await cnx.cursor() as cur:
                r = await cur.execute(query)
                r2 = await r.fetchall()
                yield row



class SqlAgentSpec(BaseModel):
    client: AnnotatedReference[SqlClient]
