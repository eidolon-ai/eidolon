import json
import logging
from typing import List

from openai import AsyncOpenAI, APIConnectionError, RateLimitError, APIStatusError
from openai.types.chat import ChatCompletionToolParam
from openai.types.chat.completion_create_params import ResponseFormat

from eidolon_sdk.cpu.agent_bus import CallContext
from eidolon_sdk.cpu.llm_message import LLMMessage, AssistantMessage, ToolCall
from eidolon_sdk.cpu.llm_unit import LLMUnit, LLMUnitConfig, LLMCallFunction
from eidolon_sdk.reference_model import Specable


def convert_to_openai(message: LLMMessage):
    if message.type == "system":
        return {
            "role": "system",
            "content": message.content
        }
    elif message.type == "user":
        content = message.content
        if not isinstance(content, str):
            content = [part.model_dump() for part in content]
        return {
            "role": "user",
            "content": content
        }
    elif message.type == "assistant":
        ret = {
            "role": "assistant",
            "content": str(message.content)
        }
        if message.tool_calls and len(message.tool_calls) > 0:
            ret["tool_calls"] = [{
                "id": tool_call.name,
                "type": "function",
                "function": {
                    "name": tool_call.name,
                    "arguments": str(tool_call.arguments)
                }
            } for tool_call in message.tool_calls]
        return ret
    elif message.type == "tool":
        # tool_call_id, content
        return {
            "role": "tool",
            "tool_call_id": message.name,
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

    def __init__(self, spec: OpenAiGPTSpec, **kwargs):
        super().__init__(spec, **kwargs)
        self.model = spec.model
        self.temperature = spec.temperature
        self.llm = AsyncOpenAI()

    async def process_llm_event(self, call_context: CallContext, inMessages: List[LLMMessage], inTools: List[LLMCallFunction], output_format: str) -> AssistantMessage:
        messages = [convert_to_openai(message) for message in inMessages]

        # add a message to the LLM for the output format which is already in json schema format
        messages.append({
            "role": "user",
            "content": f"The output MUST be valid json and the schema for the response message is {output_format}"
        })

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
        try:
            print("messages = " + str(messages))
            # print("tools = " + str(tools))
            request = {
                "messages": messages,
                "model": self.model,
                "temperature": self.temperature,
                "response_format": ResponseFormat(type="json_object")
            }
            if len(tools) > 0:
                request["tools"] = tools

            llm_response = await self.llm.chat.completions.create(**request)
            message = llm_response.choices[0].message
            tool_response = None
            if message.tool_calls:
                tool_response = []
                for tool in message.tool_calls:
                    tool_response.append(ToolCall(name=tool.function.name, arguments=json.loads(tool.function.arguments)))

            if message.content:
                response = json.loads(message.content)
            else:
                response = {}
            return AssistantMessage(content=response, tool_calls=tool_response)
        except APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        except RateLimitError as e:
            print("A 429 status code was received; we should back off a bit.")
        except APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)
        except Exception as e:
            logging.exception("An unknown error occurred")
