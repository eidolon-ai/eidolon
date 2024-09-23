import json
from typing import List, Union, Literal, Dict, Any, Callable, AsyncIterator, Optional

from pydantic import BaseModel, Field

from eidolon_ai_client.events import ToolCall, StreamEvent, ObjectOutputEvent, StringOutputEvent, \
    LLMToolCallRequestEvent
from eidolon_ai_sdk.apu.llm_message import UserMessage, UserMessageText, LLMMessage, AssistantMessage, \
    ToolResponseMessage
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
        super().__init__(**base_model.model_dump())
        self.supports_tools = True


class ToolCallResponse(BaseModel):
    """
    Response
    """

    tools: List[ToolCall] = Field(default=[], description="The tools that are available.")
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
        messages: List[LLMMessage],
        tools: List[LLMCallFunction],
        output_format: Union[Literal["str"], Dict[str, Any]],
    ) -> AsyncIterator[StreamEvent]:
        transformed_messages = self._add_tools(messages, tools)
        return self._wrap_exe_call(self.llm_unit.execute_llm, tools, transformed_messages, output_format)

    def _add_tools(self, messages: List[LLMMessage], tools: List[LLMCallFunction]):
        tool_group: List[ToolResponseMessage] = []
        acc = []
        for message in messages:
            if isinstance(message, AssistantMessage):
                message = self._transform_assistant_message(message)

            if isinstance(message, ToolResponseMessage):
                tool_group.append(message)
            else:
                if tool_group:
                    acc.append(self._transform_tool_response_messages(tool_group))
                tool_group = []
                acc.append(message)
        if tool_group:
            acc.append(self._transform_tool_response_messages(tool_group))

        if tools and len(tools) > 0:
            tool_schema = []
            for tool in sorted(tools, key=lambda x: x.name):
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
                "You have access to the following tools:\n"
                + "\n".join(tool_schema)
                + "\n"
                + self.spec.tool_message_prompt
            )
            acc.append(UserMessage(content=[UserMessageText(text=prompt)]))
        return acc

    async def _wrap_exe_call(
        self,
        exec_llm_call: Callable[
            [List[LLMMessage], List[LLMCallFunction], Union[Literal["str"], Dict[str, Any]]],
            AsyncIterator[StreamEvent],
        ],
        tools: List[LLMCallFunction],
        messages: List[LLMMessage],
        output_format: Union[Literal["str"], Dict[str, Any]] = "str",
    ) -> AsyncIterator[StreamEvent]:
        output_is_string = output_format == "str" or output_format.get('type') == "string"
        if tools:
            ret_type = dict(anyOf=[
                ToolCallResponse.model_json_schema(),
                dict(
                    type="object",
                    properties=dict(response=dict(type="string") if output_format == "str" else output_format),
                    required=["response"],
                )
            ])
        else:
            ret_type = output_format
        stream: AsyncIterator[StreamEvent] = exec_llm_call(messages, [], ret_type)
        # stream should be a single object output event
        async for event in stream:
            if tools and event.is_root_and_type(ObjectOutputEvent):
                if event.content.get("response"):
                    if output_is_string:
                        yield StringOutputEvent(content=str(event.content["response"]), metdata=event.metadata)
                    else:
                        yield ObjectOutputEvent(content=event.content["response"], metdata=event.metadata)
                else:
                    tool_call_response = ToolCallResponse.model_validate(event.content)
                    if (tool_call_response.notes or not tool_call_response.tools) and output_is_string:
                        yield StringOutputEvent(content=tool_call_response.notes)
                    for tool_call in tool_call_response.tools:
                        yield LLMToolCallRequestEvent(tool_call=tool_call)
            else:
                yield event

    def _transform_assistant_message(self, message: AssistantMessage) -> LLMMessage:
        content = str(message.content)
        if message.tool_calls:
            content += "\nCall the following tools\n"
            for tool_call in sorted(message.tool_calls, key=lambda x: x.tool_call_id):
                content += f"\n{tool_call.model_dump_json()}"
        return AssistantMessage(
            type="assistant",
            content=content,
            tool_calls=[],
        )

    def _transform_tool_response_messages(self, responses: List[ToolResponseMessage]) -> LLMMessage:
        content = []
        for response in sorted(responses, key=lambda x: x.tool_call_id):
            content.append(f"Tool {response.tool_call_id} completed with value: {response.result}")
        return UserMessage(content=[UserMessageText(text="\n\n".join(content))])
