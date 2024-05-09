from typing import List, AsyncIterator

from eidolon_ai_client.events import ObjectOutputEvent, ToolCall, StreamEvent, LLMToolCallRequestEvent, UserInputEvent, StringOutputEvent
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.llm_message import UserMessage, UserMessageText, LLMMessage
from eidolon_ai_sdk.cpu.llm_unit import LLMCallFunction
from eidolon_ai_sdk.cpu.tool_call_unit import ToolCallUnit, ToolCallUnitSpec, ToolCallResponse


def test_add_tools_adds_correct_message():
    unit = ToolCallUnit(spec=ToolCallUnitSpec(tool_message_prompt="here"), processing_unit_locator=None)
    message = UserMessage(content=[])
    tools = [
        LLMCallFunction(name="foo", description="bar", parameters={"a": "b"}),
        LLMCallFunction(name="foo2", description="bar2", parameters={"a2": "b2"}),
    ]
    unit.add_tools([message], tools)
    assert message == UserMessage(type='user', content=[
        UserMessageText(
            type='text',
            text="""You have access to the following tools:
{"tool_call_id": "foo", "name": "foo", "description": "bar", "parameters": {"a": "b"}}
{"tool_call_id": "foo2", "name": "foo2", "description": "bar2", "parameters": {"a2": "b2"}}
here"""
        )
    ])


def test_add_tools_adds_correct_message_to_new_UserMessage():
    unit = ToolCallUnit(spec=ToolCallUnitSpec(tool_message_prompt="here"), processing_unit_locator=None)
    tools = [
        LLMCallFunction(name="foo", description="bar", parameters={"a": "b"}),
        LLMCallFunction(name="foo2", description="bar2", parameters={"a2": "b2"}),
    ]
    messages = []
    unit.add_tools(messages, tools)
    assert len(messages) == 1
    assert messages[0] == UserMessage(type='user', content=[
        UserMessageText(
            type='text',
            text="""You have access to the following tools:
{"tool_call_id": "foo", "name": "foo", "description": "bar", "parameters": {"a": "b"}}
{"tool_call_id": "foo2", "name": "foo2", "description": "bar2", "parameters": {"a2": "b2"}}
here"""
        )
    ])


async def test_wrap_exe_call_converts_output():
    unit = ToolCallUnit(spec=ToolCallUnitSpec(tool_message_prompt="here"), processing_unit_locator=None)
    cc = CallContext(process_id="123")
    mess = [UserMessage(content=[UserMessageText(text="123")])]
    tls = [LLMCallFunction(name="foo", description="bar", parameters={"a": "b"})]
    tool_response = [ToolCall(tool_call_id="1", name="a", arguments={"x": "y"})]

    async def exec_llm_mock(call_context: CallContext, messages: List[LLMMessage], tools: List[LLMCallFunction], output_schema) -> AsyncIterator[StreamEvent]:
        assert call_context is cc
        assert messages is mess
        assert tools is tls
        assert output_schema == ToolCallResponse.model_json_schema()
        yield ObjectOutputEvent(content=ToolCallResponse(tools=tool_response))

    response = [event async for event in unit.wrap_exe_call(exec_llm_mock, cc, mess, tls)]
    assert response == [LLMToolCallRequestEvent(tool_call=tool) for tool in tool_response]


async def test_wrap_exe_call_yields_other_events():
    unit = ToolCallUnit(spec=ToolCallUnitSpec(tool_message_prompt="here"), processing_unit_locator=None)
    cc = CallContext(process_id="123")
    mess = [UserMessage(content=[UserMessageText(text="123")])]
    tls = [LLMCallFunction(name="foo", description="bar", parameters={"a": "b"})]
    tool_response = [ToolCall(tool_call_id="1", name="a", arguments={"x": "y"})]

    async def exec_llm_mock(call_context: CallContext, messages: List[LLMMessage], tools: List[LLMCallFunction], output_schema) -> AsyncIterator[StreamEvent]:
        assert call_context is cc
        assert messages is mess
        assert tools is tls
        assert output_schema == ToolCallResponse.model_json_schema()
        yield UserInputEvent(input="abc")
        yield ObjectOutputEvent(content=ToolCallResponse(tools=tool_response))
        yield UserInputEvent(input="abc")

    response = [event async for event in unit.wrap_exe_call(exec_llm_mock, cc, mess, tls)]
    assert response == [UserInputEvent(input="abc"), LLMToolCallRequestEvent(tool_call=tool_response[0]), UserInputEvent(input="abc")]


async def test_wrap_exe_call_yields_empty_string_event_if_no_tools():
    unit = ToolCallUnit(spec=ToolCallUnitSpec(tool_message_prompt="here"), processing_unit_locator=None)
    cc = CallContext(process_id="123")
    mess = [UserMessage(content=[UserMessageText(text="123")])]
    tls = [LLMCallFunction(name="foo", description="bar", parameters={"a": "b"})]
    tool_response = []

    async def exec_llm_mock(call_context: CallContext, messages: List[LLMMessage], tools: List[LLMCallFunction], output_schema) -> AsyncIterator[StreamEvent]:
        assert call_context is cc
        assert messages is mess
        assert tools is tls
        assert output_schema == ToolCallResponse.model_json_schema()
        yield UserInputEvent(input="abc")
        yield ObjectOutputEvent(content=ToolCallResponse(tools=tool_response))
        yield UserInputEvent(input="abc")

    response = [event async for event in unit.wrap_exe_call(exec_llm_mock, cc, mess, tls)]
    assert response == [UserInputEvent(input="abc"), StringOutputEvent(content=""), UserInputEvent(input="abc")]
