from unittest.mock import AsyncMock, MagicMock

import pytest

from eidolon_sdk.agent_machine import AgentMachine
from eidolon_sdk.cpu.agent_bus import BusEvent, BusController, CallContext
from eidolon_sdk.cpu.bus_messages import AddConversationHistory, LLMResponse, LLMEvent, InputRequest
from eidolon_sdk.cpu.llm_message import LLMMessage, SystemMessage, AssistantMessage
# Assuming the classes are in a module named 'my_module', which needs to be imported here.
from eidolon_sdk.cpu.memory_unit import MemoryUnitConfig
from eidolon_sdk.impl.conversation_memory_unit import ConversationalMemoryUnit
from eidolon_sdk.impl.local_symbolic_memory import LocalSymbolicMemory


# Mocking the LLMMessage for testing purposes
class MockLLMMessage(LLMMessage):
    content: str
    type: str = "system"


@pytest.fixture
def agent_machine():
    machine = AsyncMock()

    # Assign the asynchronous generator function to the find method
    machine.agent_memory.find = AsyncMock()
    # The insert_one method can stay as a simple AsyncMock if it's just for acknowledgment of the insert.
    machine.agent_memory.insert_one = AsyncMock()

    return machine


@pytest.fixture
def bus_event(memory_unit):
    return BusEvent(
        call_context=CallContext(process_id="process1", thread_id=1, output_format={}),
        event_type=memory_unit.spec.msf_read,
        messages=[SystemMessage(content="hi there")]
    )


@pytest.fixture
def bus_controller():
    return BusController()


@pytest.fixture
def memory_unit(agent_machine: AgentMachine, bus_controller):
    memory_unit = ConversationalMemoryUnit(MemoryUnitConfig(ms_read="ms_read", msf_read="msf_read", msf_write="msf_write"))
    memory_unit.initialize(bus_controller, cpu=None, memory=agent_machine.agent_memory)
    memory_unit.request_write = LocalSymbolicMemory()
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
            "message": MockLLMMessage(content="Message 1").model_dump()
        }, {
            "process_id": "process1",
            "thread_id": 1,
            "message": MockLLMMessage(content="Message 2").model_dump()
        }]

        agent_machine.agent_memory.symbolic_memory.find = await make_async_find_generator(existing_messages)
        memory_unit.request_write = MagicMock()

        # Perform the bus read
        await memory_unit.bus_read(bus_event)

        # Check if insert_one was called with correct arguments
        for message in bus_event.messages:
            agent_machine.agent_memory.symbolic_memory.insert.assert_awaited_once_with("conversation_memory", [{
                "process_id": bus_event.call_context.process_id,
                "thread_id": bus_event.call_context.thread_id,
                "message": message.model_dump()
            }])

    async def test_bus_read_llm_response(self, memory_unit, agent_machine):
        # Create an event for llm_response
        llm_response_event = BusEvent(
            CallContext(process_id="process1", thread_id=1, output_format={}),
            event_type="ms_read",
            messages=[AssistantMessage(content={"hello": "there"}, tool_calls=None)]
        )

        # Perform the bus read
        await memory_unit.bus_read(llm_response_event)

        # Check if insert_one was called with the correct arguments
        agent_machine.agent_memory.symbolic_memory.insert.assert_awaited_once_with("conversation_memory", [{
            "process_id": llm_response_event.call_context.process_id,
            "thread_id": llm_response_event.call_context.thread_id,
            "message": llm_response_event.messages[0].model_dump()
        }])

    async def test_bus_read_with_existing_messages(self, memory_unit, bus_event, agent_machine):
        agent_machine.agent_memory.symbolic_memory = LocalSymbolicMemory()
        agent_machine.agent_memory.symbolic_memory.start()

        # Set up existing messages
        existing_messages = [{
            "process_id": "process1",
            "thread_id": 1,
            "message": MockLLMMessage(content="Message 1").model_dump()
        }, {
            "process_id": "process1",
            "thread_id": 1,
            "message": MockLLMMessage(content="Message 2").model_dump()
        }]

        # Insert existing messages into LocalSymbolicMemory
        await agent_machine.agent_memory.symbolic_memory.insert('conversation_memory', existing_messages)

        memory_unit.request_write = MagicMock()

        # Perform the bus read
        await memory_unit.bus_read(bus_event)

        # Check if request_write was called with the correct BusEvent
        expected_messages = [SystemMessage(**message["message"]) for message in existing_messages] + bus_event.messages
        expected_bus_event = BusEvent(bus_event.call_context, memory_unit.spec.msf_write, expected_messages)
        memory_unit.request_write.assert_called_once_with(expected_bus_event)

    async def test_event_type_not_handled(self, memory_unit, agent_machine):
        # Create an event with an unhandled event type
        unhandled_event = BusEvent(
            CallContext(process_id="process1", thread_id=1, output_format={}),
            event_type="unhandled_event",
            messages=[SystemMessage(content="hello")]
        )

        # Perform the bus read and verify that no interactions with the agent memory occur
        await memory_unit.bus_read(unhandled_event)
        agent_machine.agent_memory.symbolic_memory.find.assert_not_called()
        agent_machine.agent_memory.symbolic_memory.insert_one.assert_not_called()

# It's assumed that the Bus and BusEvent classes are already defined elsewhere.
