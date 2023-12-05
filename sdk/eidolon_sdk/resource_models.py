from __future__ import annotations

from typing import List, Literal, Type, Dict, Optional, TypeVar

from pydantic import Field, BaseModel, field_validator, Extra

from .agent import Agent
from .agent_memory import FileMemory, SymbolicMemory, VectorMemory, AgentMemory
from .cpu.agent_cpu import AgentCPUConfig, AgentCPU
from .impl.generic_agent import GenericAgent
from .impl.tot_agent.tot_agent import TreeOfThoughtsAgent
from .reference_model import Reference
from .util.class_utils import fqn


class Metadata(BaseModel):
    name: str
    annotations: List[str] = []
    labels: List[str] = []


T = TypeVar("T", bound=BaseModel)


class Resource(BaseModel, extra=Extra.allow):
    apiVersion: Literal["eidolon/v1"]
    kind: str
    metadata: Metadata = Metadata(name='DEFAULT')
    spec: dict = {}

    @classmethod
    def kind_literal(cls) -> Optional[str]:
        return getattr(cls.model_fields['kind'].annotation, "__args__", [None])[0]

    def promote(self, clazz: Type[T]) -> T:
        return clazz.model_validate(self.model_dump())


class MachineResource(Resource):
    kind: Literal['Machine']
    spec: MachineSpec


class CPUResource(Resource, Reference[AgentCPU]):
    kind: Literal['CPU']
    implementation: str = fqn(AgentCPU)


class AgentResource(Resource, Reference[Agent]):
    kind: Literal['Agent']


def _build_resource(clazz: Type) -> Type[Resource]:
    class CustomResource(Resource, Reference[clazz]):
        kind: str
        implementation: str = fqn(clazz)

        @field_validator('kind')
        def _is_class_name(cls, v):
            if v != clazz.__name__:
                raise ValueError(f"Kind must be {clazz.__name__}")
            return v

        @classmethod
        def kind_literal(cls) -> str:
            return clazz.__name__

    return CustomResource


agent_resources: Dict[str, Type[Resource]] = {r.kind_literal(): r for r in [
    AgentResource,
    _build_resource(GenericAgent),
    _build_resource(TreeOfThoughtsAgent),
]}


class MachineSpec(BaseModel):
    symbolic_memory: Reference[SymbolicMemory] = Field(description="The Symbolic Memory implementation.")
    file_memory: Reference[FileMemory] = Field(default=None, description="The File Memory implementation.")
    similarity_memory: Reference[VectorMemory] = Reference(implementation=fqn(VectorMemory))

    def get_agent_memory(self):
        file_memory = self.file_memory.instantiate()
        symbolic_memory = self.symbolic_memory.instantiate()
        vector_memory = self.similarity_memory.instantiate(file_memory)
        return AgentMemory(file_memory=file_memory, symbolic_memory=symbolic_memory, similarity_memory=vector_memory)
