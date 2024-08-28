from enum import Enum
from typing import Optional, List, Callable

from pydantic import BaseModel
from qdrant_client.http.models import ScoredPoint

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.apu.call_context import CallContext
from eidolon_ai_sdk.apu.llm_message import LLMMessage
from eidolon_ai_sdk.apu.llm_unit import LLMUnit
from eidolon_ai_sdk.apu.mem0 import EidolonMem0
from eidolon_ai_sdk.apu.processing_unit import ProcessingUnit
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.reference_model import Specable


class LongTermMemoryUnitConfig(BaseModel):
    user_scoped: bool
    llm_unit: Optional[Reference[LLMUnit]] = None
    collection_name: str = "eidolon_mem0"


class LongTermMemoryUnit(ProcessingUnit, Specable[LongTermMemoryUnitConfig]):
    mem0: EidolonMem0

    def __init__(self, default_llm: LLMUnit, spec: LongTermMemoryUnitConfig = None,
                 memory_converter: Optional[Callable[[List[ScoredPoint]], List[ScoredPoint]]] = None, **kwargs):
        super().__init__(**kwargs)
        self.spec = spec
        self.user_scoped = spec.user_scoped
        if spec is not None and spec.llm_unit is not None:
            default_llm = spec.llm_unit
        self.mem0 = EidolonMem0(default_llm, spec.collection_name, memory_converter=memory_converter)

    def store_message(self, call_context: CallContext, message: LLMMessage):
        user_id = AgentOS.current_user().id
        agent_name = AgentOS.current_agent_name()
        metadata = {
            "process_id": call_context.process_id,
            "agent_name": agent_name
        }
        return self.mem0.add(message, user_id=user_id, metadata=metadata)

    def store_messages(self, call_context: CallContext, messages: List[LLMMessage]):
        user_id = AgentOS.current_user().id
        agent_name = AgentOS.current_agent_name()
        metadata = {
            "process_id": call_context.process_id,
            "agent_name": agent_name
        }
        return self.mem0.add(messages, user_id=user_id, metadata=metadata)

    def search_memories(self, query: str | LLMMessage | List[LLMMessage]):
        user_id = AgentOS.current_user().id
        results = self.mem0.search(query) if not self.user_scoped else self.mem0.search(query, user_id=user_id)
        return results

    def get_all_memories(self):
        return (self.mem0.get_all() if self.user_scoped else self.mem0.get_all(user_id=AgentOS.current_user().id))

    def delete_memories_for_process(self, process_id: str):
        memories = self.mem0.get_all()
        for mem in memories:
            try:
                if mem['metadata']['process_id'] == process_id:
                    self.mem0.delete(mem['id'])
            except Exception:
                continue

    def _get_memory(self, mem_id: str):
        return self.mem0.get(mem_id)