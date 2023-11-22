import logging
from typing import List, Annotated

import tiktoken
from pydantic import Field

from eidolon_sdk.cpu.agent_bus import CallContext
from eidolon_sdk.cpu.llm_message import LLMMessage
from eidolon_sdk.cpu.llm_unit import LLM_MAX_TOKENS, LLMUnit
from eidolon_sdk.cpu.memory_unit import MemoryUnit, MemoryUnitConfig
from eidolon_sdk.impl.message_summarizer import MessageSummarizer
from eidolon_sdk.reference_model import Specable, Reference


class SummarizationMemoryUnitConfig(MemoryUnitConfig):
    max_token_frac: Annotated[float, Field(strict=True, gt=0, le=1)] = 0.75
    summarizer: Reference[MessageSummarizer] = Reference(implementation="eidolon_sdk.impl.message_summarizer.MessageSummarizer")


class SummarizationMemoryUnit(MemoryUnit, Specable[MemoryUnitConfig]):
    def __init__(self, spec: SummarizationMemoryUnitConfig):
        super().__init__(spec)
        self.max_token_frac = spec.max_token_frac

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
            "thread_id": call_context.thread_id,
            "archive": None
        }):
            existingMessages.append(LLMMessage.from_dict(message["message"]))

        logging.debug("existingMessages = " + str(existingMessages))
        return existingMessages

    async def processStoreAndFetchEvent(self, call_context: CallContext, messages: List[LLMMessage]):
        await super().processStoreAndFetchEvent(call_context, messages)
        llm_unit = self.locate_unit(LLMUnit)

        # cl100k_base encodings only work for gpt-3.5-turbo and up models
        if sum(len(tiktoken.get_encoding('cl100k_base').encode(message.text)) for message in messages) >= LLM_MAX_TOKENS.get(llm_unit.spec.model) * self.max_token_frac:
            # get a handle to the MessageSummarizer logic unit
            # call the summarize_messages function on the MessageSummarizer logic unit
            await self.spec.summarizer.summarize_messages(call_context, llm_unit)
            # return getConversationHistory
            return await self.getConversationHistory(call_context)
