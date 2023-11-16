from __future__ import annotations

from typing import List, Optional

from pydantic import Field, BaseModel

from .agent import Agent
from .agent_memory import FileMemory, SymbolicMemory, SimilarityMemory
from .reference_model import Reference


class MachineModel(BaseModel):
    agent_memory: MemoryModel = Field(description="The Agent Memory to use.")
    agent_programs: List[ProgramReference] = Field(description="The list of Agent Programs to run on this machine.")


class ProgramReference(Reference):
    _sub_class = Agent
    name: Optional[str] = Field(None, description="The name of the program. Will be used as the endpoint name. Default to agent class")


class MemoryModel(BaseModel):
    symbolic_memory: SymbolicMemoryReference = Field(description="The Symbolic Memory implementation.")
    file_memory: FileMemoryReference = Field(default=None, description="The File Memory implementation.")
    similarity_memory: SimilarityMemoryReference = Field(default=None, description="The Similarity Memory implementation.")


class SymbolicMemoryReference(Reference):
    _sub_class = SymbolicMemory


class FileMemoryReference(Reference):
    _sub_class = FileMemory


class SimilarityMemoryReference(Reference):
    _sub_class = SimilarityMemory
