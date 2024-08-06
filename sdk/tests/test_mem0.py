import uuid
from unittest.mock import patch

import pytest
from mem0 import Memory
from pytest_asyncio import fixture

from eidolon_ai_sdk.apu.llm_unit import LLMUnit
from eidolon_ai_sdk.apu.mem0 import EidolonMem0
from eidolon_ai_sdk.system.reference_model import Reference

class _wrapper:
    i = 0

@pytest.fixture(autouse=True)
def with_mocked_mem0_timestamp():
    _wrapper.i = 0
    def pert_test_iter():
        _wrapper.i += 1
        return uuid.UUID(f"00000000-0000-0000-0000-{_wrapper.i:012d}")

    with patch("mem0.memory.main.uuid.uuid4") as mem0uuid:
        mem0uuid.side_effect = pert_test_iter
        yield


@fixture
async def memory_store(test_name, machine):
    yield EidolonMem0(Reference[LLMUnit, LLMUnit.__name__]().instantiate(), test_name)


@pytest.mark.vcr()
def test_create_memory(memory_store: Memory):
    data = "Name is John Doe."
    memory_id = memory_store.add(data=data)[-1]["id"]
    assert memory_store.get(memory_id)['text'] == data


@pytest.mark.vcr()
def test_get_memory(memory_store):
    data = "Name is John Doe."
    memory_id = memory_store.add(data=data)[-1]["id"]
    retrieved_data = memory_store.get(memory_id)
    assert retrieved_data['text'] == data


@pytest.mark.vcr()
def test_update_memory(memory_store):
    data = "Name is John Doe."
    memory_id = memory_store.add(data=data)[-1]["id"]
    new_data = "Name is John Kapoor."
    memory_store.update(memory_id, new_data)
    updated_memory = memory_store.get(memory_id)
    assert updated_memory['text'] == new_data
    assert memory_store.get(memory_id)['text'] == new_data


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
    assert memory_store.get(memory_id)['text'] == "Prefers Indian food"

    new_data = "I like italian food."
    memory_store.update(memory_id, new_data)
    history = memory_store.history(memory_id)
    assert [h["new_value"] for h in history] == ["Prefers Indian food", new_data]
    assert memory_store.get(memory_id)['text'] == new_data


# @pytest.mark.skip("todo")
@pytest.mark.vcr()
def test_list_memories(memory_store):
    data1 = "Name is John Doe."
    data2 = "Name is John Doe. I like to code in Python."
    memory_store.add(data=data1)
    memory_store.add(data=data2)
    memories = memory_store.get_all()
    assert "john doe" in str(memories).lower()
    assert "likes to code in python" in str(memories).lower()
