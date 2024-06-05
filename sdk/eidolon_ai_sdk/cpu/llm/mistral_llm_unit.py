import json
import logging
from io import BytesIO
from typing import List, Optional, Union, Literal, Dict, Any, AsyncIterator, cast

import yaml
from PIL import Image
from fastapi import HTTPException
from mistralai.async_client import MistralAsyncClient
from mistralai.exceptions import MistralConnectionException, MistralAPIStatusException, MistralAPIException
from mistralai.models.chat_completion import ChatCompletionStreamResponse, ResponseFormat, ResponseFormats, Function

from eidolon_ai_client.events import (
    StringOutputEvent,
    ObjectOutputEvent,
    LLMToolCallRequestEvent,
    ToolCall,
)
from eidolon_ai_client.util.logger import logger as eidolon_logger
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.llm_message import (
    LLMMessage,
    AssistantMessage,
    ToolResponseMessage,
    UserMessage,
    SystemMessage,
)
from eidolon_ai_sdk.cpu.llm_unit import LLMUnit, LLMCallFunction, LLMModel, LLMUnitSpec
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference
from eidolon_ai_sdk.util.replay import replayable

logger = eidolon_logger.getChild("llm_unit")


def scale_dimensions(width, height, max_size=2048, min_size=768):
    # Check if the dimensions are less than or equal to max_size.
    # If so, adjust the dimensions according to the max_size.
    if width > max_size or height > max_size:
        # Calculate the scaling ratio
        scale_ratio = max_size / max(width, height)

        # Calculate the new dimensions while keeping aspect ratio
        width = int(width * scale_ratio)
        height = int(height * scale_ratio)

    # Check if the minimum dimension is still greater than the min_size.
    # If so, adjust the dimensions according to the min_size.
    if min(width, height) > min_size:
        # Calculate the scaling ratio
        scale_ratio = min_size / min(width, height)

        # Calculate the new dimensions
        width = int(width * scale_ratio)
        height = int(height * scale_ratio)

    return width, height


def scale_image(image_bytes):
    # Load the image from bytes
    image = Image.open(BytesIO(image_bytes))

    # Get the dimensions of the image
    width, height = image.size

    logger.info(f"Original image size: {width}x{height}")
    new_width, new_height = scale_dimensions(width, height)
    logger.info(f"New image size: {new_width}x{new_height}")

    # Resize and return the image
    scaled_image = image.resize((new_width, new_height))
    output = BytesIO()
    scaled_image.save(output, format="PNG")
    return output.getvalue()


async def convert_to_mistral(message: LLMMessage):
    if isinstance(message, SystemMessage):
        return {"role": "system", "content": message.content}
    elif isinstance(message, UserMessage):
        content = message.content
        if not isinstance(content, str):
            content = ""
            for part in message.content:
                if part.type == "text":
                    content += part.text
                else:
                    # not supported
                    pass

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


mistral_large = "mistral-large-latest"


class MistralGPTSpec(LLMUnitSpec):
    model: AnnotatedReference[LLMModel, mistral_large]
    temperature: float = 0.3
    force_json: bool = True
    max_tokens: Optional[int] = None
    client_args: dict = {}


class MistralGPT(LLMUnit, Specable[MistralGPTSpec]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        LLMUnit.__init__(self, **kwargs)
        Specable.__init__(self, **kwargs)

    async def execute_llm(
        self,
        call_context: CallContext,
        messages: List[LLMMessage],
        tools: List[LLMCallFunction],
        output_format: Union[Literal["str"], Dict[str, Any]],
    ) -> AsyncIterator[AssistantMessage]:
        can_stream_message, request = await self._build_request(messages, tools, output_format)

        logger.info("executing mistral llm request", extra=request)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("request content:\n" + yaml.dump(request))
        llm_request = replayable(fn=_mistral_client(), name_override="mistral_completion", parser=_raw_parser)
        complete_message = ""
        tools_to_call = []
        try:
            async for m_chunk in llm_request(client_args=self.spec.client_args, **request):
                chunk = cast(ChatCompletionStreamResponse, m_chunk)
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
                        logger.debug(
                            f"open ai llm stream response: {message.content}", extra=dict(content=message.content)
                        )
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
        except MistralConnectionException as e:
            raise HTTPException(429, f"Mistral Connection Error: {e.message}") from e
        except MistralAPIStatusException as e:
            raise HTTPException(502, f"Mistral Status Error: {e.message}") from e
        except MistralAPIException as e:
            raise HTTPException(502, f"Mistral Error: {e.message}") from e

    async def _build_request(self, inMessages, inTools, output_format):
        tools = await self._build_tools(inTools)
        messages = [await convert_to_mistral(message) for message in inMessages]
        request = {
            "messages": messages,
            "model": str(self.model.name),
            "temperature": self.spec.temperature,
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
                request["response_format"] = ResponseFormat(type=ResponseFormats.json_object)

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
                {
                    "type": "function",
                    "function": Function(
                        **{
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": tool.parameters,
                        }
                    ).model_dump(),
                }
            )
        return tools


def _convert_tool_call(tool: Dict[str, any]) -> ToolCall:
    name = tool["name"]
    try:
        loads = json.loads(tool["arguments"])
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Error decoding response function arguments for tool {name}") from e
    return ToolCall(tool_call_id=tool["id"], name=name, arguments=loads)


def _mistral_client():
    async def fn(client_args: dict = None, **kwargs):
        client: MistralAsyncClient = MistralAsyncClient(**client_args)
        async for e in client.chat_stream(**kwargs):
            yield e

    return fn


async def _raw_parser(resp):
    """
    Parses responses from mistral and yield strings to accumulate to a human-readable message.

    Makes assumptions around tool calls. These are currently true, but may change as mistral mutates their API
    1. Tool call functions names are always in a complete message
    2. Tool calls are ordered (No chunk for tool #2 until #1 is complete)
    """
    calling_tools = False
    prefix = ""
    async for m_chunk in resp:
        chunk = cast(ChatCompletionStreamResponse, m_chunk)
        if not chunk.choices:
            continue
        message = chunk.choices[0].delta

        if message.tool_calls:
            calling_tools = True
            for i, tool_call in enumerate(message.tool_calls):
                if tool_call.function.name:
                    yield prefix + f"Tool Call: {tool_call.function.name}\nArguments: "
                    prefix = "\n"
                if tool_call.function.arguments:
                    yield tool_call.function.arguments
        elif calling_tools:
            yield "\n"
        if message.content:
            yield message.content
            prefix = "\n"
