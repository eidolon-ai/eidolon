from __future__ import annotations

from typing import Literal, Type, Dict, ClassVar

from pydantic import BaseModel, Field

from eidos.agent.generic_agent import GenericAgent
from eidos.agent.tot_agent.tot_agent import TreeOfThoughtsAgent
from eidos.cpu.agent_cpu import AgentCPU
from eidos.cpu.conversational_agent_cpu import ConversationalAgentCPU
from eidos.memory.agent_memory import (
    FileMemory,
    SymbolicMemory,
    VectorMemory,
    AgentMemory,
)
from eidos.memory.local_file_memory import LocalFileMemory
from eidos.memory.mongo_symbolic_memory import MongoSymbolicMemory
from eidos.system.reference_model import Reference, AnnotatedReference
from eidos.system.resources_base import Resource


class MachineResource(Resource):
    kind: Literal["Machine"]
    spec: MachineSpec


class CPUResource(Resource, Reference[AgentCPU, ConversationalAgentCPU]):
    kind: Literal["CPU"]


class AgentResource(Resource, Reference):
    kind: Literal["Agent"] = "Agent"


def _build_resource(clazz_: Type) -> Type[Resource]:
    class AutoAgentResource(Resource, Reference[clazz_, clazz_]):
        clazz: ClassVar[Type] = clazz_

        @classmethod
        def kind_literal(cls) -> str:
            return cls.clazz.__name__

    return AutoAgentResource


agent_resources: Dict[str, Type[Resource]] = {
    r.kind_literal(): r
    for r in [
        AgentResource,
        _build_resource(GenericAgent),
        _build_resource(TreeOfThoughtsAgent),
    ]
}


class MachineSpec(BaseModel):
    symbolic_memory: Reference[SymbolicMemory, MongoSymbolicMemory] = Field(
        description="The Symbolic Memory implementation."
    )
    file_memory: Reference[FileMemory, LocalFileMemory] = Field(desciption="The File Memory implementation.")
    similarity_memory: AnnotatedReference[VectorMemory]

    def get_agent_memory(self):
        file_memory = self.file_memory.instantiate()
        symbolic_memory = self.symbolic_memory.instantiate()
        vector_memory = self.similarity_memory.instantiate(file_memory)
        return AgentMemory(
            file_memory=file_memory,
            symbolic_memory=symbolic_memory,
            similarity_memory=vector_memory,
        )
