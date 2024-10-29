from __future__ import annotations

import base64
import json
import logging
from typing import List, Optional, Union, Literal, Dict, Any, AsyncIterator, cast

import yaml
from openai import AsyncStream
from openai.types.chat import ChatCompletionToolParam, ChatCompletionChunk, ChatCompletion, ChatCompletionMessage
from pydantic import Field

from eidolon_ai_client.events import (
    StringOutputEvent,
    ObjectOutputEvent,
    LLMToolCallRequestEvent,
    ToolCall,
)
from eidolon_ai_client.util.logger import logger as eidolon_logger
from eidolon_ai_sdk.apu.llm.open_ai_connection_handler import OpenAIConnectionHandler, OpenAIConnectionHandlerSpec
from eidolon_ai_sdk.apu.llm_message import (
    LLMMessage,
    AssistantMessage,
    ToolResponseMessage,
    UserMessage,
    SystemMessage,
    UserMessageText,
    UserMessageImage,
)
from eidolon_ai_sdk.apu.llm_unit import LLMUnit, LLMCallFunction, LLMModel, LLMUnitSpec
from eidolon_ai_sdk.system.reference_model import AnnotatedReference, Reference
from eidolon_ai_sdk.system.specable import Specable
from eidolon_ai_sdk.util.image_utils import scale_image

logger = eidolon_logger.getChild("llm_unit")


async def convert_to_openai(message: LLMMessage):
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
                    data = await part.getBytes()
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


gpt_4 = "gpt-4-turbo"


class OpenAILLMBaseSpec(LLMUnitSpec):
    model: AnnotatedReference[LLMModel, gpt_4]
    temperature: float = 0.3
    force_json: bool = True
    max_tokens: Optional[int] = None
    supports_system_messages: bool = True
    can_stream: bool = True


class OpenAILLMBase(LLMUnit, Specable[OpenAILLMBaseSpec]):
    temperature: float
    connection_handler: OpenAIConnectionHandler

    def __init__(self, connection_handler: OpenAIConnectionHandler, **kwargs):
        LLMUnit.__init__(self, **kwargs)
        Specable.__init__(self, **kwargs)
        self.temperature = self.spec.temperature
        self.connection_handler = connection_handler

    async def execute_llm(
            self,
            messages: List[LLMMessage],
            tools: List[LLMCallFunction],
            output_format: Union[Literal["str"], Dict[str, Any]],
    ) -> AsyncIterator[AssistantMessage]:
        is_string, request = await self._build_request(messages, tools, output_format)

        logger.info("executing open ai llm request", extra=request)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("request content:\n" + yaml.dump(request))

        complete_message = ""
        tools_to_call = []
        raw_completion = cast(AsyncStream[ChatCompletionChunk], await self.connection_handler.completion(**request))
        completion = raw_completion
        if isinstance(completion, ChatCompletion):
            async def _fn():
                yield raw_completion

            completion = _fn()
        async for m_chunk in completion:
            chunk = cast(ChatCompletionChunk | ChatCompletionMessage, m_chunk)
            if not chunk.choices:
                logger.info("open ai llm chunk has no choices, skipping")
                continue
            message = chunk.choices[0].delta if hasattr(chunk.choices[0], "delta") else chunk.choices[0].message

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
                if is_string:
                    logger.debug(f"open ai llm stream response: {message.content}", extra=dict(content=message.content))
                    yield StringOutputEvent(content=message.content)
                else:
                    complete_message += message.content

        logger.info(f"open ai llm tool calls: {json.dumps(tools_to_call)}", extra=dict(tool_calls=tools_to_call))
        if len(tools_to_call) > 0:
            for tool in tools_to_call:
                tool_call = self._convert_tool_call(tool)
                yield LLMToolCallRequestEvent(tool_call=tool_call)
        if not is_string:
            logger.debug(f"open ai llm object response: {complete_message}", extra=dict(content=complete_message))
            if not self.spec.force_json:
                # message format looks like json```{...}```, parse content and pull out the json
                complete_message = complete_message[complete_message.find("{"): complete_message.rfind("}") + 1]

            if complete_message:
                yield ObjectOutputEvent(content=json.loads(complete_message))
            elif len(tools_to_call) == 0:
                yield ObjectOutputEvent(content={})

    async def _build_request(self, inMessages, inTools, output_format):
        tools = await self._build_tools(inTools)

        # This is all for tests so that we can ensure deterministic behavior
        messages = []
        grouped_tool_responses = []
        for message in inMessages:
            if isinstance(message, ToolResponseMessage):
                grouped_tool_responses.append(message)
            else:
                if grouped_tool_responses:
                    # dlb - order tool_call_events by tool_call_id to ensure deterministic behavior for tests
                    grouped_tool_responses.sort(key=lambda e: e.tool_call_id)
                    for tool_response in grouped_tool_responses:
                        messages.append(tool_response)
                    grouped_tool_responses = []
                messages.append(message)
        if grouped_tool_responses:
            # dlb - order tool_call_events by tool_call_id to ensure deterministic behavior for tests
            grouped_tool_responses.sort(key=lambda e: e.tool_call_id)
            for tool_response in grouped_tool_responses:
                messages.append(tool_response)

        messages = [await convert_to_openai(message) for message in messages]
        request = {
            "messages": messages,
            "model": self.model.name,
            "temperature": self.temperature,
            "stream": self.spec.can_stream,
        }
        if output_format == "str" or output_format.get("type") == "string":
            is_string = True
        else:
            is_string = False
            force_json_msg = (
                f"Your response MUST be valid JSON satisfying the following JSON schema:\n{json.dumps(output_format)}"
            )
            if not self.spec.force_json:
                force_json_msg += "\nThe response will be wrapped in a json section json```{...}```\nRemember to use double quotes for strings and properties."
            else:
                request["response_format"] = dict(type="json_object")

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

        if not self.spec.supports_system_messages:
            if len(messages) >= 2 and messages[0].get("role") == "system" and messages[1].get('role') == "user":
                system_message = messages.pop(0)
                text_content = [c for c in messages[0]["content"] if c['type'] == "text"][0]
                text_to_add = f"For the rest of the conversation, follow the following instructions:\n<INSTRUCTIONS>\n{system_message['content']}\n</INSTRUCTIONS>"
                text_content['text'] = f"{text_to_add}\n\n{text_content['text']}"
            else:
                raise RuntimeError("System messages are not supported by this model, but unable to transform messages")

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

    @staticmethod
    def _convert_tool_call(tool: Dict[str, any]) -> ToolCall:
        name = tool["name"]
        try:
            loads = json.loads(tool["arguments"])
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Error decoding response function arguments for tool {name}") from e
        return ToolCall(tool_call_id=tool["id"], name=name, arguments=loads)


class OpenAiGPTSpec(OpenAILLMBaseSpec):
    client_args: dict = {}
    connection_handler: Optional[Reference[OpenAIConnectionHandler]] = Field(None, deprecated=True)


class OpenAIGPT(OpenAILLMBase, Specable[OpenAiGPTSpec]):
    def __init__(self, **kwargs):
        Specable.__init__(self, **kwargs)
        if self.spec.connection_handler:
            logger.warning(
                "\"connection_handler\" is deprecated and will be removed. Use client_args if customizing an openai connection or AzureLLMUnit if connecting to Azure.")
            connection_handler = self.spec.connection_handler.instantiate()
        else:
            connection_handler = OpenAIConnectionHandler(spec=OpenAIConnectionHandlerSpec(**self.spec.client_args))
        super().__init__(connection_handler=connection_handler, ** kwargs)
