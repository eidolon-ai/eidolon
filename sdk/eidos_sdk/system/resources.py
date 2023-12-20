from __future__ import annotations

from typing import Literal, Type, Dict, ClassVar, List, Tuple

from pydantic import BaseModel, Field

from eidos_sdk.agent.generic_agent import GenericAgent
from eidos_sdk.agent.tot_agent.tot_agent import TreeOfThoughtsAgent
from eidos_sdk.memory.agent_memory import (
    FileMemory,
    SymbolicMemory,
    AgentMemory,
    VectorMemory,
)
from eidos_sdk.memory.local_file_memory import LocalFileMemory, LocalFileMemoryConfig
from eidos_sdk.memory.mongo_symbolic_memory import MongoSymbolicMemory, MongoSymbolicMemoryConfig
from eidos_sdk.memory.noop_memory import NoopVectorMemory
from eidos_sdk.system.reference_model import Reference, AnnotatedReference
from eidos_sdk.system.resources_base import Resource, Metadata


class MachineSpec(BaseModel):
    symbolic_memory: AnnotatedReference[SymbolicMemory, MongoSymbolicMemory] = Field(
        description="The Symbolic Memory implementation."
    )
    file_memory: AnnotatedReference[FileMemory, LocalFileMemory] = Field(desciption="The File Memory implementation.")
    similarity_memory: AnnotatedReference[VectorMemory, NoopVectorMemory] = Field(
        description="The Vector Memory implementation."
    )

    def get_agent_memory(self):
        file_memory = self.file_memory.instantiate()
        symbolic_memory = self.symbolic_memory.instantiate()
        vector_memory = self.similarity_memory.instantiate(file_memory)
        return AgentMemory(
            file_memory=file_memory,
            symbolic_memory=symbolic_memory,
            similarity_memory=vector_memory,
        )


class MachineResource(Resource):
    kind: Literal["Machine"]
    spec: MachineSpec = MachineSpec()


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

builtin_resources: List[Tuple[Resource, str]] = [
    (r, "builtin")
    for r in [
        MachineResource(
            apiVersion="eidolon/v1",
            kind="Machine",
            metadata=Metadata(name="DEFAULT"),
            spec=MachineSpec(
                symbolic_memory=Reference[MongoSymbolicMemory](
                    spec=MongoSymbolicMemoryConfig(mongo_database_name="eidos").model_dump()
                ),
                file_memory=Reference[LocalFileMemory](
                    spec=LocalFileMemoryConfig(root_dir="/tmp/eidos/file_memory").model_dump()
                ),
                similarity_memory=Reference[NoopVectorMemory](),
            ),
        ),
        MachineResource(
            apiVersion="eidolon/v1",
            kind="Machine",
            metadata=Metadata(name="local_dev"),
            spec=MachineSpec(
                symbolic_memory=Reference[MongoSymbolicMemory](
                    spec=MongoSymbolicMemoryConfig(mongo_database_name="eidos").model_dump()
                ),
                file_memory=Reference[LocalFileMemory](
                    spec=LocalFileMemoryConfig(root_dir="/tmp/eidos/file_memory").model_dump()
                ),
                similarity_memory=Reference[NoopVectorMemory](),
            ),
        ),
    ]
]
