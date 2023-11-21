from abc import ABC

from bson import ObjectId

from eidolon_sdk.agent_memory import AgentMemory
from eidolon_sdk.cpu.agent_bus import CallContext


class ProcessingUnit(ABC):
    agent_memory: AgentMemory

    def __init__(self, memory: AgentMemory, **kwargs):
        self.agent_memory = memory

    def derive_call_context(self, existing_call_context):
        return CallContext(process_id=existing_call_context.process_id, thread_id=str(ObjectId()))
