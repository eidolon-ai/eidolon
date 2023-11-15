from unittest.mock import AsyncMock, MagicMock

import pytest

from eidolon_sdk.cpu.agent_bus import BusEvent, Bus
from eidolon_sdk.cpu.llm_message import LLMMessage
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
    return BusEvent(process_id="process1", thread_id=1, event_type="add_conversation_history", event_data={
        "messages": [{"text": "Hi there!", "type": "mock"}],
        "output_format": {}
    })


@pytest.fixture
def memory_unit(agent_machine):
    memory_unit = ConversationalMemoryUnit(agent_machine)
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

        agent_machine.agent_memory.find = await make_async_find_generator(existing_messages)
        memory_unit.request_write = MagicMock()

        bus = Bus()
        # Simulate the bus event
        bus.current_event = bus_event

        # Perform the bus read
        await memory_unit.bus_read(bus)

        # Check if insert_one was called with correct arguments
        for message in bus_event.event_data["messages"]:
            agent_machine.agent_memory.insert_one.assert_awaited_once_with("conversation_memory", {
                "process_id": bus_event.process_id,
                "thread_id": bus_event.thread_id,
                "message": message
            })

    async def test_bus_read_llm_response(self, memory_unit, agent_machine):
        # Create an event for llm_response
        llm_response_event = BusEvent(process_id="process1", thread_id=1, event_type="llm_response", event_data={"message": MockLLMMessage(text="Response message").model_dump()})

        bus = Bus()
        # Simulate the bus event
        bus.current_event = llm_response_event

        # Perform the bus read
        await memory_unit.bus_read(bus)

        # Check if insert_one was called with the correct arguments
        agent_machine.agent_memory.insert_one.assert_awaited_once_with("conversation_memory", {
            "process_id": llm_response_event.process_id,
            "thread_id": llm_response_event.thread_id,
            "message": llm_response_event.event_data["message"]
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

        agent_machine.agent_memory.find = await make_async_find_generator(existing_messages)
        memory_unit.request_write = MagicMock()

        bus = Bus()
        # Simulate the bus event
        bus.current_event = bus_event

        # Perform the bus read
        await memory_unit.bus_read(bus)

        # Check if request_write was called with the correct BusEvent
        expected_messages = [message["message"] for message in existing_messages] + bus_event.event_data["messages"]
        expected_event_data = {"messages": expected_messages, "output_format": {}}
        expected_bus_event = BusEvent(bus_event.process_id, bus_event.thread_id, "llm_event", expected_event_data)
        memory_unit.request_write.assert_called_once_with(expected_bus_event)

    async def test_event_type_not_handled(self, memory_unit, agent_machine):
        # Create an event with an unhandled event type
        unhandled_event = BusEvent(process_id="process1", thread_id=1, event_type="unhandled_event", event_data={})

        bus = Bus()
        # Simulate the bus event
        bus.current_event = unhandled_event

        # Perform the bus read and verify that no interactions with the agent memory occur
        await memory_unit.bus_read(bus)
        agent_machine.agent_memory.find.assert_not_called()
        agent_machine.agent_memory.insert_one.assert_not_called()

# It's assumed that the Bus and BusEvent classes are already defined elsewhere.
