from unittest.mock import AsyncMock, MagicMock

import pytest

from eidolon_sdk.cpu.agent_bus import BusEvent, BusController
from eidolon_sdk.cpu.bus_messages import AddConversationHistory, LLMResponse, LLMEvent, InputRequest
from eidolon_sdk.cpu.llm_message import LLMMessage, SystemMessage, AssistantMessage
# Assuming the classes are in a module named 'my_module', which needs to be imported here.
from eidolon_sdk.cpu.memory_unit import ConversationalMemoryUnit


# Mocking the LLMMessage for testing purposes
class MockLLMMessage(LLMMessage):
    text: str
    type: str = "mock"


@pytest.fixture
def agent_machine():
    machine = AsyncMock()

    # Assign the asynchronous generator function to the find method
    machine.agent_memory.find = AsyncMock()
    # The insert_one method can stay as a simple AsyncMock if it's just for acknowledgment of the insert.
    machine.agent_memory.insert_one = AsyncMock()

    return machine


@pytest.fixture
def bus_event():
    return BusEvent(process_id="process1", thread_id=1, message=AddConversationHistory(messages=[SystemMessage(content="hi there")], output_format={}))


@pytest.fixture
def bus_controller():
    return BusController()


@pytest.fixture
def memory_unit(agent_machine, bus_controller):
    memory_unit = ConversationalMemoryUnit(agent_machine, bus_controller)
    memory_unit.request_write = AsyncMock()
    return memory_unit


async def make_async_find_generator(messages):
    async def async_find_generator(_, __):
        for message in messages:
            yield message

    return async_find_generator


@pytest.mark.asyncio
class TestConversationalMemoryUnit:
    async def test_bus_read_add_conversation_history(self, memory_unit, bus_event, agent_machine):
        existing_messages = [{
            "process_id": "process1",
            "thread_id": 1,
            "message": MockLLMMessage(text="Message 1").model_dump()
        }, {
            "process_id": "process1",
            "thread_id": 1,
            "message": MockLLMMessage(text="Message 2").model_dump()
        }]

        agent_machine.agent_memory.symbolic_memory.find = await make_async_find_generator(existing_messages)
        memory_unit.request_write = MagicMock()

        # Perform the bus read
        await memory_unit.bus_read(bus_event)

        # Check if insert_one was called with correct arguments
        for message in bus_event.message.messages:
            agent_machine.agent_memory.symbolic_memory.insert_one.assert_awaited_once_with("conversation_memory", {
                "process_id": bus_event.process_id,
                "thread_id": bus_event.thread_id,
                "message": message.model_dump()
            })

    async def test_bus_read_llm_response(self, memory_unit, agent_machine):
        # Create an event for llm_response
        llm_response_event = BusEvent(process_id="process1", thread_id=1, message=LLMResponse(message=AssistantMessage(content={"hello": "there"}, tool_calls=None)))

        # Perform the bus read
        await memory_unit.bus_read(llm_response_event)

        # Check if insert_one was called with the correct arguments
        agent_machine.agent_memory.symbolic_memory.insert_one.assert_awaited_once_with("conversation_memory", {
            "process_id": llm_response_event.process_id,
            "thread_id": llm_response_event.thread_id,
            "message": llm_response_event.message.message.model_dump()
        })

    async def test_bus_read_with_existing_messages(self, memory_unit, bus_event, agent_machine):
        # Set up existing messages
        existing_messages = [{
            "process_id": "process1",
            "thread_id": 1,
            "message": MockLLMMessage(text="Message 1").model_dump()},
            {
                "process_id": "process1",
                "thread_id": 1,
                "message": MockLLMMessage(text="Message 2").model_dump()}]

        agent_machine.agent_memory.symbolic_memory.find = await make_async_find_generator(existing_messages)
        memory_unit.request_write = MagicMock()

        # Perform the bus read
        await memory_unit.bus_read(bus_event)

        # Check if request_write was called with the correct BusEvent
        expected_messages = [message["message"] for message in existing_messages] + bus_event.message.messages
        expected_bus_event = BusEvent(bus_event.process_id, bus_event.thread_id, LLMEvent(messages = expected_messages, output_format = {}))
        memory_unit.request_write.assert_called_once_with(expected_bus_event)

    async def test_event_type_not_handled(self, memory_unit, agent_machine):
        # Create an event with an unhandled event type
        unhandled_event = BusEvent(process_id="process1", thread_id=1, message=InputRequest(messages=[SystemMessage(content="hello")], output_format={}))

        # Perform the bus read and verify that no interactions with the agent memory occur
        await memory_unit.bus_read(unhandled_event)
        agent_machine.agent_memory.symbolic_memory.find.assert_not_called()
        agent_machine.agent_memory.symbolic_memory.insert_one.assert_not_called()

# It's assumed that the Bus and BusEvent classes are already defined elsewhere.
