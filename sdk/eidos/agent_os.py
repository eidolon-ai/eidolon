from __future__ import annotations

from typing import Dict, Tuple


class AgentOS:
    _resources: Dict[str, Dict[str, Tuple["Resource", str]]] = {}
    file_memory: "FileMemory" = ...
    symbolic_memory: "SymbolicMemory" = ...
    similarity_memory: "VectorMemory" = ...

    @classmethod
    def load_machine(cls, machine):
        cls.file_memory = machine.memory.file_memory
        cls.symbolic_memory = machine.memory.symbolic_memory
        cls.similarity_memory = machine.memory.similarity_memory

    @classmethod
    def register_resource(cls, resource: "Resource", source=None):
        if resource.kind not in cls._resources:
            cls._resources[resource.kind] = {}
        bucket = cls._resources[resource.kind]
        if resource.metadata.name in bucket:
            raise ValueError(
                f"Resource {resource.metadata.name} already registered by {bucket[resource.metadata.name][1]}"
            )
        bucket[resource.metadata.name] = (resource, source)

    @classmethod
    def get_resources(cls, bucket) -> Dict[str, "Resource"]:
        return {k: tu[0].model_copy() for k, tu in cls._resources.get(bucket, {}).items()}

    @classmethod
    def get_resource(cls, bucket: str, name: str = "DEFAULT", default=...) -> "Resource":
        try:
            return cls._resources[bucket][name][0].model_copy(deep=True)
        except KeyError:
            if default is not ...:
                return default
            raise ValueError(f"Resource {name} not found in bucket {bucket}")

    @classmethod
    def get_resource_source(cls, bucket, name: str = "DEFAULT") -> str:
        try:
            return cls._resources[bucket][name][1]
        except KeyError:
            raise ValueError(f"Resource {name} not found in bucket {bucket}")

    @classmethod
    def reset(cls):
        cls._resources = {}
        cls.file_memory = ...
        cls.symbolic_memory = ...
        cls.similarity_memory = ...
