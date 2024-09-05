import uuid
from typing import List
from unittest.mock import patch

import pytest
from pytest_asyncio import fixture
from qdrant_client.http.models import ScoredPoint

from eidolon_ai_client.util.request_context import RequestContext
from eidolon_ai_sdk.apu.call_context import CallContext
from eidolon_ai_sdk.apu.llm_message import UserMessage, UserMessageText
from eidolon_ai_sdk.apu.llm_unit import LLMUnit
from eidolon_ai_sdk.apu.mem0_long_term_memory import Mem0LongTermMemoryUnit, Mem0LongTermMemoryUnitConfig
from eidolon_ai_sdk.security.user import User
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
async def user_unit(machine, test_name):
    yield Mem0LongTermMemoryUnit(Reference[LLMUnit, LLMUnit.__name__]().instantiate(), spec=Mem0LongTermMemoryUnitConfig(user_scoped=True, collection_name=test_name))


@fixture
async def user_unit_const_score(machine, test_name):
    yield Mem0LongTermMemoryUnit(Reference[LLMUnit, LLMUnit.__name__]().instantiate(), memory_converter=constantScore, spec=Mem0LongTermMemoryUnitConfig(user_scoped=True, collection_name=test_name))


@fixture
async def agent_unit(machine, test_name):
    yield Mem0LongTermMemoryUnit(Reference[LLMUnit, LLMUnit.__name__]().instantiate(), spec=Mem0LongTermMemoryUnitConfig(user_scoped=False, collection_name=test_name))


@pytest.fixture(scope="function", autouse=True)
def set_agent_user_context():
    User.set_current(User(id="test_user", extra={}))
    RequestContext.set("agent_name", "test_agent")
    RequestContext.set("process_id", "test_proc")


# test memory creation
@pytest.mark.vcr()
def test_create_memory(user_unit: Mem0LongTermMemoryUnit):
    queryText = "Name is John Doe"
    data = UserMessage(content=[UserMessageText(text=queryText)])
    call_context = CallContext(process_id='test_proc')
    mem_list = user_unit.store_message(call_context, data)
    assert len(mem_list) > 0
    mem_id = mem_list[-1]["id"]
    retreived = user_unit._get_memory(mem_id)
    assert "John Doe" in retreived["text"]


# test memory updates
@pytest.mark.vcr()
def test_memory_update(user_unit: Mem0LongTermMemoryUnit):
    query1Text = "My name is John Doe"
    data = UserMessage(content=[UserMessageText(text=query1Text)])
    call_context = CallContext(process_id='test_proc')
    mem_list = user_unit.store_message(call_context, data)
    mem_id = mem_list[-1]["id"]

    query2Text = "My name is actually John Kapoor, not John Doe"
    data = UserMessage(content=[UserMessageText(text=query2Text)])
    user_unit.store_message(call_context, data)
    mem = user_unit._get_memory(mem_id)
    assert "John Kapoor" in mem["text"]


# test memory deletion
@pytest.mark.vcr()
def test_memory_delete(user_unit_const_score: Mem0LongTermMemoryUnit):
    call_context = CallContext(process_id='test_proc')
    query1Text = "bicycles have wheels"
    data = UserMessage(content=[UserMessageText(text=query1Text)])
    mem_id_1 = user_unit_const_score.store_message(call_context, data)[-1]["id"]
    query2Text = "the sky is blue"
    data = UserMessage(content=[UserMessageText(text=query2Text)])
    mem_id_2 = user_unit_const_score.store_message(call_context, data)[-1]["id"]
    user_unit_const_score.delete_memories_for_process("test_proc")
    assert user_unit_const_score._get_memory(mem_id_1) is None and user_unit_const_score._get_memory(mem_id_2) is None


# test memory search
@pytest.mark.vcr()
def test_memory_search(user_unit: Mem0LongTermMemoryUnit):
    queryText = "My name is John Doe"
    data = UserMessage(content=[UserMessageText(text=queryText)])
    call_context = CallContext(process_id='test_proc')
    user_unit.store_message(call_context, data)
    res = user_unit.search_memories("what is my name")
    assert "John Doe" in res[-1]["text"]


# add memory for a user and make sure it only shows up for appropriately
# scoped units + agents
@pytest.mark.vcr()
def test_user_agent_scoping(user_unit: Mem0LongTermMemoryUnit, agent_unit: Mem0LongTermMemoryUnit):
    queryText = "My name is John Doe"
    data = UserMessage(content=[UserMessageText(text=queryText)])
    call_context = CallContext(process_id='test_proc')
    user_unit.store_message(call_context, data)
    searchRes = user_unit.search_memories("what is my name?")
    assert len(searchRes) > 0
    User.set_current(User(id="test_user_2", extra={}))
    searchRes2 = user_unit.search_memories("what is my name?")
    assert len(searchRes2) < 1

    queryText = "My name is John Doe"
    data = UserMessage(content=[UserMessageText(text=queryText)])
    call_context = CallContext(process_id='test_proc')
    agent_unit.store_message(call_context, data)
    searchRes = agent_unit.search_memories("what is my name?")
    assert len(searchRes) > 0
    User.set_current(User(id="test_user_4", extra={}))
    searchRes2 = agent_unit.search_memories("what is my name?")
    assert len(searchRes2) > 0
