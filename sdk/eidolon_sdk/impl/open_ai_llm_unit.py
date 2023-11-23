import json
import logging
from typing import List

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionToolParam, ChatCompletionMessageToolCall
from openai.types.chat.completion_create_params import ResponseFormat

from eidolon_sdk.cpu.call_context import CallContext
from eidolon_sdk.cpu.llm_message import LLMMessage, AssistantMessage, ToolCall, ToolResponseMessage, UserMessage, \
    SystemMessage
from eidolon_sdk.cpu.llm_unit import LLMUnit, LLMUnitConfig, LLMCallFunction
from eidolon_sdk.reference_model import Specable


def convert_to_openai(message: LLMMessage):
    if isinstance(message, SystemMessage):
        return {
            "role": "system",
            "content": message.content
        }
    elif isinstance(message, UserMessage):
        content = message.content
        if not isinstance(content, str):
            content = [part.model_dump() for part in content]
        return {
            "role": "user",
            "content": content
        }
    elif isinstance(message, AssistantMessage):
        ret = {
            "role": "assistant",
            "content": str(message.content)
        }
        if message.tool_calls and len(message.tool_calls) > 0:
            ret["tool_calls"] = [{
                "id": tool_call.tool_call_id,
                "type": "function",
                "function": {
                    "name": tool_call.name,
                    "arguments": str(tool_call.arguments)
                }
            } for tool_call in message.tool_calls]
        return ret
    elif isinstance(message, ToolResponseMessage):
        # tool_call_id, content
        return {
            "role": "tool",
            "tool_call_id": message.tool_call_id,
            "content": message.result
        }
    else:
        raise ValueError(f"Unknown message type {message.type}")


class OpenAiGPTSpec(LLMUnitConfig):
    model: str = "gpt-4-1106-preview"
    temperature: float = 0.3


class OpenAIGPT(LLMUnit, Specable[OpenAiGPTSpec]):
    model: str
    temperature: float
    llm: AsyncOpenAI = None

    def __init__(self, spec: OpenAiGPTSpec, **kwargs):
        super().__init__(spec, **kwargs)
        self.model = spec.model
        self.temperature = spec.temperature

    async def execute_llm(self, call_context: CallContext, inMessages: List[LLMMessage], inTools: List[LLMCallFunction], output_format: dict) -> AssistantMessage:
        if not self.llm:
            self.llm = AsyncOpenAI()
        messages = [convert_to_openai(message) for message in inMessages]

        # add response rules to original system message for this call only
        if messages[0]['role'] == 'system':
            messages[0]['content'] += f"\n\nYour response MUST be valid JSON satisfying the following schema:\n{json.dumps(output_format)}"
        else:
            messages.insert(0, {
                "role": "system",
                "content": f"Your response MUST be valid JSON satisfying the following schema:\n{json.dumps(output_format)}"
            })

        logging.info(messages)
        tools = []
        for tool in inTools:
            tools.append(ChatCompletionToolParam(**{
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }))
        # This event is a request to query the LLM
        request = {
            "messages": messages,
            "model": self.model,
            "temperature": self.temperature,
            "response_format": ResponseFormat(type="json_object")
        }
        if len(tools) > 0:
            request["tools"] = tools

        logging.info("executing open ai llm request", extra=request)
        try:
            llm_response = await self.llm.chat.completions.create(**request)
        except Exception:
            logging.exception("error calling open ai llm")
            raise
        message = llm_response.choices[0].message

        logging.info(f"open ai llm response", extra=dict(content=message.content, tool_calls=message.tool_calls))

        tool_response = [_convert_tool_call(tool) for tool in message.tool_calls or []]
        try:
            content = json.loads(message.content) if message.content else {}
        except json.JSONDecodeError as e:
            raise RuntimeError("Error decoding response content") from e
        return AssistantMessage(content=content, tool_calls=tool_response)


def _convert_tool_call(tool: ChatCompletionMessageToolCall) -> ToolCall:
    try:
        loads = json.loads(tool.function.arguments)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Error decoding response function arguments for tool {tool.function.name}") from e
    return ToolCall(tool_call_id=tool.id, name=tool.function.name, arguments=loads)
