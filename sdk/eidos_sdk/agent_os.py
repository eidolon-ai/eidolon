from __future__ import annotations

from typing import Dict, Tuple

from eidos_sdk.util.logger import logger


class AgentOS:
    _resources: Dict[str, Dict[str, Tuple["Resource", str]]] = {}  # noqa: F821
    file_memory: "FileMemory" = ...  # noqa: F821
    symbolic_memory: "SymbolicMemory" = ...  # noqa: F821
    similarity_memory: "VectorMemory" = ...  # noqa: F821

    @classmethod
    def load_machine(cls, machine):
        cls.file_memory = machine.memory.file_memory
        cls.symbolic_memory = machine.memory.symbolic_memory
        cls.similarity_memory = machine.memory.similarity_memory

    @classmethod
    def register_resource(cls, resource: "Resource", source=None):  # noqa: F821
        if resource.kind not in cls._resources:
            cls._resources[resource.kind] = {}
        bucket = cls._resources[resource.kind]
        if resource.metadata.name in bucket:
            if bucket[resource.metadata.name][1] == "builtin":
                logger.info(f"Overriding builtin resource '{resource.kind}.{resource.metadata.name}'")
            else:
                raise ValueError(
                    f"Resource {resource.metadata.name} already registered by {bucket[resource.metadata.name][1]}"
                )
        bucket[resource.metadata.name] = (resource, source)

    @classmethod
    def get_resources(cls, bucket) -> Dict[str, "Resource"]:  # noqa: F821
        return {k: tu[0].model_copy() for k, tu in cls._resources.get(bucket, {}).items()}

    @classmethod
    def get_resource(cls, bucket: str, name: str = "DEFAULT", default=...) -> "Resource":  # noqa: F821
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
