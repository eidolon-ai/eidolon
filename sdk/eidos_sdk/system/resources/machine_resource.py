from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from eidos_sdk.memory.agent_memory import (
    FileMemory,
    SymbolicMemory,
    AgentMemory,
)
from eidos_sdk.memory.local_file_memory import LocalFileMemory
from eidos_sdk.memory.mongo_symbolic_memory import MongoSymbolicMemory
from eidos_sdk.memory.similarity_memory import SimilarityMemory
from eidos_sdk.system.reference_model import AnnotatedReference
from eidos_sdk.system.resources.resources_base import Resource


class MachineSpec(BaseModel):
    symbolic_memory: AnnotatedReference[SymbolicMemory, MongoSymbolicMemory] = Field(
        description="The Symbolic Memory implementation."
    )
    file_memory: AnnotatedReference[FileMemory, LocalFileMemory] = Field(desciption="The File Memory implementation.")
    similarity_memory: AnnotatedReference[SimilarityMemory] = Field(description="The Vector Memory implementation.")

    def get_agent_memory(self):
        file_memory = self.file_memory.instantiate()
        symbolic_memory = self.symbolic_memory.instantiate()
        vector_memory = self.similarity_memory.instantiate()
        return AgentMemory(
            file_memory=file_memory,
            symbolic_memory=symbolic_memory,
            similarity_memory=vector_memory,
        )


class MachineResource(Resource):
    kind: Literal["Machine"] = "Machine"
    spec: MachineSpec = MachineSpec()
