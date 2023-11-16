from __future__ import annotations

from typing import List

from pydantic import Field, BaseModel

from .agent import Agent
from .agent_memory import FileMemory, SymbolicMemory, SimilarityMemory
from .cpu_model import CpuModel
from .reference_model import Reference


class MachineModel(BaseModel):
    agent_memory: MemoryModel = Field(description="The Agent Memory to use.")
    agent_programs: List[ProgramModel] = Field(description="The list of Agent Programs to run on this machine.")


class ProgramModel(BaseModel):
    name: str = Field(description="The name of the program.")
    agent: Reference[Agent] = Field(description="The Agent implementation to use.")
    cpu: CpuModel = CpuModel()


class MemoryModel(BaseModel):
    symbolic_memory: Reference[SymbolicMemory] = Field(description="The Symbolic Memory implementation.")
    file_memory: Reference[FileMemory] = Field(default=None, description="The File Memory implementation.")
    similarity_memory: Reference[SimilarityMemory] = Field(default=None, description="The Similarity Memory implementation.")
