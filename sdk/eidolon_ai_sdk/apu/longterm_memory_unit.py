from pydantic import BaseModel
from typing import Optional, List

from eidolon_ai_sdk.apu.call_context import CallContext
from eidolon_ai_sdk.apu.llm_message import LLMMessage
from eidolon_ai_sdk.apu.llm_unit import LLMUnit
from eidolon_ai_sdk.apu.processing_unit import ProcessingUnit
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.reference_model import Specable


class LongTermMemoryUnitConfig(BaseModel):
    user_scoped: bool
    llm_unit: Optional[Reference[LLMUnit]] = None


class LongTermMemoryUnit(ProcessingUnit, Specable[LongTermMemoryUnitConfig]):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

    def store_message(self, call_context: CallContext, message: LLMMessage):
        raise NotImplementedError

    def store_messages(self, call_context: CallContext, messages: List[LLMMessage]):
        raise NotImplementedError

    def search_memories(self, query: str | LLMMessage | List[LLMMessage]):
        raise NotImplementedError

    def get_all_memories(self):
        raise NotImplementedError

    def delete_memories_for_process(self, process_id: str):
        raise NotImplementedError

    def _get_memory(self, mem_id: str):
        raise NotImplementedError
