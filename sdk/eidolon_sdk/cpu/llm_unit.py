from abc import ABC

from openai import AsyncOpenAI, RateLimitError, APIStatusError, APIConnectionError
from openai.types.chat.completion_create_params import ResponseFormat
from pydantic import BaseModel

from eidolon_sdk.cpu.agent_bus import BusParticipant, BusEvent
from eidolon_sdk.cpu.llm_message import LLMMessage, AssistantMessage


class CompletionUsage(BaseModel):
    completion_tokens: int
    """Number of tokens in the generated completion."""

    prompt_tokens: int
    """Number of tokens in the prompt."""

    total_tokens: int
    """Total number of tokens used in the request (prompt + completion)."""


class LLMUnit(ABC, BusParticipant):
    pass


def convert_to_openai(message: LLMMessage):
    if message.type == "system":
        return {
            "role": "system",
            "content": message.content
        }
    elif message.type == "user":
        return {
            "role": "user",
            "content": message.content
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


class OpenAIGPT(LLMUnit):
    model: str
    temperature: float

    def __init__(self, model: str, temperature: float):
        self.model = model
        self.temperature = temperature
        self.llm = AsyncOpenAI()

    async def bus_read(self, bus):
        if bus.current_event.event_type == "llm_event":
            messages = [convert_to_openai(message) for message in bus.current_event.event_data["messages"]]
            output_format = bus.current_event.event_data["output_format"]
            # add a message to the LLM for the output format which is already in json schema format
            messages.append({
                "role": "user",
                "content": f"The output MUST be valid json and the schema for the response message is {output_format}"
            })
            # This event is a request to query the LLM
            try:
                response = await self.llm.chat.completions.create(
                    messages=messages,
                    model=self.model,
                    temperature=self.temperature,
                    response_format=ResponseFormat(type="json_object")
                )

                bus_event = BusEvent(
                    bus.current_event.process_id,
                    bus.current_event.thread_id,
                    "llm_response", {
                        "usage": CompletionUsage.model_validate(response.usage),
                        "message": AssistantMessage.model_validate(response.choices[0].message)
                    })
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
