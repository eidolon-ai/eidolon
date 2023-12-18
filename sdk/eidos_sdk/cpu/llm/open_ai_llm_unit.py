import base64
import json
from io import BytesIO
from typing import List, Optional, Union, Literal, Dict, Any

from PIL import Image
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionToolParam, ChatCompletionMessageToolCall
from openai.types.chat.completion_create_params import ResponseFormat
from pydantic import Field, BaseModel

from eidos_sdk.agent_os import AgentOS
from eidos_sdk.cpu.call_context import CallContext
from eidos_sdk.cpu.llm_message import (
    LLMMessage,
    AssistantMessage,
    ToolCall,
    ToolResponseMessage,
    UserMessage,
    SystemMessage,
)
from eidos_sdk.cpu.llm_unit import LLMUnit, LLMCallFunction
from eidos_sdk.system.reference_model import Specable
from eidos_sdk.util.logger import logger


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
            "content": message.result,
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
        inMessages: List[LLMMessage],
        inTools: List[LLMCallFunction],
        output_format: Union[Literal["str"], Dict[str, Any]],
    ) -> AssistantMessage:
        if not self.llm:
            self.llm = AsyncOpenAI()
        messages = [convert_to_openai(message) for message in inMessages]

        if not isinstance(output_format, str):
            force_json_msg = (
                f"Your response MUST be valid JSON satisfying the following schema:\n{json.dumps(output_format)}"
            )
            if not self.spec.force_json:
                force_json_msg += "\nThe response will be wrapped in a json section json```{...}```\nRemember to use double quotes for strings and properties."

            # add response rules to original system message for this call only
            if messages[0]["role"] == "system":
                messages[0]["content"] += f"\n\n{force_json_msg}"
            else:
                messages.insert(0, {"role": "system", "content": force_json_msg})

        logger.debug(messages)
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
        # This event is a request to query the LLM
        request = {
            "messages": messages,
            "model": self.model,
            "temperature": self.temperature,
        }
        if self.spec.force_json and isinstance(output_format, dict):
            request["response_format"] = ResponseFormat(type="json_object")

        if len(tools) > 0:
            request["tools"] = tools

        if self.spec.max_tokens:
            request["max_tokens"] = self.spec.max_tokens

        logger.info("executing open ai llm request", extra=request)
        try:
            llm_response = await self.llm.chat.completions.create(**request)
        except Exception:
            logger.exception("error calling open ai llm")
            raise
        message = llm_response.choices[0].message

        logger.info(
            f"open ai llm response\ntool calls: {len(message.tool_calls or [])}\ncontent:\n{message.content}",
            extra=dict(content=message.content, tool_calls=message.tool_calls),
        )

        tool_response = [_convert_tool_call(tool) for tool in message.tool_calls or []]
        if not self.spec.force_json and output_format != "str":
            # message format looks like json```{...}```, parse content and pull out the json
            message_text = message.content[message.content.find("{") : message.content.rfind("}") + 1]
        else:
            message_text = message.content

        try:
            if output_format == "str":
                content = message_text
            else:
                content = json.loads(message_text) if message_text else {}
        except json.JSONDecodeError as e:
            raise RuntimeError("Error decoding response content") from e
        return AssistantMessage(content=content, tool_calls=tool_response)


def _convert_tool_call(tool: ChatCompletionMessageToolCall) -> ToolCall:
    try:
        loads = json.loads(tool.function.arguments)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Error decoding response function arguments for tool {tool.function.name}") from e
    return ToolCall(tool_call_id=tool.id, name=tool.function.name, arguments=loads)
