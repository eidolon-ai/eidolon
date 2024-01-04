from __future__ import annotations

from typing import Dict, Tuple, TypeVar, Type

from eidos_sdk.util.logger import logger


T = TypeVar("T", bound="Resource")  # noqa: F821


class AgentOS:
    _resources: Dict[str, Dict[str, Tuple["Resource", str]]] = {}  # noqa: F821
    file_memory: "FileMemory" = ...  # noqa: F821
    symbolic_memory: "SymbolicMemory" = ...  # noqa: F821
    similarity_memory: "SimilarityMemory" = ...  # noqa: F821

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
    def get_resources(cls, kind: Type[T]) -> Dict[str, T]:  # noqa: F821
        return {k: tu[0].promote(kind) for k, tu in cls._resources.get(kind.kind_literal(), {}).items()}

    @classmethod
    def get_resource(cls, kind: Type[T], name: str = "DEFAULT", default=...) -> T:
        bucket = kind.kind_literal()
        try:
            return cls._resources[bucket][name][0].promote(kind)
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
        cls.embedder = ...
