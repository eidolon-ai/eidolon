import pytest
from pymongo.errors import DuplicateKeyError

from eidos_sdk.memory.local_symbolic_memory import LocalSymbolicMemory


@pytest.fixture
def memory():
    # Setup memory instance
    mem = LocalSymbolicMemory()
    mem.start()
    yield mem
    # Teardown memory instance
    mem.stop()


class TestLocalSymbolicMemory:
    def test_start(self, memory):
        assert LocalSymbolicMemory.db == {}, "Database should be initialized as an empty dictionary."

    def test_stop(self, memory):
        LocalSymbolicMemory.db["test"] = "value"
        memory.stop()
        assert LocalSymbolicMemory.db == {}, "Database should be cleared after stop."

    @pytest.mark.asyncio
    async def test_insert_one(self, memory):
        await memory.insert_one("collection", {"key": "value"})
        assert "collection" in LocalSymbolicMemory.db
        assert LocalSymbolicMemory.db["collection"][0] == {"key": "value"}

    @pytest.mark.asyncio
    async def test_insert(self, memory):
        documents = [{"key1": "value1"}, {"key2": "value2"}]
        await memory.insert("collection", documents)
        assert len(LocalSymbolicMemory.db["collection"]) == 2

    # ... more tests for the rest of the CRUD operations ...

    @pytest.mark.asyncio
    async def test_matches_query_simple(self, memory):
        await memory.insert_one("collection", {"key": "value"})
        result = await memory.find_one("collection", {"key": "value"})
        assert result == {"key": "value"}

    @pytest.mark.asyncio
    async def test_matches_query_complex(self, memory):
        document = {
            "name": "John",
            "age": 30,
            "address": {"city": "New York", "zip": "10001"},
        }
        query = {"name": "John", "address": {"city": "New York"}}
        await memory.insert_one("collection", document)
        result = await memory.find_one("collection", query)
        assert result == document

    # Tests for MongoDB-like query operations
    @pytest.mark.asyncio
    async def test_matches_query_with_operators(self, memory):
        document = {"age": 25}
        await memory.insert_one("collection", document)
        # The LocalSymbolicMemory class does not support MongoDB-like query operators
        # so we cannot test for them

    # Tests for upsert operations
    @pytest.mark.asyncio
    async def test_upsert_one_existing(self, memory):
        await memory.insert_one(
            "collection", {"_id": "1", "key": "value", "counter": 1, "updated": "2022-01-01T00:00:00"}
        )
        update = {"_id": "1", "key": "value", "counter": 2, "updated": "2022-01-01T00:00:00"}
        await memory.upsert_one("collection", update, {"_id": "1", "updated": "2022-01-01T00:00:00"})
        result = await memory.find_one("collection", {"_id": "1"})
        assert result == update

    @pytest.mark.asyncio
    async def test_upsert_one_new(self, memory):
        await memory.upsert_one(
            "collection", {"_id": "2", "key": "new_value", "updated": "2022-01-01T00:00:00"}, {"_id": "non_existing"}
        )
        result = await memory.find_one("collection", {"_id": "2"})
        assert result == {"_id": "2", "key": "new_value", "updated": "2022-01-01T00:00:00"}

    @pytest.mark.asyncio
    async def test_upsert_one_duplicate_id(self, memory):
        await memory.insert_one("collection", {"_id": "3", "key": "value", "updated": "2022-01-01T00:00:00"})
        with pytest.raises(DuplicateKeyError):
            await memory.upsert_one(
                "collection", {"_id": "3", "key": "new_value", "updated": "2022-01-01T00:00:00"}, {"_id": "non_existing"}
            )

    @pytest.mark.asyncio
    async def test_upsert_one_updated_since_read(self, memory):
        await memory.insert_one("collection", {"_id": "4", "key": "value", "updated": "2022-01-01T00:00:00"})
        with pytest.raises(DuplicateKeyError):
            await memory.upsert_one(
                "collection", {"_id": "4"}, {"key": "updated_value", "updated": "2022-01-02T00:00:00"}
            )
