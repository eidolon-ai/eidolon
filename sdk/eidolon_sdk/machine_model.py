from __future__ import annotations

from typing import Dict

from pydantic import Field, BaseModel

from .agent import Agent
from .agent_memory import FileMemory, SymbolicMemory, SimilarityMemory
from .cpu.agent_io import IOUnit
from .cpu.control_unit import ControlUnit, ConversationalControlUnit
from .cpu.llm_unit import LLMUnit, OpenAIGPT
from .cpu.logic_unit import LogicUnit
from .cpu.memory_unit import MemoryUnit, ConversationalMemoryUnit
from .reference_model import Reference
from .util.class_utils import fqn


class MachineModel(BaseModel):
    agent_memory: MemoryModel = Field(description="The Agent Memory to use.")
    agent_programs: Dict[str, ProgramModel] = Field(description="The list of Agent Programs to run on this machine.")


class CpuModel(BaseModel):
    io_unit: Reference[IOUnit] = Reference(implementation=fqn(IOUnit))
    control_unit: Reference[ControlUnit] = Reference(implementation=fqn(ConversationalControlUnit))
    memory_unit: Reference[MemoryUnit] = Reference(implementation=fqn(ConversationalMemoryUnit))
    llm_unit: Reference[LLMUnit] = Reference(implementation=fqn(OpenAIGPT))
    logic_units: Dict[str, Reference[LogicUnit]] = Field(default={})


class ProgramModel(BaseModel):
    agent: Reference[Agent] = Field(description="The Agent implementation to use.")
    cpu: CpuModel = Field(CpuModel(), description="The CPU implementation to use.")


class MemoryModel(BaseModel):
    symbolic_memory: Reference[SymbolicMemory] = Field(description="The Symbolic Memory implementation.")
    file_memory: Reference[FileMemory] = Field(default=None, description="The File Memory implementation.")
    similarity_memory: Reference[SimilarityMemory] = Field(default=None, description="The Similarity Memory implementation.")
