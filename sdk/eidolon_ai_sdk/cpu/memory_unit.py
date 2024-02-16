from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel

from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.llm_message import LLMMessage
from eidolon_ai_sdk.cpu.processing_unit import ProcessingUnit
from eidolon_ai_sdk.system.reference_model import Specable


class MemoryUnitConfig(BaseModel):
    pass


class MemoryUnit(ProcessingUnit, Specable[MemoryUnitConfig], ABC):
    def __init__(self, spec: MemoryUnitConfig = None, **kwargs):
        super().__init__(**kwargs)
        self.spec = spec

    async def storeMessages(self, call_context: CallContext, messages: List[LLMMessage]):
        """
        Store the messages for the given call context
        :param call_context: The call context for the current conversation
        :param messages: The messages to store
        :return: None
        """
        await self.writeMessages(call_context, messages)

    async def storeBootMessages(self, call_context: CallContext, messages: List[LLMMessage]):
        """
        Store the messages for the given call context
        :param call_context: The call context for the current conversation
        :param messages: The messages to store
        :return: None
        """
        await self.writeBootMessages(call_context, messages)

    async def storeAndFetch(self, call_context: CallContext, messages: List[LLMMessage]) -> List[LLMMessage]:
        """
        Store the messages and returns the full conversation history for the given call context (including the messages just stored)
        :param call_context: The call context for the current conversation
        :param messages: The messages to store
        :return: The full conversation history for the given call context (including the messages just stored)
        """
        if messages and len(messages) > 0:
            await self.writeMessages(call_context, messages)
        conversation = await self.getConversationHistory(call_context)
        return conversation

    @abstractmethod
    async def writeBootMessages(self, call_context: CallContext, messages: List[LLMMessage]):
        """
        Store the messages for the given call context
        :param call_context: The call context for the current conversation
        :param messages: The messages to store
        :return: None
        """
        raise NotImplementedError("writeBootMessages not implemented")

    @abstractmethod
    async def writeMessages(self, call_context: CallContext, messages: List[LLMMessage]):
        """
        Store the messages for the given call context
        :param call_context: The call context for the current conversation
        :param messages: The messages to store
        :return: None
        """
        raise NotImplementedError("writeMessages not implemented")

    @abstractmethod
    async def getConversationHistory(self, call_context: CallContext) -> List[LLMMessage]:
        """
        Get the full conversation history for the given call context
        :param call_context: The call context for the current conversation
        :return: The full conversation history for the given call context
        """
        raise NotImplementedError("getConversationHistory not implemented")

    async def clone_thread(self, old_context: CallContext, new_context: CallContext):
        messages = await self.getConversationHistory(old_context)
        for m in messages:
            m["thread_id"] = new_context.thread_id
        await self.storeMessages(new_context, messages)
