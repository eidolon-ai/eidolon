from __future__ import annotations

from typing import List

from pydantic import Field, BaseModel

from .agent import Agent
from .agent_memory import FileMemory, SymbolicMemory, SimilarityMemory
from .cpu.agent_io import IOUnit
from .cpu.memory_unit import MemoryUnit
from .reference_model import Reference


class MachineModel(BaseModel):
    agent_memory: MemoryModel = Field(description="The Agent Memory to use.")
    agent_programs: List[ProgramModel] = Field(description="The list of Agent Programs to run on this machine.")


class CpuModel(BaseModel):
    memory_unit: Reference[MemoryUnit] = Reference[MemoryUnit](implementation='eidolon_sdk.cpu.memory_unit.MemoryUnit')
    io_unit: Reference[IOUnit] = Reference[IOUnit](implementation='eidolon_sdk.cpu.agent_io.IOUnit')


class ProgramModel(BaseModel):
    name: str = Field(description="The name of the program.")
    agent: Reference[Agent] = Field(description="The Agent implementation to use.")
    cpu: CpuModel = Field(CpuModel(), description="The CPU implementation to use.")


class MemoryModel(BaseModel):
    symbolic_memory: Reference[SymbolicMemory] = Field(description="The Symbolic Memory implementation.")
    file_memory: Reference[FileMemory] = Field(default=None, description="The File Memory implementation.")
    similarity_memory: Reference[SimilarityMemory] = Field(default=None, description="The Similarity Memory implementation.")
