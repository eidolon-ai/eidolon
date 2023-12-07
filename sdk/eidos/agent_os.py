from __future__ import annotations

from typing import Any

from eidos.memory.agent_memory import FileMemory, SymbolicMemory, VectorMemory

_machine: Any = None


class AgentOS:
    @staticmethod
    def machine() -> Any:
        return _machine

    @staticmethod
    def file_memory() -> FileMemory:
        return _machine.memory.file_memory

    @staticmethod
    def symbolic_memory() -> SymbolicMemory:
        return _machine.memory.symbolic_memory

    @staticmethod
    def similarity_memory() -> VectorMemory:
        return _machine.memory.similarity_memory