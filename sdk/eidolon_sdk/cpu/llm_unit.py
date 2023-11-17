import json
from abc import ABC

from openai import AsyncOpenAI, RateLimitError, APIStatusError, APIConnectionError
from openai.types.chat.completion_create_params import ResponseFormat
from pydantic import BaseModel

from eidolon_sdk.cpu.agent_bus import BusParticipant, BusEvent, BusController
from eidolon_sdk.cpu.bus_messages import LLMResponse
from eidolon_sdk.cpu.llm_message import AssistantMessage, LLMMessage
from eidolon_sdk.reference_model import Specable


class CompletionUsage(BaseModel):
    completion_tokens: int
    """Number of tokens in the generated completion."""

    prompt_tokens: int
    """Number of tokens in the prompt."""

    total_tokens: int
    """Total number of tokens used in the request (prompt + completion)."""


class LLMUnit(BusParticipant, ABC):
    pass


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
        return {
            "role": "assistant",
            "content": message.content,
            "tool_calls": message.tool_calls
        }
    elif message.type == "tool":
        return {
            "role": "tool",
            "tool_calls": message.tool_calls
        }
    else:
        raise ValueError(f"Unknown message type {message.type}")


class OpenAiGPTSpec(BaseModel):
    model: str = "gpt-4-1106-preview"
    temperature: float = 0.3


class OpenAIGPT(LLMUnit, Specable[OpenAiGPTSpec]):
    model: str
    temperature: float

    def __init__(self, controller: BusController, spec: OpenAiGPTSpec):
        super().__init__(controller)
        self.model = spec.model
        self.temperature = spec.temperature
        self.llm = AsyncOpenAI()

    async def bus_read(self, event: BusEvent):
        if event.message.event_type == "llm_event":
            messages = [convert_to_openai(message) for message in event.message.messages]
            output_format = event.message.output_format
            # add a message to the LLM for the output format which is already in json schema format
            messages.append({
                "role": "user",
                "content": f"The output MUST be valid json and the schema for the response message is {output_format}"
            })
            # This event is a request to query the LLM
            try:
                print("messages = " + str(messages))
                response = await self.llm.chat.completions.create(
                    messages=messages,
                    model=self.model,
                    temperature=self.temperature,
                    response_format=ResponseFormat(type="json_object")
                )

                response = response.choices[0].message.model_dump()
                response["content"] = json.loads(response["content"])
                bus_event = BusEvent(
                    event.process_id,
                    event.thread_id,
                    LLMResponse(message=AssistantMessage.model_validate(response)))
                self.request_write(bus_event)
            except APIConnectionError as e:
                print("The server could not be reached")
                print(e.__cause__)  # an underlying Exception, likely raised within httpx.
            except RateLimitError as e:
                print("A 429 status code was received; we should back off a bit.")
            except APIStatusError as e:
                print("Another non-200-range status code was received")
                print(e.status_code)
                print(e.response)
