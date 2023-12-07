import pytest
from eidos.cpu.agent_io import IOUnit, UserTextCPUMessage, SystemCPUMessage, ImageCPUMessage, CPUMessage
from eidos.cpu.call_context import CallContext


# noinspection PyTypeChecker
@pytest.fixture
async def io_unit() -> IOUnit:
    return IOUnit(None)


@pytest.mark.asyncio
async def test_process_request_with_user_text_message(io_unit: IOUnit):
    prompts = [UserTextCPUMessage(prompt="Hello", is_boot_prompt=True)]
    boot_event_prompts, conv_message = await io_unit.process_request(prompts)
    assert len(boot_event_prompts) == 1
    assert conv_message == []


@pytest.mark.asyncio
async def test_process_request_with_system_message(io_unit: IOUnit):
    prompts = [SystemCPUMessage(prompt="System boot", is_boot_prompt=True)]
    boot_event_prompts, conv_message = await io_unit.process_request(prompts)
    assert len(boot_event_prompts) == 1
    assert conv_message == []


@pytest.mark.asyncio
async def test_process_request_with_image_url_message(io_unit: IOUnit):
    prompts = [ImageCPUMessage(prompt="http://example.com/image.jpg", is_boot_prompt=True)]
    boot_event_prompts, conv_message = await io_unit.process_request(prompts)
    assert len(boot_event_prompts) == 1
    assert conv_message == []


@pytest.mark.asyncio
async def test_process_request_with_multiple_messages(io_unit: IOUnit):
    prompts = [
        UserTextCPUMessage(prompt="Hello", is_boot_prompt=True),
        SystemCPUMessage(prompt="System boot", is_boot_prompt=True),
        ImageCPUMessage(prompt="http://example.com/image.jpg", is_boot_prompt=True)
    ]
    boot_event_prompts, conv_message = await io_unit.process_request(prompts)
    assert len(boot_event_prompts) == 3
    assert conv_message == []


@pytest.mark.asyncio
async def test_process_request_with_unknown_message_type(io_unit: IOUnit):
    with pytest.raises(ValueError):
        prompts = [CPUMessage(prompt="Unknown", type="unknown")]
        await io_unit.process_request(prompts)


@pytest.mark.asyncio
async def test_process_response(io_unit: IOUnit):
    call_context = CallContext()
    response = {"message": "Hello"}
    result = await io_unit.process_response(call_context, response)
    assert result == response
