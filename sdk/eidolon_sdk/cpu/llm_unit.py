import logging
from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel, Field

from eidolon_sdk.cpu.agent_bus import BusEvent, CallContext
from eidolon_sdk.cpu.processing_unit import ProcessingUnit
from eidolon_sdk.cpu.bus_messages import READ_PORT, WRITE_PORT
from eidolon_sdk.cpu.llm_message import AssistantMessage, LLMMessage, ToolCallMessage, ToolCall
from eidolon_sdk.reference_model import Specable

LLM_MAX_TOKENS = {
    "DEFAULT": 8192,
    # OpenAI models: https://platform.openai.com/docs/models/overview
    # gpt-4
    "gpt-4-1106-preview": 128000,
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-0613": 8192,
    "gpt-4-32k-0613": 32768,
    "gpt-4-0314": 8192,  # legacy
    "gpt-4-32k-0314": 32768,  # legacy
    # gpt-3.5
    "gpt-3.5-turbo-1106": 16385,
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16385,
    "gpt-3.5-turbo-0613": 4096,  # legacy
    "gpt-3.5-turbo-16k-0613": 16385,  # legacy
    "gpt-3.5-turbo-0301": 4096,  # legacy
}


class CompletionUsage(BaseModel):
    completion_tokens: int
    """Number of tokens in the generated completion."""

    prompt_tokens: int
    """Number of tokens in the prompt."""

    total_tokens: int
    """Total number of tokens used in the request (prompt + completion)."""


class LLMUnitConfig(BaseModel):
    llm_read: READ_PORT = Field(description="A port that, when bound to an event, will read the conversation, or message, from the bus and execute it.")
    llm_write: WRITE_PORT = Field(description="A port that, when bound to an event, will write the response from the LLM to the bus.")
    lt_write: WRITE_PORT = Field(default=None, description="A port that, when bound to an event, will write the tool calls from the LLM to the bus.")
    ltc_write: WRITE_PORT = Field(default=None, description="A port that, when bound to an event, will write the tool calls with the full conversation from the LLM to the bus.")


class AddsMessages(ABC):
    @abstractmethod
    def get_messages(self) -> List[LLMMessage]:
        pass


class LLMUnit(ProcessingUnit, Specable[LLMUnitConfig], ABC):
    def __init__(self, spec: LLMUnitConfig = None):
        self.spec = spec

    async def bus_read(self, event: BusEvent):
        if event.event_type == self.spec.llm_read:
            await self.process_llm_event(event.call_context, event.messages)

    @abstractmethod
    async def process_llm_event(self, call_context: CallContext, messages: List[LLMMessage]):
        pass

    def write_llm_response(self, call_context: CallContext, message: AssistantMessage):
        self.request_write(BusEvent(
            call_context,
            self.spec.llm_write,
            [message]
        ))

    def write_llm_tool_conversations(self, call_context: CallContext, existing_conversation: List[LLMMessage],
                                     tool_call: ToolCall):
        logging.info(f"calling tool {tool_call.name}")
        self.request_write(BusEvent(
            call_context,
            self.spec.lt_write,
            [ToolCallMessage(conversation=existing_conversation, tool_call=tool_call)]
        ))
