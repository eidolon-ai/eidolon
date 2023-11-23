from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel

from eidolon_sdk.cpu.call_context import CallContext
from eidolon_sdk.cpu.llm_message import LLMMessage
from eidolon_sdk.cpu.processing_unit import ProcessingUnit
from eidolon_sdk.reference_model import Specable


class MemoryUnitConfig(BaseModel):
    pass


class MemoryUnit(ProcessingUnit, Specable[MemoryUnitConfig], ABC):
    def __init__(self, spec: MemoryUnitConfig = None, **kwargs):
        super().__init__(**kwargs)
        self.spec = spec

    async def storeMessages(self, call_context: CallContext, messages: List[LLMMessage]):
        await self.writeMessages(call_context, messages)

    async def storeAndFetch(self, call_context: CallContext, messages: List[LLMMessage]) -> List[LLMMessage]:
        if messages and len(messages) > 0:
            await self.writeMessages(call_context, messages)
        conversation = await self.getConversationHistory(call_context)
        return conversation

    @abstractmethod
    async def writeMessages(self, call_context: CallContext, messages: List[LLMMessage]):
        raise NotImplementedError("getConversationHistory not implemented")

    @abstractmethod
    async def getConversationHistory(self, call_context: CallContext) -> List[LLMMessage]:
        raise NotImplementedError("getConversationHistory not implemented")
