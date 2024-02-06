from __future__ import annotations

import os

import pathlib
from typing import Dict, Tuple, TypeVar, Type

from eidolon_ai_sdk.system.resources.resources_base import load_resources, Resource
from eidolon_ai_sdk.util.logger import logger

T = TypeVar("T", bound="Resource")  # noqa: F821


class AgentOS:
    _resources: Dict[str, Dict[str, Tuple["Resource", str]]] = ...  # noqa: F821
    file_memory: "FileMemory" = ...  # noqa: F821
    symbolic_memory: "SymbolicMemory" = ...  # noqa: F821
    similarity_memory: "SimilarityMemory" = ...  # noqa: F821
    security_manager: "SecurityManager" = ...  # noqa: F821

    @staticmethod
    def current_machine_url() -> str:
        return os.environ.get("EIDOLON_LOCAL_MACHINE", "http://localhost:8080")

    @classmethod
    def _get_or_load_resources(cls) -> Dict[str, Dict[str, Tuple[Resource, str]]]:
        if cls._resources is ...:
            from eidolon_ai_sdk.builtins.code_builtins import named_builtins

            cls._resources = {}
            for resource in named_builtins():
                cls.register_resource(resource, source="builtin")
            for resource in load_resources(pathlib.Path(__file__).parent / "builtins" / "resources"):
                cls.register_resource(resource, source="builtin")

        return cls._resources

    @classmethod
    def load_machine(cls, machine):
        cls.file_memory = machine.memory.file_memory
        cls.symbolic_memory = machine.memory.symbolic_memory
        cls.similarity_memory = machine.memory.similarity_memory
        cls.security_manager = machine.security_manager

    @classmethod
    def register_resource(cls, resource: Resource, source=None):  # noqa: F821
        resources = cls._get_or_load_resources()
        if resource.kind not in resources:
            resources[resource.kind] = {}
        bucket = resources[resource.kind]
        if resource.metadata.name in bucket:
            if bucket[resource.metadata.name][1] == "builtin":
                logger.info(f"Overriding builtin resource '{resource.kind}.{resource.metadata.name}'")
            else:
                raise ValueError(
                    f"Resource {resource.metadata.name} already registered by {bucket[resource.metadata.name][1]}"
                )
        logger.debug(f"Registering resource {resource.kind}.{resource.metadata.name}")
        bucket[resource.metadata.name] = (resource, source)

    @classmethod
    def get_resources(cls, kind: Type[T]) -> Dict[str, T]:  # noqa: F821
        return {k: tu[0].promote(kind) for k, tu in cls._get_or_load_resources().get(kind.kind_literal(), {}).items()}

    @classmethod
    def get_resource(cls, kind: Type[T], name: str, default=...) -> T:
        bucket = kind.kind_literal()
        try:
            return cls._get_or_load_resources()[bucket][name][0].promote(kind)
        except KeyError:
            if default is not ...:
                return default
            raise ValueError(f"Resource {name} not found in bucket {bucket}")

    @classmethod
    def get_resource_source(cls, bucket, name: str) -> str:
        try:
            return cls._get_or_load_resources()[bucket][name][1]
        except KeyError:
            raise ValueError(f"Resource {name} not found in bucket {bucket}")

    @classmethod
    def reset(cls):
        cls._resources = ...
        cls.file_memory = ...
        cls.symbolic_memory = ...
        cls.similarity_memory = ...
        cls.embedder = ...
