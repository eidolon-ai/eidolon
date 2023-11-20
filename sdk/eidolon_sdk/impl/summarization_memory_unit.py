from typing import List

import tiktoken

from eidolon_sdk.cpu.agent_bus import CallContext
from eidolon_sdk.cpu.llm_message import LLMMessage
from eidolon_sdk.cpu.memory_unit import MemoryUnit, MemoryUnitConfig
from eidolon_sdk.reference_model import Specable
from eidolon_sdk.cpu.llm_unit import LLM_MAX_TOKENS


class SummarizationMemoryUnit(MemoryUnit, Specable[MemoryUnitConfig]):
    async def writeMessages(self, call_context: CallContext, messages: List[LLMMessage]):
        conversationItems = [{
            "process_id": call_context.process_id,
            "thread_id": call_context.thread_id,
            "message": message.model_dump()} for message in messages]

        print(str(messages))
        print(conversationItems)

        await self.agent_memory.symbolic_memory.insert("conversation_memory", conversationItems)

    async def getConversationHistory(self, call_context: CallContext) -> List[LLMMessage]:
        existingMessages = []
        async for message in self.agent_memory.symbolic_memory.find("conversation_memory", {
            "process_id": call_context.process_id,
            "thread_id": call_context.thread_id,
            "archive": None
        }):
            existingMessages.append(LLMMessage.from_dict(message["message"]))

        print("existingMessages = " + str(existingMessages))
        return existingMessages

    async def processStoreAndFetchEvent(self, call_context: CallContext, messages: List[LLMMessage]):
        SUMMARIZE_FRAC = 0.75
        # cl100k_base encodings only work for gpt-3.5-turbo and up models
        if sum(len(tiktoken.get_encoding('cl100k_base').encode(message.text)) for message in messages) > LLM_MAX_TOKENS.get('gpt-4-1106-preview') * SUMMARIZE_FRAC:
            # call summarizer
            pass
        await super().processStoreAndFetchEvent(call_context, messages)
