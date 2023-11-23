from __future__ import annotations

from typing import Dict

from pydantic import Field, BaseModel

from .agent import Agent
from .agent_memory import FileMemory, SymbolicMemory, SimilarityMemory
from .cpu.agent_cpu import AgentCPU
from .reference_model import Reference
from .util.class_utils import fqn


class MachineModel(BaseModel):
    agent_memory: MemoryModel = Field(description="The Agent Memory to use.")
    agent_programs: Dict[str, ProgramModel] = Field(description="The list of Agent Programs to run on this machine.")


class ProgramModel(BaseModel):
    agent: Reference[Agent] = Field(description="The Agent implementation to use.")
    cpu: Reference[AgentCPU] = Reference(implementation=fqn(AgentCPU))


class MemoryModel(BaseModel):
    symbolic_memory: Reference[SymbolicMemory] = Field(description="The Symbolic Memory implementation.")
    file_memory: Reference[FileMemory] = Field(default=None, description="The File Memory implementation.")
    similarity_memory: Reference[SimilarityMemory] = Field(default=None, description="The Similarity Memory implementation.")
