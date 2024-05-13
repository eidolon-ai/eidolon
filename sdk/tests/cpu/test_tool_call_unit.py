from typing import List, AsyncIterator, Union, Literal, Dict, Any, Callable

import pytest

from eidolon_ai_client.client import Agent
from eidolon_ai_client.events import ObjectOutputEvent, ToolCall, StreamEvent, LLMToolCallRequestEvent, UserInputEvent, StringOutputEvent
from eidolon_ai_sdk.agent.simple_agent import SimpleAgent
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.llm_message import UserMessage, UserMessageText, LLMMessage
from eidolon_ai_sdk.cpu.llm_unit import LLMCallFunction, LLMUnit
from eidolon_ai_sdk.cpu.logic_unit import LogicUnit, llm_function
from eidolon_ai_sdk.cpu.tool_call_unit import ToolCallLLMWrapper, ToolCallResponse
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.resources.resources_base import Metadata, Resource
from eidolon_ai_sdk.util.class_utils import fqn


class TestLLMUnit(LLMUnit):
    fn: Callable

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def execute_llm(self, call_context: CallContext, messages: List[LLMMessage],
                          tools: List[LLMCallFunction], output_format: Union[Literal["str"], Dict[str, Any]]) -> AsyncIterator[StreamEvent]:
        return self.fn(call_context, messages, tools, output_format)


def noop(*args, **kwargs):
    yield ObjectOutputEvent(content=ToolCallResponse(tools=[]))


def make_wrapper(prompt: str, fn):
    spec = {
        "tool_message_prompt": prompt,
        "llm_unit": {
            "implementation": fqn(TestLLMUnit),
            "model": {
                "human_name": "Test LLM Unit",
                "name": "test_llm_unit",
                "input_context_limit": 1024,
                "output_context_limit": 1024,
                "supports_tools": False,
                "supports_image_input": False,
                "supports_audio_input": False,
            },
        }
    }
    llm_spec = Reference[ToolCallLLMWrapper](**spec)
    llm_wrapper = llm_spec.instantiate(processing_unit_locator=None)
    # llm_wrapper = ToolCallLLMWrapper(spec=spec, processing_unit_locator=None)
    llm_wrapper.llm_unit.fn = fn
    return llm_wrapper


class MeaningOfLife(LogicUnit):
    @llm_function()
    async def meaning_of_life_tool(self) -> str:
        """
        call this tool to get the meaning of life
        """
        return "42"


def r(name, **kwargs):
    spec = dict(
        implementation=SimpleAgent.__name__, **kwargs,
        apu=dict(
            implementation="APU",
            logic_units=[fqn(MeaningOfLife)],
            llm_unit=dict(
                implementation=fqn(ToolCallLLMWrapper),
            )
        )
    )
    return Resource(
        apiVersion="eidolon/v1",
        kind="Agent",
        metadata=Metadata(name=name),
        spec=spec,
    )


resources = [
    r("simple", actions=[dict(allow_file_upload=True)]),
]


@pytest.fixture(scope="module", autouse=True)
async def server(run_app):
    async with run_app(*resources) as ra:
        yield ra


def test_add_tools_adds_correct_message(server):
    unit = make_wrapper("here", noop)
    message = UserMessage(content=[])
    tools = [
        LLMCallFunction(name="foo", description="bar", parameters={"a": "b"}),
        LLMCallFunction(name="foo2", description="bar2", parameters={"a2": "b2"}),
    ]
    messages = unit._add_tools([message], tools)
    assert len(messages) == 2
    assert messages[1] == UserMessage(type='user', content=[
        UserMessageText(
            type='text',
            text="""You have access to the following tools:
{"tool_call_id": "foo", "name": "foo", "description": "bar", "parameters": {"a": "b"}}
{"tool_call_id": "foo2", "name": "foo2", "description": "bar2", "parameters": {"a2": "b2"}}
here"""
        )
    ])


def test_add_tools_adds_correct_message_to_new_UserMessage():
    unit = make_wrapper("here", noop)
    tools = [
        LLMCallFunction(name="foo", description="bar", parameters={"a": "b"}),
        LLMCallFunction(name="foo2", description="bar2", parameters={"a2": "b2"}),
    ]
    messages = []
    messages = unit._add_tools(messages, tools)
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
    cc = CallContext(process_id="123")
    mess = [UserMessage(content=[UserMessageText(text="123")])]
    tool_response = [ToolCall(tool_call_id="1", name="a", arguments={"x": "y"})]

    async def exec_llm_mock(call_context: CallContext, messages: List[LLMMessage], tools: List[LLMCallFunction], output_schema):
        assert output_schema == ToolCallResponse.model_json_schema()
        yield ObjectOutputEvent(content=ToolCallResponse(tools=tool_response))

    unit = make_wrapper("here", exec_llm_mock)

    response = [event async for event in unit._wrap_exe_call(exec_llm_mock, cc, mess)]
    assert response == [LLMToolCallRequestEvent(tool_call=tool) for tool in tool_response]


async def test_wrap_exe_call_yields_other_events():
    cc = CallContext(process_id="123")
    mess = [UserMessage(content=[UserMessageText(text="123")])]
    tool_response = [ToolCall(tool_call_id="1", name="a", arguments={"x": "y"})]

    async def exec_llm_mock(call_context: CallContext, messages: List[LLMMessage], tools: List[LLMCallFunction], output_schema) -> AsyncIterator[StreamEvent]:
        assert output_schema == ToolCallResponse.model_json_schema()
        yield UserInputEvent(input="abc")
        yield ObjectOutputEvent(content=ToolCallResponse(tools=tool_response))
        yield UserInputEvent(input="abc")

    unit = make_wrapper("here", exec_llm_mock)

    response = [event async for event in unit._wrap_exe_call(exec_llm_mock, cc, mess)]
    assert response == [UserInputEvent(input="abc"), LLMToolCallRequestEvent(tool_call=tool_response[0]), UserInputEvent(input="abc")]


async def test_wrap_exe_call_yields_empty_string_event_if_no_tools():
    cc = CallContext(process_id="123")
    mess = [UserMessage(content=[UserMessageText(text="123")])]
    tool_response = []

    async def exec_llm_mock(call_context: CallContext, messages: List[LLMMessage], tools: List[LLMCallFunction], output_schema) -> AsyncIterator[StreamEvent]:
        assert output_schema == ToolCallResponse.model_json_schema()
        yield UserInputEvent(input="abc")
        yield ObjectOutputEvent(content=ToolCallResponse(tools=tool_response))
        yield UserInputEvent(input="abc")

    unit = make_wrapper("here", exec_llm_mock)

    response = [event async for event in unit._wrap_exe_call(exec_llm_mock, cc, mess)]
    assert response == [UserInputEvent(input="abc"), StringOutputEvent(content=""), UserInputEvent(input="abc")]


async def test_end_to_end():
    process = await Agent.get("simple").create_process()
    resp = await process.action("converse", body=dict(body="what is the meaning of life?"))
    print(resp)
