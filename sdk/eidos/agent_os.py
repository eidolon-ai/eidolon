from __future__ import annotations

from eidos.memory.agent_memory import FileMemory, SymbolicMemory, VectorMemory

_machine: AgentMachine

class AgentOS:
    @staticmethod
    def file_memory() -> FileMemory:
        return _machine.memory.file_memory

    @staticmethod
    def symbolic_memory() -> SymbolicMemory:
        return _machine.memory.symbolic_memory

    @staticmethod
    def similarity_memory() -> VectorMemory:
        return _machine.memory.similarity_memory