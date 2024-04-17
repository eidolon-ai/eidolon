import os

# noinspection PyPackageRequirements
from contextvars import ContextVar
from typing import Any, Optional, AsyncIterable, Union, Dict, List

from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
from pydantic import Field, BaseModel

from eidolon_ai_sdk.memory.semantic_memory import SymbolicMemoryBase
from eidolon_ai_sdk.system.reference_model import Specable


class MongoSymbolicMemoryConfig(BaseModel):
    mongo_connection_string: str = Field(
        default=os.environ.get("MONGO_CONNECTION_STR", "mongodb://localhost:27017/?directConnection=true"),
        description="The connection string to the MongoDB instance.",
    )
    mongo_database_name: str = Field(
        default=os.environ.get("MONGO_DATABASE_NAME", "eidolon"), description="The name of the MongoDB database to use."
    )


class MongoSymbolicMemory(SymbolicMemoryBase, Specable[MongoSymbolicMemoryConfig]):
    mongo_connection_string: Optional[str]
    mongo_database_name: str
    _database: Optional[ContextVar]

    def __init__(self, spec: MongoSymbolicMemoryConfig):
        super().__init__(spec)
        self.mongo_connection_string = spec.mongo_connection_string
        self.mongo_database_name = spec.mongo_database_name
        self._database = None

    @property
    def database(self) -> AsyncIOMotorDatabase:
        if not self._database:
            self._database = ContextVar("database")
        try:
            return self._database.get()
        except LookupError:
            client = AsyncIOMotorClient(self.mongo_connection_string)
            database = client.get_database(self.mongo_database_name)
            self._database.set(database)
            return database

    async def count(self, symbol_collection: str, query: dict[str, Any]) -> int:
        return await self.database[symbol_collection].count_documents(query)

    async def find(
        self,
        symbol_collection: str,
        query: dict[str, Any],
        projection: Union[List[str], Dict[str, int]] = None,
        sort: dict = None,
        skip: int = None,
    ) -> AsyncIterable[dict[str, Any]]:
        cursor = self.database[symbol_collection].find(query, projection=projection)
        if sort:
            cursor = cursor.sort(sort)
        if skip:
            cursor = cursor.skip(skip)
        async for document in cursor:
            yield document

    async def find_one(
        self, symbol_collection: str, query: dict[str, Any], sort: dict = None
    ) -> Optional[dict[str, Any]]:
        kwargs = dict(filter=query)
        if sort:
            kwargs["sort"] = sort
        return await self.database[symbol_collection].find_one(**kwargs)

    async def insert(self, symbol_collection: str, documents: list[dict[str, Any]]) -> None:
        return await self.database[symbol_collection].insert_many(documents)

    async def insert_one(self, symbol_collection: str, document: dict[str, Any]) -> None:
        return await self.database[symbol_collection].insert_one(document)

    async def update_many(self, symbol_collection: str, query: dict[str, Any], document: dict[str, Any]) -> None:
        return await self.database[symbol_collection].update_many(query, document)

    async def upsert_one(self, symbol_collection: str, document: dict[str, Any], query: dict[str, Any]) -> None:
        return await self.database[symbol_collection].update_one(query, {"$set": document}, upsert=True)

    async def delete(self, symbol_collection, query):
        return await self.database[symbol_collection].delete_many(query)

    async def stop(self):
        """
        Stops the memory implementation. Noop for this implementation.
        """
        if self.database is not None:
            self.database.client.close()
            self._database = None
