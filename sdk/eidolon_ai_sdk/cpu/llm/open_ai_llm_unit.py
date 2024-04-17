import base64
import json
import logging
from typing import List, Optional, Union, Literal, Dict, Any, AsyncIterator, cast

import yaml
from openai import AsyncStream
from openai.types.chat import ChatCompletionToolParam, ChatCompletionChunk
from openai.types.chat.completion_create_params import ResponseFormat

from eidolon_ai_client.events import (
    StringOutputEvent,
    ObjectOutputEvent,
    LLMToolCallRequestEvent,
    ToolCall,
)
from eidolon_ai_client.util.logger import logger as eidolon_logger
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.llm.open_ai_connection_handler import OpenAIConnectionHandler
from eidolon_ai_sdk.cpu.llm_message import (
    LLMMessage,
    AssistantMessage,
    ToolResponseMessage,
    UserMessage,
    SystemMessage,
    UserMessageText,
    UserMessageImage,
)
from eidolon_ai_sdk.cpu.llm_unit import LLMUnit, LLMCallFunction, LLMModel, LLMUnitSpec
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference
from eidolon_ai_sdk.util.image_utils import scale_image

logger = eidolon_logger.getChild("llm_unit")


async def convert_to_openai(message: LLMMessage, process_id: str):
    if isinstance(message, SystemMessage):
        return {"role": "system", "content": message.content}
    elif isinstance(message, UserMessage):
        content = message.content
        if not isinstance(content, str):
            content = []
            for part in message.content:
                if isinstance(part, UserMessageText):
                    content.append({"type": "text", "text": part.text})
                elif isinstance(part, UserMessageImage):
                    data = await part.getBytes(process_id=process_id)
                    # scale the image such that the max size of the shortest size is at most 768px
                    data = scale_image(data)
                    # base64 encode the data
                    base64_image = base64.b64encode(data).decode("utf-8")
                    content.append(
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        }
                    )
                else:
                    raise ValueError(f"Unknown user message part type {part.type}")

        return {"role": "user", "content": content}
    elif isinstance(message, AssistantMessage):
        ret = {"role": "assistant", "content": str(message.content)}
        if message.tool_calls and len(message.tool_calls) > 0:
            ret["tool_calls"] = [
                {
                    "id": tool_call.tool_call_id,
                    "type": "function",
                    "function": {
                        "name": tool_call.name,
                        "arguments": str(tool_call.arguments),
                    },
                }
                for tool_call in message.tool_calls
            ]
        return ret
    elif isinstance(message, ToolResponseMessage):
        # tool_call_id, content
        return {
            "role": "tool",
            "tool_call_id": message.tool_call_id,
            "content": json.dumps(message.result),
        }
    else:
        raise ValueError(f"Unknown message type {message.type}")


gpt_4 = "gpt-4-turbo-preview"


class OpenAiGPTSpec(LLMUnitSpec):
    model: AnnotatedReference[LLMModel, gpt_4]
    temperature: float = 0.3
    force_json: bool = True
    max_tokens: Optional[int] = None
    connection_handler: AnnotatedReference[OpenAIConnectionHandler]


class OpenAIGPT(LLMUnit, Specable[OpenAiGPTSpec]):
    temperature: float
    connection_handler: OpenAIConnectionHandler

    def __init__(self, **kwargs):
        LLMUnit.__init__(self, **kwargs)
        Specable.__init__(self, **kwargs)
        self.temperature = self.spec.temperature
        self.connection_handler = self.spec.connection_handler.instantiate()

    async def execute_llm(
        self,
        call_context: CallContext,
        messages: List[LLMMessage],
        tools: List[LLMCallFunction],
        output_format: Union[Literal["str"], Dict[str, Any]],
    ) -> AsyncIterator[AssistantMessage]:
        can_stream_message, request = await self._build_request(call_context, messages, tools, output_format)
        request["stream"] = True

        logger.info("executing open ai llm request", extra=request)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("request content:\n" + yaml.dump(request))

        complete_message = ""
        tools_to_call = []
        completion = cast(AsyncStream[ChatCompletionChunk], await self.connection_handler.completion(**request))
        async for m_chunk in completion:
            chunk = cast(ChatCompletionChunk, m_chunk)
            if not chunk.choices:
                logger.info("open ai llm chunk has no choices, skipping")
                continue
            message = chunk.choices[0].delta

            logger.debug(
                f"open ai llm response\ntool calls: {len(message.tool_calls or [])}\ncontent:\n{message.content}",
                extra=dict(content=message.content, tool_calls=message.tool_calls),
            )

            for tool_call in message.tool_calls or []:
                index = tool_call.index
                if index == len(tools_to_call):
                    tools_to_call.append({"id": "", "name": "", "arguments": ""})
                if tool_call.id:
                    tools_to_call[index]["id"] = tool_call.id
                if tool_call.function:
                    if tool_call.function.name:
                        tools_to_call[index]["name"] = tool_call.function.name
                    if tool_call.function.arguments:
                        tools_to_call[index]["arguments"] += tool_call.function.arguments

            if message.content:
                if can_stream_message:
                    logger.debug(f"open ai llm stream response: {message.content}", extra=dict(content=message.content))
                    yield StringOutputEvent(content=message.content)
                else:
                    complete_message += message.content

        logger.info(f"open ai llm tool calls: {json.dumps(tools_to_call)}", extra=dict(tool_calls=tools_to_call))
        if len(tools_to_call) > 0:
            for tool in tools_to_call:
                tool_call = _convert_tool_call(tool)
                yield LLMToolCallRequestEvent(tool_call=tool_call)
        if not can_stream_message:
            logger.debug(f"open ai llm object response: {complete_message}", extra=dict(content=complete_message))
            if not self.spec.force_json:
                # message format looks like json```{...}```, parse content and pull out the json
                complete_message = complete_message[complete_message.find("{") : complete_message.rfind("}") + 1]

            content = json.loads(complete_message) if complete_message else {}
            yield ObjectOutputEvent(content=content)

    async def _build_request(self, call_context: CallContext, inMessages, inTools, output_format):
        tools = await self._build_tools(inTools)
        messages = [await convert_to_openai(message, call_context.process_id) for message in inMessages]
        request = {
            "messages": messages,
            "model": self.model.name,
            "temperature": self.temperature,
        }
        if output_format == "str" or output_format["type"] == "string":
            is_string = True
        else:
            is_string = False
            force_json_msg = (
                f"Your response MUST be valid JSON satisfying the following JSON schema:\n{json.dumps(output_format)}"
            )
            if not self.spec.force_json:
                force_json_msg += "\nThe response will be wrapped in a json section json```{...}```\nRemember to use double quotes for strings and properties."
            else:
                request["response_format"] = ResponseFormat(type="json_object")

            # add response rules to original system message for this call only
            if messages[0]["role"] == "system":
                messages[0]["content"] += f"\n\n{force_json_msg}"
            else:
                messages.insert(0, {"role": "system", "content": force_json_msg})
        logger.debug(messages)
        if len(tools) > 0:
            request["tools"] = tools
        if self.spec.max_tokens:
            request["max_tokens"] = self.spec.max_tokens
        return is_string, request

    async def _build_tools(self, inTools):
        tools = []
        for tool in inTools:
            tools.append(
                ChatCompletionToolParam(
                    **{
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": tool.parameters,
                        },
                    }
                )
            )
        return tools


def _convert_tool_call(tool: Dict[str, any]) -> ToolCall:
    name = tool["name"]
    try:
        loads = json.loads(tool["arguments"])
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Error decoding response function arguments for tool {name}") from e
    return ToolCall(tool_call_id=tool["id"], name=name, arguments=loads)
