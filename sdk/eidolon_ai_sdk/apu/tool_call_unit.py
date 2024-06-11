import json
from typing import List, Union, Literal, Dict, Any, Callable, AsyncIterator, Optional

from pydantic import BaseModel, Field

from eidolon_ai_client.events import ToolCall, StreamEvent, ObjectOutputEvent, StringOutputEvent, \
    LLMToolCallRequestEvent
from eidolon_ai_sdk.apu.call_context import CallContext
from eidolon_ai_sdk.apu.llm_message import UserMessage, UserMessageText, LLMMessage, AssistantMessage
from eidolon_ai_sdk.apu.llm_unit import LLMCallFunction, LLMUnit, LLMModel
from eidolon_ai_sdk.system.reference_model import Specable, Reference, AnnotatedReference


class _DefaultModel(LLMModel):
    human_name: str = "Default"
    name: str = "default"
    input_context_limit: int = 1024
    output_context_limit: int = 1024
    supports_tools: bool = False
    supports_image_input: bool = False
    supports_audio_input: bool = False


class ModelWrapper(LLMModel):
    def __init__(self, base_model: LLMModel):
        super().__init__(**base_model.dict())
        self.supports_tools = True


class ToolCallResponse(BaseModel):
    """
    Response
    """
    tools: Optional[List[ToolCall]] = Field(default=[], description="The tools that are available.")
    notes: str = Field(default="", description="Any notes or explanations.")


class ToolCallLLMWrapperSpec(BaseModel):
    tool_message_prompt: str = """You must follow these instructions:
You can select zero or more of the above tools based on the user query
If there are multiple tools required, make sure a list of tools are returned in a JSON array.
If there is no tool that match the user request or you have already answered the question, you will respond with empty json array for the tools.
You can also add any additional notes or explanations in the notes field."""
    llm_unit: AnnotatedReference[LLMUnit]
    model: Optional[Reference[LLMModel]] = Field(default=None)


class ToolCallLLMWrapper(LLMUnit, Specable[ToolCallLLMWrapperSpec]):
    llm_unit: LLMUnit

    def __init__(self, **kwargs):
        Specable.__init__(self, **kwargs)
        super().__init__(**kwargs)
        self.llm_unit = self.spec.llm_unit.instantiate(
            processing_unit_locator=self.processing_unit_locator, spec=self.spec.llm_unit
        )
        self.model = ModelWrapper(base_model=self.llm_unit.model)

    def execute_llm(
        self,
        call_context: CallContext,
        messages: List[LLMMessage],
        tools: List[LLMCallFunction],
        output_format: Union[Literal["str"], Dict[str, Any]],
    ) -> AsyncIterator[StreamEvent]:
        messages = self._add_tools(messages, tools)
        return self._wrap_exe_call(self.llm_unit.execute_llm, call_context, tools, messages)

    def _add_tools(self, messages: List[LLMMessage], tools: List[LLMCallFunction]):
        if tools and len(tools) > 0:
            tool_schema = []
            for tool in tools:
                tool_schema.append(
                    json.dumps(
                        {
                            "tool_call_id": tool.name,
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": tool.parameters,
                        }
                    )
                )

            prompt = (
                "You have access to the following tools:\n" + "\n".join(tool_schema) + "\n" + self.spec.tool_message_prompt
            )
            messages = messages + [UserMessage(content=[UserMessageText(text=prompt)])]

        return messages

    async def _wrap_exe_call(
        self,
        exec_llm_call: Callable[
            [CallContext, List[LLMMessage], List[LLMCallFunction], Union[Literal["str"], Dict[str, Any]]],
            AsyncIterator[StreamEvent],
        ],
        call_context: CallContext,
        tools: List[LLMCallFunction],
        messages: List[LLMMessage],
    ) -> AsyncIterator[StreamEvent]:
        ret_type = ToolCallResponse.model_json_schema() if tools else dict(type="string")
        stream: AsyncIterator[StreamEvent] = exec_llm_call(
            call_context, messages, [], ret_type
        )
        # stream should be a single object output event
        async for event in stream:
            if isinstance(event, ObjectOutputEvent):
                toolCallResponse = ToolCallResponse.model_validate(event.content)
                if toolCallResponse.tools:
                    for tool_call in toolCallResponse.tools:
                        yield LLMToolCallRequestEvent(tool_call=tool_call)
                    if toolCallResponse.notes:
                        yield StringOutputEvent(content=toolCallResponse.notes)
                else:
                    yield StringOutputEvent(content=toolCallResponse.notes)
            else:
                yield event

    def create_assistant_message(self, call_context: CallContext, content: str, tool_call_events) -> LLMMessage:
        if tool_call_events and len(tool_call_events) > 0:
            content += "\nCall the following tools\n"
            for tool_call in tool_call_events:
                content += f"\n{tool_call.tool_call.model_dump_json()}"
        return AssistantMessage(
            type="assistant",
            content=content,
            tool_calls=[],
        )

    def create_tool_response_message(self, logic_unit_name: str, tc: ToolCall, content: str) -> LLMMessage:
        return UserMessage(content=[UserMessageText(text=f"Tool {tc.model_dump_json()} completed with value {content}")])
