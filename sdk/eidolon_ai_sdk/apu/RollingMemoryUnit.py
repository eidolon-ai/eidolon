from typing import List

import tiktoken
from pydantic import BaseModel, Field
from tiktoken import Encoding

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.apu.call_context import CallContext
from eidolon_ai_sdk.apu.conversation_memory_unit import RawMemoryUnit
from eidolon_ai_sdk.apu.llm_message import LLMMessageTypes, UserMessage, LLMMessage
from eidolon_ai_sdk.system.specable import Specable


class RollingMemoryUnitConfig(BaseModel):
    """
    Memory unit that only retrieves the most recent messages that are under a token limit. Does not summarize removed messages.
    """

    encoding: str = Field("o200k_base", description="tiktoken encoding to use when counting tokens")
    token_limit: int = Field(32000, description="The maximum number of message tokens to sent to llm")


class RollingMemoryUnit(RawMemoryUnit, Specable[RollingMemoryUnitConfig]):
    encoding: Encoding

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.encoding = tiktoken.get_encoding(self.spec.encoding)

    async def getConversationHistory(self, call_context: CallContext, include_boot: bool = True) -> List[LLMMessageTypes]:
        boot_messages = []
        if include_boot:
            async for message in AgentOS.symbolic_memory.find(
                    "conversation_memory",
                    {
                        "process_id": call_context.process_id,
                        "thread_id": call_context.thread_id,
                        "is_boot_message": True,
                    },
                    {"is_boot_message": 0},
            ):
                boot_messages.append(LLMMessage.from_dict(message["message"]))

        non_boot_messages = []
        async for message in AgentOS.symbolic_memory.find(
                "conversation_memory",
                {
                    "process_id": call_context.process_id,
                    "thread_id": call_context.thread_id,
                    "is_boot_message": False,
                },
                {"is_boot_message": 0},
        ):
            non_boot_messages.append(LLMMessage.from_dict(message["message"]))

        total_token_count = 0

        for message in boot_messages:
            message_str = message.model_dump_json()
            total_token_count += len(self.encoding.encode(message_str))

        for i in reversed(range(len(non_boot_messages))):
            message: LLMMessageTypes = non_boot_messages[i]
            message_str = message.model_dump_json()  # this will over count since it includes json object, but fine for now
            total_token_count += len(self.encoding.encode(message_str))
            if total_token_count > self.spec.token_limit:
                non_boot_messages = non_boot_messages[i+1:]
                break

        while non_boot_messages and not isinstance(non_boot_messages[0], UserMessage):
            non_boot_messages = non_boot_messages[1:]

        return boot_messages + non_boot_messages
