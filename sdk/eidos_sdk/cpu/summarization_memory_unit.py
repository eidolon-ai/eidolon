import logging
from typing import List, Annotated

import tiktoken
from bson import ObjectId
from pydantic import Field

from eidos_sdk.agent_os import AgentOS
from eidos_sdk.cpu.call_context import CallContext
from eidos_sdk.cpu.llm_message import LLMMessage
from eidos_sdk.cpu.llm_unit import LLM_MAX_TOKENS, LLMUnit
from eidos_sdk.cpu.memory_unit import MemoryUnit, MemoryUnitConfig
from eidos_sdk.cpu.message_summarizer import MessageSummarizer
from eidos_sdk.system.reference_model import Specable, AnnotatedReference


class SummarizationMemoryUnitConfig(MemoryUnitConfig):
    max_token_fraction: Annotated[float, Field(strict=True, gt=0, le=1)] = 0.75
    summarizer: AnnotatedReference[MessageSummarizer]


class SummarizationMemoryUnit(MemoryUnit, Specable[SummarizationMemoryUnitConfig]):
    def __init__(self, spec: SummarizationMemoryUnitConfig, **kwargs):
        super().__init__(spec, **kwargs)
        self.max_token_frac = spec.max_token_fraction
        self.summarizer = spec.summarizer.instantiate()

    async def writeMessages(self, call_context: CallContext, messages: List[LLMMessage]):
        conversationItems = [
            {
                "process_id": call_context.process_id,
                "thread_id": call_context.thread_id,
                "message": message.model_dump(),
            }
            for message in messages
        ]

        logging.debug(str(messages))
        logging.debug(conversationItems)

        await AgentOS.symbolic_memory.insert("conversation_memory", conversationItems)

    async def getConversationHistory(self, call_context: CallContext) -> List[LLMMessage]:
        existingMessages = []
        async for message in AgentOS.symbolic_memory.find(
            "conversation_memory",
            {
                "process_id": call_context.process_id,
                "thread_id": call_context.thread_id,
                "archive": None,
                "is_boot_message": False,
            },
            {"is_boot_message": 0},
        ):
            existingMessages.append(LLMMessage.from_dict(message["message"]))

        logging.debug("existingMessages = " + str(existingMessages))
        return existingMessages

    async def storeAndFetch(self, call_context: CallContext, messages: List[LLMMessage]):
        conversation = await super().storeAndFetch(call_context, messages)
        llm_unit = self.locate_unit(LLMUnit)

        num_tokens = sum(
            [len(tiktoken.get_encoding("cl100k_base").encode(message.model_dump_json())) for message in conversation]
        )

        logger = logging.getLogger("eidolon")

        logger.debug(
            "num_tokens = "
            + str(num_tokens)
            + ", tokens limit = "
            + str(LLM_MAX_TOKENS.get(llm_unit.spec.model) * self.max_token_frac)
        )

        # cl100k_base encodings only work for gpt-3.5-turbo and up models
        if num_tokens >= LLM_MAX_TOKENS.get(llm_unit.spec.model) * self.max_token_frac:
            existingMessages = []
            async for message in AgentOS.symbolic_memory.find(
                "conversation_memory",
                {
                    "process_id": call_context.process_id,
                    "thread_id": call_context.thread_id,
                    "archive": None,
                    "is_boot_message": False,
                },
                {"is_boot_message": 0},
            ):
                existingMessages.append(LLMMessage.from_dict(message["message"]))

            # call the summarize_messages function on the MessageSummarizer logic unit
            assistant_message = await self.summarizer.summarize_messages(call_context, existingMessages, llm_unit)

            # create a new object id for the summary message
            summary_id = str(ObjectId())
            # update existing messages and set the archive column to the new object id and insert the new message into the database with the object id all using an upsert in the db
            await AgentOS.symbolic_memory.update_many(
                "conversation_memory",
                {
                    "process_id": call_context.process_id,
                    "thread_id": call_context.thread_id,
                },
                {"$set": {"archive": summary_id}},
            )

            await AgentOS.symbolic_memory.insert_one(
                "conversation_memory",
                {
                    "_id": summary_id,
                    "process_id": call_context.process_id,
                    "thread_id": call_context.thread_id,
                    "message": assistant_message.model_dump(),
                },
            )

        # return getConversationHistory
        return conversation
