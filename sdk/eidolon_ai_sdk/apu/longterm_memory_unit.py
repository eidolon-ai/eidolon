from pydantic import BaseModel
from typing import Optional, List

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.apu.call_context import CallContext
from eidolon_ai_sdk.apu.llm_message import LLMMessage
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.apu.processing_unit import ProcessingUnit
from eidolon_ai_sdk.apu.llm_unit import LLMUnit
from eidolon_ai_sdk.apu.mem0 import EidolonMem0
from eidolon_ai_sdk.agent_os_interfaces import SimilarityMemory


class LongTermMemoryUnitConfig(BaseModel):
    llm_unit: Optional[LLMUnit]
    db_collection: Optional[str]
    similarity_memory: Optional[SimilarityMemory]
    pass

class LongTermMemoryUnit(ProcessingUnit, Specable[LongTermMemoryUnitConfig]):
    def __init__(self, spec: LongTermMemoryUnitConfig = None, **kwargs):
        super().__init__(**kwargs)
        self.spec = spec
        self.mem0: EidolonMem0 = EidolonMem0(spec.llm_unit, spec.db_collection, spec.similarity_memory)

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

    def searchMemories(self, call_context: CallContext, message: LLMMessage, multi_process: bool = False, multi_agent: bool = False):
        query = str(message)
        user_id = AgentOS.current_user().id
        results = self.mem0.search(query, user_id=user_id)
        def filter_func(res):
            try:
                valid = True
                if not multi_process and res.process_id != call_context.process_id:
                    valid = False
                if not multi_agent and res.agent_id != AgentOS.current_agent_name():
                    valid = False
                return valid
            except:
                # assume caused by missing process_id or agent_id fields
                if multi_process and multi_agent:
                    return True
                return False
            
        filtered_results = results.filter(filter_func)
        return filtered_results

    def getAllMemories(self, call_context: CallContext, filter_by_process: bool = True, filter_by_agent: bool = True):
        if filter_by_agent:
            return self.mem0.get_all(agent_id=AgentOS.current_agent_name())
        memories = self.mem0.get_all()
        def filter_func(mem):
            try:
                valid = True
                if filter_by_process and mem.metadata.process_id != call_context.process_id:
                    valid = False
                return valid
            except:
                if filter_by_agent or filter_by_process:
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