import json
from typing import List

from openai import AsyncOpenAI, APIConnectionError, RateLimitError, APIStatusError
from openai.types.chat.completion_create_params import ResponseFormat

from eidolon_sdk.cpu.agent_bus import CallContext
from eidolon_sdk.cpu.llm_message import LLMMessage, ToolCall, AssistantMessage
from eidolon_sdk.cpu.llm_unit import LLMUnit, LLMUnitConfig
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
        return {
            "role": "tool",
            "tool_calls": [ToolCall(name=message.tool_name, arguments=message.tool_arguments)]
        }
    else:
        raise ValueError(f"Unknown message type {message.type}")


class OpenAiGPTSpec(LLMUnitConfig):
    model: str = "gpt-4-1106-preview"
    temperature: float = 0.3


class OpenAIGPT(LLMUnit, Specable[OpenAiGPTSpec]):
    model: str
    temperature: float

    def __init__(self, spec: OpenAiGPTSpec):
        super().__init__(spec)
        self.model = spec.model
        self.temperature = spec.temperature
        self.llm = AsyncOpenAI()

    async def process_llm_event(self, call_context: CallContext, inMessages: List[LLMMessage]):
        messages = [convert_to_openai(message) for message in inMessages]
        # add a message to the LLM for the output format which is already in json schema format
        messages.append({
            "role": "user",
            "content": f"The output MUST be valid json and the schema for the response message is {call_context.output_format}"
        })
        # This event is a request to query the LLM
        try:
            print("messages = " + str(messages))
            llm_response = await self.llm.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=self.temperature,
                response_format=ResponseFormat(type="json_object")
            )

            message = llm_response.choices[0].message
            if message.tool_calls and len(message.tool_calls) > 0:
                for tool_call in message.tool_calls:
                    arguments = json.dumps(tool_call.function.arguments)
                    self.write_llm_tool_conversations(call_context, inMessages, ToolCall(name=tool_call.function.name, arguments=arguments))

            response = message.model_dump()
            response["content"] = json.loads(response["content"])
            self.write_llm_response(call_context, AssistantMessage.model_validate(response))
        except APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        except RateLimitError as e:
            print("A 429 status code was received; we should back off a bit.")
        except APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)
