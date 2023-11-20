from unittest.mock import AsyncMock, MagicMock

import pytest
from jinja2 import UndefinedError
from pydantic import ValidationError

from eidolon_sdk.cpu.agent_bus import BusEvent, Bus, BusController, CallContext
from eidolon_sdk.cpu.agent_io import UserTextCPUMessage, CPUMessage, SystemCPUMessage, ImageURLCPUMessage, IOUnit, \
    ResponseHandler, IOUnitConfig
from eidolon_sdk.cpu.bus_messages import InputRequest
from eidolon_sdk.cpu.llm_message import UserMessageText, UserMessage, UserMessageImageURL, SystemMessage
from eidolon_sdk.impl.local_symbolic_memory import LocalSymbolicMemory


# Assuming the IOUnit and other related classes are in a module named 'io_unit_module', which needs to be imported here.
# from io_unit_module import IOUnit, UserTextCPUMessage, ImageURLCPUMessage, SystemCPUMessage, Bus, AgentCPU, BusEvent

@pytest.fixture
def response_handler():
    rh = MagicMock(spec=ResponseHandler)
    rh.handle = AsyncMock()
    return rh


@pytest.fixture
def bus_controller():
    return BusController()


@pytest.fixture
def memory_unit():
    return LocalSymbolicMemory()


@pytest.fixture
def io_config():
    return IOUnitConfig(io_read='mock_io_read', io_write='mock_io_write')


@pytest.fixture
def io_unit(bus_controller, response_handler, memory_unit, io_config):
    io_unit = IOUnit(io_config)
    io_unit.initialize(response_handler, bus_controller=bus_controller, cpu=None, memory=memory_unit)
    bus_controller.add_participant(io_unit)
    return io_unit


@pytest.fixture
def bus():
    return Bus()


@pytest.fixture
def bus_event(io_config):
    return BusEvent(
        CallContext(process_id="process1", thread_id="0", output_format={}),
        io_config.io_read, messages=[SystemMessage(content="Test Response")]
    )


@pytest.mark.asyncio
class TestIOUnit:
    async def test_bus_read_output_response(self, io_unit, bus, bus_event, response_handler):
        bus.current_event = bus_event
        await io_unit.bus_read(bus_event)
        response_handler.handle.assert_awaited_once_with(bus_event.call_context.process_id, bus_event.messages[0].content)

    def test_process_request_with_user_prompt(self, io_unit):
        prompts = [UserTextCPUMessage(type="user", prompt="Hello, {{ name }}")]
        input_data = {"name": "World"}
        io_unit.request_write = MagicMock()
        io_unit.process_request("process1", prompts, input_data, {})
        expected_message = UserMessage(type='user', content=[UserMessageText(type='text', text='Hello, World')])
        io_unit.request_write.assert_called_once_with(BusEvent(CallContext("process1", 0, {}), event_type="mock_io_write", messages=[expected_message]))

    def test_process_request_with_system_prompt(self, io_unit):
        prompts = [SystemCPUMessage(type="system", prompt="System update complete.")]
        io_unit.request_write = MagicMock()
        io_unit.process_request("process2", prompts, {}, {})
        expected_message = SystemMessage(content="System update complete.")
        io_unit.request_write.assert_called_once_with(BusEvent(CallContext("process2", 0, {}), event_type="mock_io_write", messages=[expected_message]))

    def test_process_request_with_image_url_prompt(self, io_unit):
        prompts = [ImageURLCPUMessage(type="image_url", prompt="https://example.com/image.jpg")]
        io_unit.request_write = MagicMock()
        io_unit.process_request("process3", prompts, {}, {})
        expected_message = UserMessage(content=[UserMessageImageURL(image_url="https://example.com/image.jpg")])
        io_unit.request_write.assert_called_once_with(BusEvent(CallContext("process3", 0, {}), event_type="mock_io_write", messages=[expected_message]))

    def test_process_request_with_mixed_prompts(self, io_unit):
        prompts = [
            UserTextCPUMessage(type="user", prompt="Hello, {{ name }}"),
            SystemCPUMessage(type="system", prompt="System update complete."),
            ImageURLCPUMessage(type="image_url", prompt="https://example.com/image.jpg")
        ]
        input_data = {"name": "World"}
        io_unit.request_write = MagicMock()
        io_unit.process_request("process4", prompts, input_data, {})
        expected_messages = [
            SystemMessage(content="System update complete."),
            UserMessage(content=[
                UserMessageText(text="Hello, World"),
                UserMessageImageURL(image_url="https://example.com/image.jpg")
            ])
        ]

        io_unit.request_write.assert_called_once_with(BusEvent(CallContext("process4", 0, {}), event_type="mock_io_write", messages=expected_messages))

    def test_process_request_with_invalid_prompt_type(self, io_unit):
        prompts = [CPUMessage(type="invalid_type", prompt="This should fail.")]
        with pytest.raises(ValueError) as excinfo:
            io_unit.process_request("process5", prompts, {}, {})
        assert "Input should be a valid dictionary or instance of UserTextCPUMessage" in str(excinfo.value)

    def test_process_request_with_template_rendering(self, io_unit):
        prompts = [UserTextCPUMessage(type="user", prompt="Hello, {{ name }}")]
        input_data = {"name": "World"}
        io_unit.request_write = MagicMock()
        io_unit.process_request("process6", prompts, input_data, {})
        expected_message = UserMessage(content=[UserMessageText(text="Hello, World")])
        io_unit.request_write.assert_called_once_with(BusEvent(CallContext("process6", 0, {}), event_type="mock_io_write", messages=[expected_message]))

    def test_process_request_with_missing_template_data(self, io_unit):
        prompts = [UserTextCPUMessage(type="user", prompt="Hello, {{ name }}")]
        with pytest.raises(UndefinedError):
            io_unit.process_request("process7", prompts, {}, {})

    def test_process_request_validation_error(self, io_unit):
        with pytest.raises(ValidationError):
            io_unit.process_request("process8", [{}], {}, {})  # Empty prompt should raise validation error
