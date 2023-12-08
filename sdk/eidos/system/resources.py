from __future__ import annotations

from typing import Literal, Type, Dict

from pydantic import BaseModel, field_validator

from eidos.agent.generic_agent import GenericAgent
from eidos.agent.tot_agent.tot_agent import TreeOfThoughtsAgent
from eidos.cpu.agent_cpu import AgentCPU
from eidos.cpu.conversational_agent_cpu import ConversationalAgentCPU
from eidos.memory.agent_memory import FileMemory, SymbolicMemory, VectorMemory, AgentMemory
from eidos.system.reference_model import Reference
from eidos.system.resources_base import Resource
from eidos.util.class_utils import fqn


class MachineResource(Resource):
    kind: Literal['Machine']
    spec: MachineSpec


class CPUResource(Resource, Reference(AgentCPU, ConversationalAgentCPU, kind='CPU')):
    kind: Literal['CPU']


class AgentResource(Resource, Reference()):
    kind: Literal['Agent']


def _build_resource(clazz: Type) -> Type[Resource]:
    class AutoAgentResource(Resource, Reference()):
        def __init__(self, **kwargs):
            if 'implementation' not in kwargs:
                kwargs['implementation'] = fqn(clazz)
            super().__init__(**kwargs)

        @field_validator('kind')
        def _is_class_name(cls, v):
            if v != clazz.__name__:
                raise ValueError(f"Kind must be {clazz.__name__}")
            return v

        @classmethod
        def kind_literal(cls) -> str:
            return clazz.__name__

    return AutoAgentResource


agent_resources: Dict[str, Type[Resource]] = {r.kind_literal(): r for r in [
    AgentResource,
    _build_resource(GenericAgent),
    _build_resource(TreeOfThoughtsAgent),
]}


class MachineSpec(BaseModel):
    symbolic_memory: Reference(SymbolicMemory, description="The Symbolic Memory implementation.")
    file_memory: Reference(FileMemory, description="The File Memory implementation.")
    similarity_memory: Reference(VectorMemory, default=fqn(VectorMemory))

    def get_agent_memory(self):
        file_memory = self.file_memory.instantiate()
        symbolic_memory = self.symbolic_memory.instantiate()
        vector_memory = self.similarity_memory.instantiate(file_memory)
        return AgentMemory(file_memory=file_memory, symbolic_memory=symbolic_memory, similarity_memory=vector_memory)
