from __future__ import annotations

from abc import abstractmethod
from functools import cached_property
from typing import AsyncIterable, List, cast, Any

from pydantic import BaseModel, Field, model_validator
from sqlalchemy import make_url, MetaData, text, Row
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


class SqlClient(BaseModel):
    protocol: str

    @abstractmethod
    def execute(self, query: str) -> AsyncIterable[tuple]:
        pass

    async def get_schema(self) -> dict:
        pass


class MetadataAttribute(BaseModel):
    name: str
    metadata: List["MetadataAttribute"] | List[str] = []
    remove_falsy_metadata: bool = True


class SqlAlchemy(SqlClient):
    """
    A client for executing SQL queries using SQLAlchemy.
    See https://docs.sqlalchemy.org/ for connection configuration details.

    Performs cursory checks when `select_only` is set to True. Additionally ensure user is restricted to allowed permissions.
    """

    connection_string: str = Field(
        "sqlite+aiosqlite:///:memory:",
        description="SQLAlchemy connection string. See https://docs.sqlalchemy.org/en/20/core/engines.html for more information.",
    )
    engine_kwargs: dict = {}
    select_only: bool = False
    metadata: List[MetadataAttribute] = [
        MetadataAttribute(
            name="tables",
            atributes=[
                MetadataAttribute(
                    name="columns",
                    attributes=[
                        "name",
                        "type",
                        "nullable",
                        "default",
                        "autoincrement",
                        "primary_key",
                        "foreign_keys",
                        "constraints",
                    ],
                )
            ],
        )
    ]
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
