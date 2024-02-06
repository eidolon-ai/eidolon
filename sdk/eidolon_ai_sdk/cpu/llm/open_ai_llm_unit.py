import base64
import json
import logging
import yaml
from PIL import Image
from io import BytesIO
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionToolParam, ChatCompletionChunk
from openai.types.chat.completion_create_params import ResponseFormat
from pydantic import Field, BaseModel
from typing import List, Optional, Union, Literal, Dict, Any, AsyncIterator, cast

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.llm_message import (
    LLMMessage,
    AssistantMessage,
    ToolCall,
    ToolResponseMessage,
    UserMessage,
    SystemMessage,
)
from eidolon_ai_sdk.cpu.llm_unit import LLMUnit, LLMCallFunction
from eidolon_ai_sdk.io.events import (
    ErrorEvent,
    StringOutputEvent,
    ObjectOutputEvent,
    StartLLMEvent,
    SuccessEvent,
    LLMToolCallRequestEvent,
)
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.util.logger import logger as eidolon_logger

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


def convert_to_openai(message: LLMMessage):
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
                    data = AgentOS.file_memory.read_file(part.image_url)
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


class OpenAiGPTSpec(BaseModel):
    model: str = Field(default="gpt-4-1106-preview", description="The model to use for the LLM.")
    temperature: float = 0.3
    force_json: bool = True
    max_tokens: Optional[int] = None


class OpenAIGPT(LLMUnit, Specable[OpenAiGPTSpec]):
    model: str
    temperature: float
    llm: AsyncOpenAI = None

    def __init__(self, **kwargs):
        LLMUnit.__init__(self, **kwargs)
        Specable.__init__(self, **kwargs)

        self.model = self.spec.model
        self.temperature = self.spec.temperature

    async def execute_llm(
        self,
        call_context: CallContext,
        messages: List[LLMMessage],
        tools: List[LLMCallFunction],
        output_format: Union[Literal["str"], Dict[str, Any]],
    ) -> AsyncIterator[AssistantMessage]:
        if not self.llm:
            self.llm = AsyncOpenAI()
        yield StartLLMEvent()

        try:
            can_stream_message, request = await self._build_request(messages, tools, output_format)
            request["stream"] = True

            logger.info("executing open ai llm request", extra=request)
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug("request content:\n" + yaml.dump(request))
            llm_response = await self.llm.chat.completions.create(**request)
            complete_message = ""
            tools_to_call = []
            async for m_chunk in llm_response:
                chunk = cast(ChatCompletionChunk, m_chunk)
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
            yield SuccessEvent()
        except Exception as e:
            logger.exception("error calling open ai llm")
            yield ErrorEvent(reason=e)

    async def _build_request(self, inMessages, inTools, output_format):
        tools = await self._build_tools(inTools)
        messages = [convert_to_openai(message) for message in inMessages]
        request = {
            "messages": messages,
            "model": self.model,
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
