from __future__ import annotations

from typing import List, Literal

from pydantic import Field, BaseModel

from .agent import Agent
from .agent_memory import FileMemory, SymbolicMemory, VectorMemory, AgentMemory
from .reference_model import Reference
from .util.class_utils import fqn


class Metadata(BaseModel):
    name: str
    annotations: List[str] = []
    labels: List[str] = []


class Resource(BaseModel):
    type: str
    metadata: Metadata


class MachineResource(Resource):
    type: Literal['eidolon/machine']
    metadata: Metadata = Metadata(name='DEFAULT')
    spec: MachineSpec


class AgentResource(Resource, Reference[Agent]):
    type: Literal['eidolon/agent']


class MachineSpec(BaseModel):
    symbolic_memory: Reference[SymbolicMemory] = Field(description="The Symbolic Memory implementation.")
    file_memory: Reference[FileMemory] = Field(default=None, description="The File Memory implementation.")
    similarity_memory: Reference[VectorMemory] = Reference(implementation=fqn(VectorMemory))

    def to_agent_memory(self):
        file_memory = self.file_memory.instantiate()
        symbolic_memory = self.symbolic_memory.instantiate()
        vector_memory = self.similarity_memory.instantiate(file_memory)
        return AgentMemory(file_memory=file_memory, symbolic_memory=symbolic_memory, similarity_memory=vector_memory)
