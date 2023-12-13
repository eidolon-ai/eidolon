import pytest

from eidos.memory.local_symbolic_memory import LocalSymbolicMemory, _DB


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
        assert _DB == {}, "Database should be initialized as an empty dictionary."

    def test_stop(self, memory):
        _DB["test"] = "value"
        memory.stop()
        assert _DB == {}, "Database should be cleared after stop."

    @pytest.mark.asyncio
    async def test_insert_one(self, memory):
        await memory.insert_one("collection", {"key": "value"})
        assert "collection" in _DB
        assert _DB["collection"][0] == {"key": "value"}

    @pytest.mark.asyncio
    async def test_insert(self, memory):
        documents = [{"key1": "value1"}, {"key2": "value2"}]
        await memory.insert("collection", documents)
        assert len(_DB["collection"]) == 2

    # ... more tests for the rest of the CRUD operations ...

    @pytest.mark.asyncio
    async def test_matches_query_simple(self, memory):
        await memory.insert_one("collection", {"key": "value"})
        assert memory._matches_query({"key": "value"}, {"key": "value"})

    @pytest.mark.asyncio
    async def test_matches_query_complex(self, memory):
        document = {
            "name": "John",
            "age": 30,
            "address": {"city": "New York", "zip": "10001"},
        }
        query = {"name": "John", "address": {"city": "New York"}}
        await memory.insert_one("collection", document)
        assert memory._matches_query(document, query)

    # Tests for MongoDB-like query operations
    @pytest.mark.asyncio
    async def test_matches_query_with_operators(self, memory):
        document = {"age": 25}
        await memory.insert_one("collection", document)
        assert memory._matches_query(document, {"age": {"$gt": 20}})
        assert not memory._matches_query(document, {"age": {"$lt": 20}})

    # ... more tests for other MongoDB-like query operations ...

    # Tests for update operations with MongoDB-like modifiers
    @pytest.mark.asyncio
    async def test_update_with_set(self, memory):
        document = {"name": "John", "age": 30}
        await memory.insert_one("collection", document)
        update = {"$set": {"age": 31}}
        memory._apply_update_modifiers(document, update)
        assert document["age"] == 31

    # ... more tests for other MongoDB-like update modifiers ...

    # Tests for upsert operations
    @pytest.mark.asyncio
    async def test_upsert_one_existing(self, memory):
        await memory.insert_one("collection", {"key": "value", "counter": 1})
        update = {"$set": {"counter": 2}}
        await memory.upsert_one("collection", update, {"key": "value"})
        assert _DB["collection"][0]["counter"] == 2

    @pytest.mark.asyncio
    async def test_upsert_one_new(self, memory):
        await memory.upsert_one("collection", {"key": "new_value"}, {"key": "non_existing"})
        assert _DB["collection"][0]["key"] == "new_value"

    # ... more tests to cover all edge cases and operations ...
