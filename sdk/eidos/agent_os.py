from __future__ import annotations

from eidos.memory.agent_memory import FileMemory, SymbolicMemory, VectorMemory
from eidos.system.agent_machine import AgentMachine

_machine: AgentMachine


@property
def file_memory() -> FileMemory:
    return _machine.memory.file_memory


@property
def symbolic_memory() -> SymbolicMemory:
    return _machine.memory.symbolic_memory


@property
def similarity_memory() -> VectorMemory:
    return _machine.memory.similarity_memory
