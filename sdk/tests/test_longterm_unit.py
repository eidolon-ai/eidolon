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
from eidolon_ai_sdk.apu.longterm_memory_unit import LongTermMemoryUnit, LongTermMemoryUnitConfig
from eidolon_ai_sdk.apu.longterm_memory_unit import LongTermMemoryUnitScope
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
def test_spec(test_name):
    yield LongTermMemoryUnitConfig(collection_name=test_name)


@fixture
async def user_proc_unit(machine, test_spec):
    yield LongTermMemoryUnit(Reference[LLMUnit, LLMUnit.__name__]().instantiate(), LongTermMemoryUnitScope.USER_PROCESS, spec=test_spec)


@fixture
async def user_proc_unit_const_score(machine, test_spec):
    yield LongTermMemoryUnit(Reference[LLMUnit, LLMUnit.__name__]().instantiate(), LongTermMemoryUnitScope.USER_PROCESS, memory_converter=constantScore, spec=test_spec)


@fixture
async def user_agent_unit(machine, test_spec):
    yield LongTermMemoryUnit(Reference[LLMUnit, LLMUnit.__name__]().instantiate(), LongTermMemoryUnitScope.USER_AGENT, spec=test_spec)


@fixture
async def user_unit(machine, test_spec):
    yield LongTermMemoryUnit(Reference[LLMUnit, LLMUnit.__name__]().instantiate(), LongTermMemoryUnitScope.USER, spec=test_spec)


@fixture
async def agent_unit(machine, test_spec):
    yield LongTermMemoryUnit(Reference[LLMUnit, LLMUnit.__name__]().instantiate(), LongTermMemoryUnitScope.AGENT, spec=test_spec)


@fixture
async def system_unit(machine, test_spec):
    yield LongTermMemoryUnit(Reference[LLMUnit, LLMUnit.__name__]().instantiate(), LongTermMemoryUnitScope.SYSTEM, spec=test_spec)


@pytest.fixture(scope="function", autouse=True)
def set_agent_user_context():
    User.set_current(User(id="test_user", extra={}))
    RequestContext.set("agent_name", "test_agent")
    RequestContext.set("process_id", "test_proc")


# test memory creation
@pytest.mark.vcr()
def test_create_memory(user_proc_unit: LongTermMemoryUnit):
    queryText = "Name is John Doe"
    data = UserMessage(content=[UserMessageText(text=queryText)])
    call_context = CallContext(process_id='test_proc')
    mem_list = user_proc_unit.storeMessage(call_context, data)
    assert len(mem_list) > 0
    mem_id = mem_list[-1]["id"]
    retreived = user_proc_unit.getMemory(mem_id)
    assert "John Doe" in retreived["text"]


# test memory updates
@pytest.mark.vcr()
def test_memory_update(user_proc_unit: LongTermMemoryUnit):
    query1Text = "My name is John Doe"
    data = UserMessage(content=[UserMessageText(text=query1Text)])
    call_context = CallContext(process_id='test_proc')
    mem_list = user_proc_unit.storeMessage(call_context, data)
    mem_id = mem_list[-1]["id"]

    query2Text = "My name is actually John Kapoor, not John Doe"
    data = UserMessage(content=[UserMessageText(text=query2Text)])
    user_proc_unit.storeMessage(call_context, data)
    mem = user_proc_unit.getMemory(mem_id)
    assert "John Kapoor" in mem["text"]


# test memory deletion
@pytest.mark.vcr()
def test_memory_delete(user_proc_unit_const_score: LongTermMemoryUnit):
    queryText = "My name is John Doe"
    data = UserMessage(content=[UserMessageText(text=queryText)])
    call_context = CallContext(process_id='test_proc')
    mem_list = user_proc_unit_const_score.storeMessage(call_context, data)
    if len(mem_list) > 0:
        mem_id = mem_list[-1]["id"]
        user_proc_unit_const_score.deleteMemory(mem_id)
        assert user_proc_unit_const_score.getMemory(mem_id) is None

    query1Text = "bicycles have wheels"
    data = UserMessage(content=[UserMessageText(text=query1Text)])
    mem_id_1 = user_proc_unit_const_score.storeMessage(call_context, data)[-1]["id"]
    query2Text = "the sky is blue"
    data = UserMessage(content=[UserMessageText(text=query2Text)])
    mem_id_2 = user_proc_unit_const_score.storeMessage(call_context, data)[-1]["id"]
    user_proc_unit_const_score.deleteMemoriesForProcess("test_proc")
    assert user_proc_unit_const_score.getMemory(mem_id_1) is None and user_proc_unit_const_score.getMemory(mem_id_2) is None


# test memory search
@pytest.mark.vcr()
def test_memory_search(user_proc_unit: LongTermMemoryUnit):
    queryText = "My name is John Doe"
    data = UserMessage(content=[UserMessageText(text=queryText)])
    call_context = CallContext(process_id='test_proc')
    user_proc_unit.storeMessage(call_context, data)
    res = user_proc_unit.searchMemories(call_context, "what is my name")
    assert "John Doe" in res[-1]["text"]


# test memory history
@pytest.mark.vcr()
def test_memory_history(user_proc_unit_const_score: LongTermMemoryUnit):
    queryText = "My name is John Doe"
    data = UserMessage(content=[UserMessageText(text=queryText)])
    call_context = CallContext(process_id='test_proc')
    mem_id = user_proc_unit_const_score.storeMessage(call_context, data)[-1]['id']
    query2Text = "My name is actually John Kapoor, not John Doe"
    data = UserMessage(content=[UserMessageText(text=query2Text)])
    user_proc_unit_const_score.storeMessage(call_context, data)
    history = user_proc_unit_const_score.getMemoryHistory(mem_id)
    assert len(history) > 0


# add memory for one process and make sure it doesn't come up when searched
# by another process unless the query is made by the appropriate unit
@pytest.mark.vcr()
def test_proc_scoping(user_proc_unit: LongTermMemoryUnit, user_unit: LongTermMemoryUnit, agent_unit: LongTermMemoryUnit):
    queryText = "My name is John Doe"
    data = UserMessage(content=[UserMessageText(text=queryText)])
    call_context = CallContext(process_id='test_proc_1')
    user_proc_unit.storeMessage(call_context, data)
    searchRes = user_proc_unit.searchMemories(call_context, "what is my name?")
    assert len(searchRes) > 0
    call_context = CallContext(process_id='test_proc_2')
    searchRes2 = user_proc_unit.searchMemories(call_context, "what is my name?")
    assert len(searchRes2) < 1

    queryText = "My name is John Doe"
    data = UserMessage(content=[UserMessageText(text=queryText)])
    call_context = CallContext(process_id='test_proc_1')
    user_unit.storeMessage(call_context, data)
    searchRes = user_unit.searchMemories(call_context, "what is my name?")
    assert len(searchRes) > 0
    call_context = CallContext(process_id='test_proc_2')
    searchRes2 = user_unit.searchMemories(call_context, "what is my name?")
    assert len(searchRes2) > 0

    queryText = "My name is John Doe"
    data = UserMessage(content=[UserMessageText(text=queryText)])
    call_context = CallContext(process_id='test_proc_1')
    agent_unit.storeMessage(call_context, data)
    searchRes = agent_unit.searchMemories(call_context, "what is my name?")
    assert len(searchRes) > 0
    call_context = CallContext(process_id='test_proc_2')
    searchRes2 = agent_unit.searchMemories(call_context, "what is my name?")
    assert len(searchRes2) > 0


# add memory for a user and make sure it only shows up for appropriately
# scoped units + agents
@pytest.mark.vcr()
def test_user_agent_scoping(user_unit: LongTermMemoryUnit, user_agent_unit: LongTermMemoryUnit, agent_unit: LongTermMemoryUnit):
    queryText = "My name is John Doe"
    data = UserMessage(content=[UserMessageText(text=queryText)])
    call_context = CallContext(process_id='test_proc')
    user_unit.storeMessage(call_context, data)
    searchRes = user_unit.searchMemories(call_context, "what is my name?")
    assert len(searchRes) > 0
    User.set_current(User(id="test_user_2", extra={}))
    searchRes2 = user_unit.searchMemories(call_context, "what is my name?")
    assert len(searchRes2) < 1

    queryText = "My name is John Doe"
    data = UserMessage(content=[UserMessageText(text=queryText)])
    call_context = CallContext(process_id='test_proc')
    user_agent_unit.storeMessage(call_context, data)
    searchRes = user_agent_unit.searchMemories(call_context, "what is my name?")
    assert len(searchRes) > 0
    User.set_current(User(id="test_user_3", extra={}))
    searchRes2 = user_agent_unit.searchMemories(call_context, "what is my name?")
    assert len(searchRes2) < 1

    queryText = "My name is John Doe"
    data = UserMessage(content=[UserMessageText(text=queryText)])
    call_context = CallContext(process_id='test_proc')
    agent_unit.storeMessage(call_context, data)
    searchRes = agent_unit.searchMemories(call_context, "what is my name?")
    assert len(searchRes) > 0
    User.set_current(User(id="test_user_4", extra={}))
    searchRes2 = agent_unit.searchMemories(call_context, "what is my name?")
    assert len(searchRes2) > 0
    RequestContext.set("agent_name", "test_agent_2")
    searchRes2 = agent_unit.searchMemories(call_context, "what is my name?")
    assert len(searchRes2) < 1


# make sure system scoping ignores everything
@pytest.mark.vcr()
def test_system_scoping(system_unit: LongTermMemoryUnit):
    queryText = "My name is John Doe"
    data = UserMessage(content=[UserMessageText(text=queryText)])
    call_context = CallContext(process_id='test_proc')
    system_unit.storeMessage(call_context, data)
    searchRes = system_unit.searchMemories(call_context, "what is my name?")
    assert len(searchRes) > 0
    User.set_current(User(id="test_user_4", extra={}))
    searchRes2 = system_unit.searchMemories(call_context, "what is my name?")
    assert len(searchRes2) > 0
    RequestContext.set("agent_name", "test_agent_2")
    searchRes2 = system_unit.searchMemories(call_context, "what is my name?")
    assert len(searchRes2) > 0
