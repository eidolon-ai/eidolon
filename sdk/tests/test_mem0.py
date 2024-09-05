import uuid
from typing import List
from unittest.mock import patch

import pytest
from mem0 import Memory
from pytest_asyncio import fixture
from qdrant_client.http.models import ScoredPoint

from eidolon_ai_sdk.apu.llm_unit import LLMUnit
from eidolon_ai_sdk.apu.mem0 import EidolonMem0
from eidolon_ai_sdk.system.reference_model import Reference


class MockUUID:
    def __init__(self):
        self.i = 0

    def uuid4(self):
        self.i += 1
        return uuid.UUID(f"00000000-0000-0000-0000-{self.i:012d}")


@pytest.fixture(autouse=True)
def deterministic_uuids(test_name):
    with patch("mem0.memory.main.uuid", new=MockUUID()):
        yield


def constantScore(scores: List[ScoredPoint]) -> List[ScoredPoint]:
    for score in scores:
        score.score = 1
    return scores


@fixture
async def memory_store(test_name, machine):
    yield EidolonMem0(Reference[LLMUnit, LLMUnit.__name__]().instantiate(), test_name)


@fixture
async def memory_store_const_score(test_name, machine):
    yield EidolonMem0(Reference[LLMUnit, LLMUnit.__name__]().instantiate(), test_name, memory_converter=constantScore)


@pytest.mark.vcr()
def test_create_memory(memory_store: Memory):
    data = "Name is John Doe."
    memory_id = memory_store.add(data=data)[-1]["id"]
    assert memory_store.get(memory_id)["text"] == data


@pytest.mark.vcr()
def test_get_memory(memory_store):
    data = "Name is John Doe."
    memory_id = memory_store.add(data=data)[-1]["id"]
    retrieved_data = memory_store.get(memory_id)
    assert retrieved_data["text"] == data


@pytest.mark.vcr()
def test_update_memory(memory_store):
    data = "Name is John Doe."
    memory_id = memory_store.add(data=data)[-1]["id"]
    new_data = "Name is John Kapoor."
    memory_store.update(memory_id, new_data)
    updated_memory = memory_store.get(memory_id)
    assert updated_memory["text"] == new_data
    assert memory_store.get(memory_id)["text"] == new_data


@pytest.mark.vcr()
def test_delete_memory(memory_store):
    data = "Name is John Doe."
    memory_id = memory_store.add(data=data)[-1]["id"]
    memory_store.delete(memory_id)
    assert memory_store.get(memory_id) is None


@pytest.mark.vcr()
def test_history(memory_store):
    data = "I like indian food."
    memory_id = memory_store.add(data=data)[-1]["id"]
    history = memory_store.history(memory_id)
    assert [h["new_value"] for h in history] == ["Prefers Indian food"]
    assert memory_store.get(memory_id)["text"] == "Prefers Indian food"

    new_data = "I like italian food."
    memory_store.update(memory_id, new_data)
    history = memory_store.history(memory_id)
    assert [h["new_value"] for h in history] == ["Prefers Indian food", new_data]
    assert memory_store.get(memory_id)["text"] == new_data


# @pytest.mark.skip("todo")
@pytest.mark.vcr()
def test_list_memories(memory_store_const_score):
    data1 = "Name is Fredrick."
    data2 = "Name is Fredrick. I like to code in Python."
    memory_store_const_score.add(data=data1)
    memory_store_const_score.add(data=data2)
    memories = memory_store_const_score.get_all()
    assert "fredrick" in str(memories).lower()
    assert "likes to code in python" in str(memories).lower()
