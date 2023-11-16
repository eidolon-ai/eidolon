from unittest.mock import AsyncMock, MagicMock

import pytest
from jinja2 import UndefinedError
from pydantic import ValidationError

from eidolon_sdk.cpu.agent_bus import BusEvent, Bus
from eidolon_sdk.cpu.agent_cpu import AgentCPU
from eidolon_sdk.cpu.agent_io import UserTextCPUMessage, CPUMessage, SystemCPUMessage, ImageURLCPUMessage, IOUnit
from eidolon_sdk.cpu.bus_messages import OutputResponse, InputRequest
from eidolon_sdk.cpu.llm_message import UserMessageText, UserMessage, UserMessageImageURL, SystemMessage


# Assuming the IOUnit and other related classes are in a module named 'io_unit_module', which needs to be imported here.
# from io_unit_module import IOUnit, UserTextCPUMessage, ImageURLCPUMessage, SystemCPUMessage, Bus, AgentCPU, BusEvent

@pytest.fixture
def agent_cpu():
    cpu = MagicMock(spec=AgentCPU)
    cpu.respond = AsyncMock()
    return cpu


@pytest.fixture
def io_unit(agent_cpu):
    return IOUnit(agent_cpu=agent_cpu)


@pytest.fixture
def bus():
    return Bus()


@pytest.fixture
def bus_event():
    return BusEvent(process_id="process1", thread_id=0, message=OutputResponse(response={"response": "Test Response"}))


@pytest.mark.asyncio
class TestIOUnit:
    async def test_bus_read_output_response(self, io_unit, bus, bus_event, agent_cpu):
        bus.current_event = bus_event
        await io_unit.bus_read(bus_event)
        agent_cpu.respond.assert_awaited_once_with(bus_event.process_id, bus_event.message.response)

    def test_process_request_with_user_prompt(self, io_unit):
        prompts = [UserTextCPUMessage(type="user", prompt="Hello, {{ name }}")]
        input_data = {"name": "World"}
        io_unit.request_write = MagicMock()
        io_unit.process_request("process1", prompts, input_data, {})
        expected_message = UserMessage(content=[UserMessageText(text="Hello, World")])
        io_unit.request_write.assert_called_once_with(BusEvent("process1", 0, message=InputRequest(messages=[expected_message], output_format={})))

    def test_process_request_with_system_prompt(self, io_unit):
        prompts = [SystemCPUMessage(type="system", prompt="System update complete.")]
        io_unit.request_write = MagicMock()
        io_unit.process_request("process2", prompts, {}, {})
        expected_message = SystemMessage(content="System update complete.")
        io_unit.request_write.assert_called_once_with(BusEvent("process2", 0, message=InputRequest(messages=[expected_message], output_format={})))

    def test_process_request_with_image_url_prompt(self, io_unit):
        prompts = [ImageURLCPUMessage(type="image_url", prompt="https://example.com/image.jpg")]
        io_unit.request_write = MagicMock()
        io_unit.process_request("process3", prompts, {}, {})
        expected_message = UserMessage(content=[UserMessageImageURL(image_url="https://example.com/image.jpg")])
        io_unit.request_write.assert_called_once_with(BusEvent("process3", 0, message=InputRequest(messages=[expected_message], output_format={})))

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
        io_unit.request_write.assert_called_once_with(BusEvent("process4", 0, message=InputRequest(messages=expected_messages, output_format={})))

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
        io_unit.request_write.assert_called_once_with(BusEvent("process6", 0, message=InputRequest(messages=[expected_message], output_format={})))

    def test_process_request_with_missing_template_data(self, io_unit):
        prompts = [UserTextCPUMessage(type="user", prompt="Hello, {{ name }}")]
        with pytest.raises(UndefinedError):
            io_unit.process_request("process7", prompts, {}, {})

    def test_process_request_validation_error(self, io_unit):
        with pytest.raises(ValidationError):
            io_unit.process_request("process8", [{}], {}, {})  # Empty prompt should raise validation error
