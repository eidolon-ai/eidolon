from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.apu.call_context import CallContext
from eidolon_ai_sdk.apu.llm_message import LLMMessage
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.apu.processing_unit import ProcessingUnit
from eidolon_ai_sdk.apu.llm_unit import LLMUnit
from eidolon_ai_sdk.apu.mem0 import EidolonMem0
from eidolon_ai_sdk.agent_os_interfaces import SimilarityMemory

EIDOLON_DB_COL_NAME = "eidolon_mem0"

class LongTermMemoryUnitScope(Enum):
    SYSTEM = "system"
    AGENT = "agent"
    USER = "user"
    USER_AGENT = "userAgent"
    USER_PROCESS = "userProcess"

class LongTermMemoryUnitConfig(BaseModel):
    llm_unit: Optional[LLMUnit]
    unit_scope: Optional[LongTermMemoryUnitScope]
    pass

class LongTermMemoryUnit(ProcessingUnit, Specable[LongTermMemoryUnitConfig]):
    def __init__(self, default_llm: LLMUnit,  spec: LongTermMemoryUnitConfig = None, **kwargs):
        super().__init__(**kwargs)
        self.spec = spec
        if spec.unit_scope is None:
            self.unit_scope = LongTermMemoryUnitScope.USER_PROCESS
        else :
            self.unit_scope = spec.unit_scope
        if spec.llm_unit is not None:
            self.mem0 = EidolonMem0(spec.llm_unit, EIDOLON_DB_COL_NAME)
        else:
            self.mem0 = EidolonMem0(default_llm, EIDOLON_DB_COL_NAME)

    def storeMessage(self, call_context: CallContext, message: LLMMessage):
        user_id = AgentOS.current_user().id
        agent_name = AgentOS.current_agent_name()
        metadata = {
            "process_id": call_context.process_id,
            "agent_name": AgentOS.current_agent_name()
        }
        # not sure if I should manipulate result somehow - what's the expected return value?
        return self.mem0.add(message, user_id=user_id, agent_id=agent_name, metadata=metadata)

    def storeMessages(self, call_context: CallContext, messages: List[LLMMessage]):
        user_id = AgentOS.current_user().id
        agent_name = AgentOS.current_agent_name()
        metadata = {
            "process_id": call_context.process_id,
            "agent_name": AgentOS.current_agent_name()
        }
        # not sure if I should manipulate result somehow - what's the expected return value?
        return self.mem0.add(messages, user_id=user_id, metadata=metadata, agent_id=agent_name)

    def searchMemories(self, call_context: CallContext, message: LLMMessage):
        query = str(message)
        user_id = AgentOS.current_user().id
        results = self.mem0.search(query) if self._multi_user_scope() else self.mem0.search(query, user_id=user_id)
        def filter_func(res):
            try:
                valid = True
                if not self._multi_process_scope() and res.metadata.process_id != call_context.process_id:
                    valid = False
                if not self._multi_agent_scope() and res.agent_id != AgentOS.current_agent_name():
                    valid = False
                return valid
            except:
                # assume caused by missing process_id or agent_id fields
                if self._multi_process_scope() and self._multi_agent_scope():
                    return True
                return False
            
        filtered_results = results.filter(filter_func)
        return filtered_results

    def getAllMemories(self, call_context: CallContext):
        if self.unit_scope == LongTermMemoryUnitScope.AGENT:
            return self.mem0.get_all(agent_id=AgentOS.current_agent_name())
        elif self.unit_scope == LongTermMemoryUnitScope.USER:
            return self.mem0.get_all(user_id=AgentOS.current_user().id)
        elif self.unit_scope == LongTermMemoryUnitScope.USER_AGENT:
            return self.mem0.get_all(user_id=AgentOS.current_user().id, agent_id=AgentOS.current_agent_name()) 
        
        memories = self.mem0.get_all(user_id=AgentOS.current_user().id)
        if self._unit_scope == LongTermMemoryUnitScope.SYSTEM:
            return memories
        
        def filter_func(mem):
            try:
                valid = True
                if not self._multi_process_scope() and mem.metadata.process_id != call_context.process_id:
                    valid = False
                return valid
            except:
                if self._multi_agent_scope() and self._multi_process_scope():
                    return False
                return True

        return memories.filter(filter_func)
    
    def getMemoryHistory(self, memory_id: str):
        return self.mem0.history(memory_id)
    
    def deleteMemory(self, memory_id: str):
        return self.mem0.delete(memory_id)
    
    def deleteMemoriesForProcess(self, process_id: str):
        memories = self.mem0.get_all()
        for mem in memories:
            try:
                if mem.metadata.process_id == process_id:
                    self.mem0.delete(mem.id)
            except:
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
        if self.unit_scope != LongTermMemoryUnitScope:
            return True
        return False