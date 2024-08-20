from pydantic import BaseModel
from typing import Optional, List, Callable
from enum import Enum

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.apu.call_context import CallContext
from eidolon_ai_sdk.apu.llm_message import LLMMessage
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.apu.processing_unit import ProcessingUnit
from eidolon_ai_sdk.apu.llm_unit import LLMUnit
from eidolon_ai_sdk.apu.mem0 import EidolonMem0
from eidolon_ai_sdk.system.reference_model import Reference
from qdrant_client.http.models import ScoredPoint

EIDOLON_DB_COL_NAME = "eidolon_mem0"


class LongTermMemoryUnitScope(Enum):
    SYSTEM = "system"
    AGENT = "agent"
    USER = "user"
    USER_AGENT = "userAgent"
    USER_PROCESS = "userProcess"


class LongTermMemoryUnitConfig(BaseModel):
    llm_unit: Optional[Reference[LLMUnit]]
    pass


class LongTermMemoryUnit(ProcessingUnit, Specable[LongTermMemoryUnitConfig]):
    mem0: EidolonMem0

    def __init__(self, default_llm: LLMUnit, unit_scope: LongTermMemoryUnitScope, spec: LongTermMemoryUnitConfig = None, memory_converter: Optional[Callable[[List[ScoredPoint]], List[ScoredPoint]]] = None, **kwargs):
        super().__init__(**kwargs)
        self.spec = spec
        self.unit_scope = unit_scope
        if spec is not None and spec.llm_unit is not None:
            default_llm = spec.llm_unit
        self.mem0 = EidolonMem0(default_llm, EIDOLON_DB_COL_NAME, memory_converter=memory_converter)

    def storeMessage(self, call_context: CallContext, message: LLMMessage):
        user_id = AgentOS.current_user().id
        agent_name = AgentOS.current_agent_name()
        metadata = {
            "process_id": call_context.process_id,
            "agent_name": agent_name
        }
        # not sure if I should manipulate result somehow - what's the expected return value?
        return self.mem0.add(message, user_id=user_id, metadata=metadata)

    def storeMessages(self, call_context: CallContext, messages: List[LLMMessage]):
        user_id = AgentOS.current_user().id
        agent_name = AgentOS.current_agent_name()
        metadata = {
            "process_id": call_context.process_id,
            "agent_name": agent_name
        }
        # not sure if I should manipulate result somehow - what's the expected return value?
        return self.mem0.add(messages, user_id=user_id, metadata=metadata)

    def searchMemories(self, call_context: CallContext, query: str | LLMMessage | List[LLMMessage]):
        user_id = AgentOS.current_user().id
        results = self.mem0.search(query) if self._multi_user_scope() else self.mem0.search(query, user_id=user_id)
        if (self.unit_scope == LongTermMemoryUnitScope.SYSTEM):
            return results

        def filter_func(res):
            try:
                valid = True
                if not self._multi_process_scope() and res['metadata']['process_id'] != call_context.process_id:
                    valid = False
                if not self._multi_agent_scope() and res['metadata']['agent_name'] != AgentOS.current_agent_name():
                    valid = False
                return valid
            except Exception:
                # assume caused by missing process_id or agent_id fields
                if self._multi_process_scope() and self._multi_agent_scope():
                    return True
                return False

        filtered_results = list(filter(filter_func, results))
        return filtered_results

    def getAllMemories(self, call_context: CallContext):
        if self._unit_scope == LongTermMemoryUnitScope.SYSTEM:
            return self.mem0.get_all()
        elif self.unit_scope == LongTermMemoryUnitScope.USER:
            return self.mem0.get_all(user_id=AgentOS.current_user().id)

        user_id = AgentOS.current_user().id
        memories = self.mem0.get_all() if self._multi_user_scope() else self.mem0.get_all(user_id=user_id)

        def filter_func(mem):
            try:
                valid = True
                if not self._multi_process_scope() and mem['metadata']['process_id'] != call_context.process_id:
                    valid = False
                if not self._multi_agent_scope() and mem['metadata']['agent_name'] != AgentOS.current_agent_name():
                    valid = False
                return valid
            except Exception:
                if self._multi_agent_scope() and self._multi_process_scope():
                    return False
                return True

        return list(filter(filter_func, memories))

    def getMemory(self, memory_id: str):
        return self.mem0.get(memory_id)

    def getMemoryHistory(self, memory_id: str):
        return self.mem0.history(memory_id)

    def deleteMemory(self, memory_id: str):
        return self.mem0.delete(memory_id)

    def deleteMemoriesForProcess(self, process_id: str):
        memories = self.mem0.get_all()
        for mem in memories:
            try:
                if mem['metadata']['process_id'] == process_id:
                    self.mem0.delete(mem['id'])
            except Exception:
                continue

    def deleteMemoriesForAgent(self, agent_id: str):
        memories = self.mem0.get_all(agent_id=agent_id)
        for mem in memories:
            self.mem0.delete(mem.id)

    def _multi_agent_scope(self):
        if self.unit_scope == LongTermMemoryUnitScope.SYSTEM or self.unit_scope == LongTermMemoryUnitScope.USER:
            return True
        return False

    def _multi_user_scope(self):
        if self.unit_scope == LongTermMemoryUnitScope.AGENT or self.unit_scope == LongTermMemoryUnitScope.SYSTEM:
            return True
        return False

    def _multi_process_scope(self):
        if self.unit_scope != LongTermMemoryUnitScope.USER_PROCESS:
            return True
        return False
