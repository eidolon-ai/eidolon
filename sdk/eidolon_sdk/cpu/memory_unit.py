from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel, Field

from eidolon_sdk.cpu.agent_bus import BusEvent, CallContext
from eidolon_sdk.cpu.bus_messages import READ_PORT, WRITE_PORT
from eidolon_sdk.cpu.llm_message import LLMMessage
from eidolon_sdk.cpu.processing_unit import ProcessingUnit
from eidolon_sdk.reference_model import Specable


class MemoryUnitConfig(BaseModel):
    ms_read: READ_PORT = Field(default=None, description="A port that, when bound to an event, will read a new conversation message in the event and store it at the end "
                                                         "of the current conversation.")
    msf_read: READ_PORT = Field(description="A port that, when bound to an event, will read a new conversation message in the event and store it at the end "
                                            "of the current conversation. This will produce a write on the the MSF write port.")
    msf_write: WRITE_PORT = Field(description="A port that, when bound to an event, will write the complete conversation history to the event bus.")


class MemoryUnit(ProcessingUnit, Specable[MemoryUnitConfig], ABC):
    def __init__(self, spec: MemoryUnitConfig = None):
        self.spec = spec

    async def bus_read(self, event: BusEvent):
        if event.event_type == self.spec.ms_read:
            await self.processStoreEvent(event.call_context, event.messages)
        elif event.event_type == self.spec.msf_read:
            await self.processStoreAndFetchEvent(event.call_context, event.messages)

    async def processStoreEvent(self, call_context: CallContext, messages: List[LLMMessage]):
        await self.writeMessages(call_context, messages)

    async def processStoreAndFetchEvent(self, call_context: CallContext, messages: List[LLMMessage]):
        await self.writeMessages(call_context, messages)
        conversation = await self.getConversationHistory(call_context)
        self.request_write(BusEvent(
            call_context,
            self.spec.msf_write,
            conversation
        ))

    @abstractmethod
    async def writeMessages(self, call_context: CallContext, messages: List[LLMMessage]):
        pass

    @abstractmethod
    async def getConversationHistory(self, call_context: CallContext) -> List[LLMMessage]:
        pass
