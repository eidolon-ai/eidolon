import json
from typing import List, Union, Literal, Dict, Any, Callable, AsyncIterator, cast

from pydantic import BaseModel

from eidolon_ai_client.events import ToolCall, StreamEvent, ObjectOutputEvent, StringOutputEvent, LLMToolCallRequestEvent
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.llm_message import UserMessage, UserMessageText, LLMMessage
from eidolon_ai_sdk.cpu.llm_unit import LLMCallFunction
from eidolon_ai_sdk.cpu.processing_unit import ProcessingUnit
from eidolon_ai_sdk.system.reference_model import Specable


class ToolCallResponse(BaseModel):
    tools: List[ToolCall]


class ToolCallUnitSpec(BaseModel):
    tool_message_prompt: str = """You must follow these instructions:
Always select one or more of the above tools based on the user query
If a tool is found, you must respond in the JSON format matching the following schema:
{
   "tools": [
   {
        "tool_call_id": "<the id of the selected tool>",
        "name": "<name of the selected tool>",
        "arguments": <arguments for the selected tool, matching the tool's parameter JSON schema
   }
   ]
}
If there are multiple tools required, make sure a list of tools are returned in a JSON array.
If there is no tool that match the user request, you will respond with empty json.
Do not add any additional Notes or Explanations"""


class ToolCallUnit(ProcessingUnit, Specable[ToolCallUnitSpec]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Specable.__init__(self, **kwargs)

    def add_tools(self, messages: List[LLMMessage], tools: List[LLMCallFunction]):
        # find last UserMessage or add one
        userMessage = None
        for message in messages:
            if isinstance(message, UserMessage):
                userMessage = message

        if not userMessage:
            userMessage = UserMessage(content=[])
            messages.append(userMessage)
        tool_schema = []
        for tool in tools:
            tool_schema.append(
                json.dumps({
                    "tool_call_id": tool.name,
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters,
                })
            )

        prompt = "You have access to the following tools:\n" + "\n".join(tool_schema) + "\n" + self.spec.tool_message_prompt
        userMessage.content.insert(0, UserMessageText(text=prompt))

    async def wrap_exe_call(self, exec_llm_call: Callable[[CallContext, List[LLMMessage], List[LLMCallFunction],
                                                           Union[Literal["str"], Dict[str, Any]]], AsyncIterator[StreamEvent]],
                            call_context: CallContext, messages: List[LLMMessage], tools: List[LLMCallFunction]) -> AsyncIterator[StreamEvent]:
        stream: AsyncIterator[StreamEvent] = exec_llm_call(call_context, messages, tools, ToolCallResponse.model_json_schema())
        # stream should be a single object output event
        async for event in stream:
            if isinstance(event, ObjectOutputEvent):
                found_object_event = True
                toolCallResponse = cast(ToolCallResponse, event.content)
                if not toolCallResponse.tools:
                    yield StringOutputEvent(content="")
                else:
                    for tool_call in toolCallResponse.tools:
                        yield LLMToolCallRequestEvent(tool_call=tool_call)

            else:
                yield event
