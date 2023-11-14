import asyncio

import pytest
from bson import ObjectId

from eidolon_sdk.impl.mongo_symbolic_memory import MongoSymbolicMemory


@pytest.fixture(scope='class')
def event_loop(request):
    """
    Create an instance of the default event loop for each test class.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Test class for grouping the tests
@pytest.mark.usefixtures("event_loop")
class TestMongoSymbolicMemory:
    @pytest.fixture(scope='function')
    async def collection_name(self):
        # Setup for each test method: create a new collection
        collection_name = f"test_collection_{ObjectId()}"  # Unique name for test collection
        yield collection_name

    @pytest.mark.asyncio
    async def test_connection(self, symbolic_memory: MongoSymbolicMemory):
        memory = symbolic_memory
        memory.start()
        assert memory.database is not None
        memory.stop()
        assert memory.database is None

    @pytest.mark.asyncio
    async def test_insert_one(self, symbolic_memory: MongoSymbolicMemory, collection_name: str):
        memory = symbolic_memory
        document = {"test": "data"}
        await memory.insert_one(collection_name, document)
        result = await memory.find_one(collection_name, document)
        assert result["test"] == "data"

    @pytest.mark.asyncio
    async def test_insert_one(self, symbolic_memory: MongoSymbolicMemory, collection_name: str):
        memory = symbolic_memory
        document = {"test": "data"}
        await memory.insert_one(collection_name, document)
        result = await memory.find_one(collection_name, document)
        assert result["test"] == "data"

    @pytest.mark.asyncio
    async def test_insert_and_find(self, symbolic_memory: MongoSymbolicMemory, collection_name: str):
        memory = symbolic_memory
        documents = [{"test": "data1"}, {"test": "data2"}]
        await memory.insert(collection_name, documents)
        cursor = memory.find(collection_name, {})
        results = [record async for record in cursor]
        assert len(results) == 2

    @pytest.mark.asyncio
    async def test_find_one_non_existent(self, symbolic_memory: MongoSymbolicMemory, collection_name: str):
        memory = symbolic_memory
        result = await memory.find_one(collection_name, {"test": "nonexistent"})
        assert result is None

    @pytest.mark.asyncio
    async def test_upsert_one_new_document(self, symbolic_memory: MongoSymbolicMemory, collection_name: str):
        memory = symbolic_memory
        document = {"test": "upsert"}
        await memory.upsert_one(collection_name, {"$set": document}, {"test": "upsert"})
        result = await memory.find_one(collection_name, {"test": "upsert"})
        assert result["test"] == "upsert"

    @pytest.mark.asyncio
    async def test_upsert_one_existing_document(self, symbolic_memory: MongoSymbolicMemory, collection_name: str):
        memory = symbolic_memory
        document = {"test": "existing"}
        await memory.insert_one(collection_name, document)
        await memory.upsert_one(collection_name, {"$set": {"test": "updated"}}, {"test": "existing"})
        result = await memory.find_one(collection_name, {"test": "updated"})
        assert result["test"] == "updated"

    @pytest.mark.asyncio
    async def test_invalid_query(self, symbolic_memory: MongoSymbolicMemory, collection_name: str):
        memory = symbolic_memory
        with pytest.raises(Exception):  # Replace with specific exception if necessary
            await memory.find_one(collection_name, {"$invalidOperator": "value"})
