import base64
import json
import logging
from io import BytesIO
from typing import List, Optional, Union, Literal, Dict, Any, AsyncIterator

import yaml
from PIL import Image
from anthropic import AsyncAnthropic, APIConnectionError, RateLimitError, APIStatusError
from fastapi import HTTPException

from eidolon_ai_client.events import (
    StringOutputEvent,
    ObjectOutputEvent,
    ToolCall,
)
from eidolon_ai_client.util.logger import logger as eidolon_logger
from eidolon_ai_sdk.agent_os import AgentOS
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


async def convert_to_llm(message: LLMMessage):
    if isinstance(message, SystemMessage):
        return {"role": "system", "content": message.content}
    elif isinstance(message, UserMessage):
        content = message.content
        if not isinstance(content, str):
            content = []
            for part in message.content:
                if part.type == "text":
                    content.append({"type": "text", "text": part.text})
                else:
                    # retrieve the image from the file system
                    data = await AgentOS.file_memory.read_file(part.image_url)
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


claude_opus = "claude-3-opus-20240229"


class AnthropicLLMUnitSpec(LLMUnitSpec):
    model: AnnotatedReference[LLMModel, claude_opus]
    temperature: float = 0.3
    max_tokens: Optional[int] = None
    client_args: dict = {}


class AnthropicLLMUnit(LLMUnit, Specable[AnthropicLLMUnitSpec]):
    temperature: float

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        LLMUnit.__init__(self, **kwargs)
        Specable.__init__(self, **kwargs)

        self.temperature = self.spec.temperature

    async def execute_llm(
        self,
        call_context: CallContext,
        messages: List[LLMMessage],
        tools: List[LLMCallFunction],
        output_format: Union[Literal["str"], Dict[str, Any]],
    ) -> AsyncIterator[AssistantMessage]:
        if len(tools) > 0:
            logger.warn("Anthropic does not support tool calls, ignoring")
        can_stream_message, request = await self._build_request(messages, tools, output_format)

        logger.info("executing open ai llm request", extra=request)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("request content:\n" + yaml.dump(request))
        llm_request = replayable(fn=_llm_request(), name_override="anthropic_completion", parser=_raw_parser)
        complete_message = ""
        try:
            async for message in llm_request(client_args=self.spec.client_args, **request):
                # todo -- handle tool calls in some weird way...
                if can_stream_message:
                    logger.debug(f"anthropic llm stream response: {message}", extra=dict(content=message))
                    yield StringOutputEvent(content=message)
                else:
                    complete_message += message

            if not can_stream_message:
                logger.debug(f"anthropic llm object response: {complete_message}", extra=dict(content=complete_message))
                # message format looks like json```{...}```, parse content and pull out the json
                complete_message = complete_message[complete_message.find("{") : complete_message.rfind("}") + 1]

                content = json.loads(complete_message) if complete_message else {}
                yield ObjectOutputEvent(content=content)
        except APIConnectionError as e:
            raise HTTPException(502, f"Anthropic Error: {e.message}") from e
        except RateLimitError as e:
            raise HTTPException(429, "Anthropic Rate Limit Exceeded") from e
        except APIStatusError as e:
            raise HTTPException(502, f"Anthropic Status Error: {e.message}") from e

    async def _build_request(self, inMessages, inTools, output_format):
        # tools = await self._build_tools(inTools)
        tools = []
        system_prompt = "\n".join([message.content for message in inMessages if isinstance(message, SystemMessage)])
        messages = [await convert_to_llm(message) for message in inMessages if not isinstance(message, SystemMessage)]
        request = {
            "messages": messages,
            "model": self.model.name,
            "temperature": self.temperature,
        }
        if system_prompt:
            request["system"] = system_prompt

        if output_format == "str" or output_format["type"] == "string":
            is_string = True
        else:
            is_string = False
            force_json_msg = (
                f"Your response MUST be valid JSON satisfying the following JSON schema:\n{json.dumps(output_format)}"
            )
            force_json_msg += "\nThe response will be wrapped in a json section json```{...}```\nRemember to use double quotes for strings and properties."

            # add response rules to original system message for this call only
            if messages[0]["role"] == "system":
                messages[0]["content"] += f"\n\n{force_json_msg}"
            else:
                messages.insert(0, {"role": "system", "content": force_json_msg})
        logger.debug(messages)
        if len(tools) > 0:
            request["tools"] = tools
        request["max_tokens"] = self.spec.max_tokens or 4000
        return is_string, request

    async def _build_tools(self, inTools):
        tools = []
        # for tool in inTools:
        #     tools.append(
        #         ChatCompletionToolParam(
        #             **{
        #                 "type": "function",
        #                 "function": {
        #                     "name": tool.name,
        #                     "description": tool.description,
        #                     "parameters": tool.parameters,
        #                 },
        #             }
        #         )
        #     )
        return tools


def _convert_tool_call(tool: Dict[str, any]) -> ToolCall:
    name = tool["name"]
    try:
        loads = json.loads(tool["arguments"])
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Error decoding response function arguments for tool {name}") from e
    return ToolCall(tool_call_id=tool["id"], name=name, arguments=loads)


def _llm_request():
    async def fn(client_args: dict = None, **kwargs):
        client = AsyncAnthropic(**(client_args or {}))
        async with client.messages.stream(**kwargs) as stream:
            async for e in stream.text_stream:
                yield e

    return fn


async def _raw_parser(resp):
    async for m_chunk in resp:
        yield m_chunk
