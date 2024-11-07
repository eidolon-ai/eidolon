import base64
import json
import logging
from io import BytesIO
from typing import List, Optional, Union, Literal, Dict, Any, AsyncIterator, cast

import yaml
from PIL import Image
from anthropic import (
    AsyncAnthropic,
    APIConnectionError,
    RateLimitError,
    APIStatusError,
    TextEvent,
    ContentBlockStopEvent, AuthenticationError,
)
from anthropic.types import MessageStreamEvent, ToolUseBlock, TextBlockParam, ImageBlockParam, ToolUseBlockParam
from anthropic.types.image_block_param import Source
from fastapi import HTTPException

from eidolon_ai_client.events import (
    StringOutputEvent,
    ObjectOutputEvent,
    ToolCall,
    LLMToolCallRequestEvent,
)
from eidolon_ai_client.util.logger import logger as eidolon_logger
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.apu.llm_message import (
    LLMMessage,
    AssistantMessage,
    ToolResponseMessage,
    UserMessage,
    SystemMessage,
)
from eidolon_ai_sdk.apu.llm_unit import LLMUnit, LLMCallFunction, LLMModel, LLMUnitSpec
from eidolon_ai_sdk.system.reference_model import AnnotatedReference
from eidolon_ai_sdk.system.specable import Specable
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


class GroupedToolResponse(LLMMessage):
    tool_responses: List[ToolResponseMessage]
    type: str = "grouped_tool"


async def convert_to_llm(message: LLMMessage):
    if isinstance(message, SystemMessage):
        return {"role": "user", "content": [TextBlockParam(type="text", text=message.content)]}
    elif isinstance(message, UserMessage):
        content = message.content
        if not isinstance(content, str):
            content = []
            for part in message.content:
                if part.type == "text":
                    if part.text:
                        content.append(TextBlockParam(text=part.text, type="text"))
                else:
                    # retrieve the image from the file system
                    data = await AgentOS.file_memory.read_file(part.image_url)
                    # scale the image such that the max size of the shortest size is at most 768px
                    data = scale_image(data)
                    # base64 encode the data
                    base64_image = base64.b64encode(data).decode("utf-8")
                    content.append(
                        ImageBlockParam(
                            source=Source(data=base64_image, media_type="image/png", type="base64"), type="image"
                        )
                    )
        else:
            content = [TextBlockParam(type="text", text=content)]

        return {"role": "user", "content": content}
    elif isinstance(message, AssistantMessage):
        content = [TextBlockParam(type="text", text=message.content)]
        if message.tool_calls and len(message.tool_calls) > 0:
            for tool_call in message.tool_calls:
                content.append(
                    ToolUseBlockParam(
                        type="tool_use", id=tool_call.tool_call_id, name=tool_call.name, input=tool_call.arguments
                    )
                )
        return {"role": "assistant", "content": content}
    elif isinstance(message, GroupedToolResponse):
        # dlb - order tool_call_events by tool_call_id to ensure deterministic behavior for tests
        message.tool_responses.sort(key=lambda e: e.tool_call_id)
        # tool_call_id, content
        content = [dict(type="tool_result", tool_use_id=m.tool_call_id, content=[TextBlockParam(type="text", text=json.dumps(m.result))]) for m in message.tool_responses]
        return {
            "role": "user",
            "content": content,
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
        messages: List[LLMMessage],
        tools: List[LLMCallFunction],
        output_format: Union[Literal["str"], Dict[str, Any]],
    ) -> AsyncIterator[AssistantMessage]:
        can_stream_message, request = await self._build_request(messages, tools, output_format)

        logger.info("executing open ai llm request", extra=request)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("request content:\n" + yaml.dump(request))
        llm_request = replayable(fn=_llm_request(), name_override="anthropic_completion", parser=_raw_parser)
        complete_message = ""
        tools_to_call = []
        try:
            async for in_message in llm_request(client_args=self.spec.client_args, **request):
                message = cast(MessageStreamEvent, in_message)

                if isinstance(message, ContentBlockStopEvent) and isinstance(message.content_block, ToolUseBlock):
                    tc = ToolCall(
                        tool_call_id=message.content_block.id,
                        name=message.content_block.name,
                        arguments=message.content_block.input,
                    )
                    tools_to_call.append(tc)
                elif isinstance(message, TextEvent):
                    content = message.text
                    if can_stream_message:
                        logger.debug(f"open ai llm stream response: {content}", extra=dict(content=content))
                        yield StringOutputEvent(content=content)
                    else:
                        complete_message += content

            if len(tools_to_call) > 0:
                logger.info(f"anthropic llm tool calls: {tools_to_call}", extra=dict(tool_calls=tools_to_call))
                for tool in tools_to_call:
                    yield LLMToolCallRequestEvent(tool_call=tool)

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
        except AuthenticationError as e:
            raise HTTPException(500, "Anthropic Authentication Error") from e
        except APIStatusError as e:
            raise HTTPException(502, f"Anthropic Status Error: {e.message}") from e

    async def _build_request(self, inMessages, inTools, output_format):
        tools = await self._build_tools(inTools)
        system_prompt = "\n".join([message.content for message in inMessages if isinstance(message, SystemMessage)])

        # We need to group tool response messages together so they appear in one block
        messages = []
        grouped_tool_responses = []
        for message in inMessages:
            if isinstance(message, ToolResponseMessage):
                grouped_tool_responses.append(message)
            else:
                if grouped_tool_responses:
                    messages.append(GroupedToolResponse(tool_responses=grouped_tool_responses))
                    grouped_tool_responses = []
                messages.append(message)
        if grouped_tool_responses:
            messages.append(GroupedToolResponse(tool_responses=grouped_tool_responses))

        messages = [await convert_to_llm(message) for message in messages if not isinstance(message, SystemMessage)]
        if output_format == "str" or output_format["type"] == "string":
            is_string = True
        else:
            is_string = False
            force_json_msg = (
                f"Your response MUST be valid JSON satisfying the following JSON schema:\n{json.dumps(output_format)}"
            )
            force_json_msg += "\nThe response will be wrapped in a json section json```{...}```\nRemember to use double quotes for strings and properties."

            # add response rules to original system message for this call only
            messages.insert(0, {"role": "user", "content": [TextBlockParam(type="text", text=force_json_msg)]})

        # combine messages such that no two user messages are consecutive
        last_message = None
        new_messages = []
        for message in messages:
            if message["role"] == "user":
                if last_message and last_message["role"] == "user":
                    content = message["content"]
                    last_message["content"].extend(content)
                else:
                    new_messages.append(message)
            else:
                new_messages.append(message)
            last_message = message

        request = {
            "messages": new_messages,
            "model": self.model.name,
            "temperature": self.temperature,
        }
        if system_prompt:
            request["system"] = system_prompt

        logger.debug(new_messages)
        if len(tools) > 0:
            request["tools"] = tools
        request["max_tokens"] = self.spec.max_tokens or 4000
        return is_string, request

    async def _build_tools(self, inTools):
        tools = []
        for tool in inTools:
            tools.append(
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.parameters,
                }
            )
        return tools


def _llm_request():
    async def fn(client_args: dict = None, **kwargs):
        client = AsyncAnthropic(**(client_args or {}))
        try:
            async with client.messages.stream(**kwargs) as stream:
                async for e in stream:
                    yield e
        except TypeError as e:
            if "Could not resolve authentication method." in str(e):
                raise HTTPException(500, "Authentication Error: set envar `ANTHROPIC_API_KEY`")
            raise

    return fn


async def _raw_parser(resp):
    async for in_message in resp:
        message = cast(MessageStreamEvent, in_message)

        if isinstance(message, ContentBlockStopEvent) and isinstance(message.content_block, ToolUseBlock):
            yield f"\nTool Call: {message.content_block.name}\nArguments: {message.content_block.input}\n"
        elif isinstance(message, TextEvent):
            yield message.text
