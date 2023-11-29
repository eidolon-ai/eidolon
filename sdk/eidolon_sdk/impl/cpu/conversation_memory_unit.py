import logging
from typing import List

from eidolon_sdk.cpu.call_context import CallContext
from eidolon_sdk.cpu.llm_message import LLMMessage
from eidolon_sdk.cpu.memory_unit import MemoryUnit, MemoryUnitConfig
from eidolon_sdk.reference_model import Specable


class ConversationalMemoryUnit(MemoryUnit, Specable[MemoryUnitConfig]):
    async def writeMessages(self, call_context: CallContext, messages: List[LLMMessage]):
        conversationItems = [{
            "process_id": call_context.process_id,
            "thread_id": call_context.thread_id,
            "message": message.model_dump()} for message in messages]

        logging.debug(str(messages))
        logging.debug(conversationItems)

        await self.agent_memory.symbolic_memory.insert("conversation_memory", conversationItems)

    async def getConversationHistory(self, call_context: CallContext) -> List[LLMMessage]:
        existingMessages = []
        async for message in self.agent_memory.symbolic_memory.find("conversation_memory", {
            "process_id": call_context.process_id,
            "thread_id": call_context.thread_id
        }):
            existingMessages.append(LLMMessage.from_dict(message["message"]))

        logging.debug("existingMessages = " + str(existingMessages))
        return existingMessages
