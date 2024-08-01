from mem0 import Memory
from pytest_asyncio import fixture

from eidolon_ai_sdk.apu.llm_unit import LLMUnit
from eidolon_ai_sdk.apu.mem0 import EidolonMem0
from eidolon_ai_sdk.system.reference_model import Reference


@fixture
async def memory_store(test_name, machine):
    yield EidolonMem0(Reference[LLMUnit, LLMUnit.__name__]().instantiate(), test_name)


def test_create_memory(memory_store: Memory):
    data = "Name is John Doe."
    memory_id = memory_store.add(data=data)[-1]["id"]
    assert memory_store.get(memory_id)['text'] == data


def test_get_memory(memory_store):
    data = "Name is John Doe."
    memory_id = memory_store.add(data=data)[-1]["id"]
    retrieved_data = memory_store.get(memory_id)
    assert retrieved_data['text'] == data


def test_update_memory(memory_store):
    data = "Name is John Doe."
    memory_id = memory_store.add(data=data)[-1]["id"]
    new_data = "Name is John Kapoor."
    updated_memory = memory_store.update(memory_id, new_data)
    assert updated_memory['text'] == new_data
    assert memory_store.get(memory_id)['text'] == new_data


def test_delete_memory(memory_store):
    data = "Name is John Doe."
    memory_id = memory_store.add(data=data)[-1]["id"]
    memory_store.delete(memory_id)
    assert memory_store.get(memory_id)['text'] is None


def test_history(memory_store):
    data = "I like indian food."
    memory_id = memory_store.add(data=data)[-1]["id"]
    history = memory_store.history(memory_id)
    assert history == [data]
    assert memory_store.get(memory_id)['text'] == data

    new_data = "I like italian food."
    memory_store.update(memory_id, new_data)
    history = memory_store.history(memory_id)
    assert history == [data, new_data]
    assert memory_store.get(memory_id)['text'] == new_data


def test_list_memories(memory_store):
    data1 = "Name is John Doe."
    data2 = "Name is John Doe. I like to code in Python."
    memory_store.add(data=data1)
    memory_store.add(data=data2)
    memories = memory_store.get_all()
    assert data1 in memories
    assert data2 in memories
