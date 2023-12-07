from __future__ import annotations

from typing import Any

from eidos.memory.agent_memory import FileMemory, SymbolicMemory, VectorMemory

_machine: Any = None


class _AgentOSMeta(type):
    def __getattr__(self, item):
        if item in ['file_memory', 'symbolic_memory', 'similarity_memory']:
            return getattr(_machine.memory, item)
        elif item == 'machine':
            return _machine
        else:
            raise AttributeError(f"Attribute {item} not found on AgentOS")

    def __setattr__(self, key, value):
        pass


class AgentOS(metaclass=_AgentOSMeta):
    machine: Any
    file_memory: FileMemory
    symbolic_memory: SymbolicMemory
    similarity_memory: VectorMemory
