from __future__ import annotations

import pathlib
from typing import Dict, Tuple, TypeVar, Type

from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.system import resource_load_error_handler
from eidolon_ai_sdk.system.resource_load_error_handler import register_resource_error, register_resource_promote_error
from eidolon_ai_sdk.system.resources.resources_base import load_resources, Resource

T = TypeVar("T", bound="Resource")  # noqa: F821
S = TypeVar("S", bound="BaseModel")  # noqa: F821


class AgentOSKernel:
    _resources: Dict[str, Dict[str, Tuple["Resource", str]]] = ...  # noqa: F821

    @classmethod
    def _get_or_load_resources(cls) -> Dict[str, Dict[str, Tuple[Resource, str]]]:
        if cls._resources is ...:
            from eidolon_ai_sdk.builtins.code_builtins import named_builtins

            cls._resources = {}
            for resource in named_builtins():
                cls.register_resource(resource, source="builtin")
            for resource, loc in load_resources([pathlib.Path(__file__).parent.parent / "builtins" / "resources"]):
                cls.register_resource(resource, source="builtin")

        return cls._resources

    @classmethod
    def load_machine(cls, machine):
        AgentOS.file_memory = machine.memory.file_memory
        AgentOS.symbolic_memory = machine.memory.symbolic_memory
        AgentOS.similarity_memory = machine.memory.similarity_memory
        AgentOS.security_manager = machine.security_manager
        AgentOS.process_file_system = machine.process_file_system
        resource_load_error_handler.fail_on_agent_start_error = machine.spec.fail_on_agent_start_error

    @classmethod
    def register_resource(cls, resource: Resource, source=None):  # noqa: F821
        try:
            resources = cls._get_or_load_resources()
            if resource.kind not in resources:
                resources[resource.kind] = {}
            bucket = resources[resource.kind]
            if resource.metadata.name in bucket:
                if bucket[resource.metadata.name][1] == "builtin":
                    logger.info(f"Overriding builtin resource '{resource.kind}.{resource.metadata.name}'")
                    old_spec = getattr(bucket[resource.metadata.name][0], "spec", {})
                    old_spec = dict(implementation=old_spec) if isinstance(old_spec, str) else old_spec
                    new_spec = getattr(resource, "spec")
                    new_spec = dict(implementation=new_spec) if isinstance(new_spec, str) else new_spec
                    old_spec.update(new_spec)
                    resource.spec = old_spec
                else:
                    raise ValueError(
                        f"Resource {resource.metadata.name} already registered by {bucket[resource.metadata.name][1]}"
                    )
            logger.debug(f"Registering resource {resource.kind}.{resource.metadata.name}")
            bucket[resource.metadata.name] = (resource, source)
        except Exception as e:
            register_resource_error(resource.metadata.name, resource.kind, e)

    @classmethod
    def get_resources(cls, kind: Type[T]) -> Dict[str, T]:  # noqa: F821
        ret = {}
        for k, tu in cls._get_or_load_resources().get(kind.kind_literal(), {}).items():
            try:
                ret[k] = tu[0].promote(kind)
            except Exception as e:
                register_resource_promote_error(k, kind.__name__, e, tu[1])
        return ret

    @classmethod
    def get_resource_raw(cls, kind: Type[T], name: str) -> Resource:
        return cls._get_or_load_resources()[kind.kind_literal()][name][0]

    @classmethod
    def get_resource(cls, kind: Type[T], name: str, default=...) -> T:
        bucket = kind.kind_literal()
        try:
            return cls.get_resource_raw(kind, name).promote(kind)
        except KeyError:
            if default is not ...:
                return default
            raise ValueError(f"Resource {name} not found in bucket {bucket}")

    @classmethod
    def get_instance(cls, kind: Type[S], **kwargs) -> S:
        from eidolon_ai_sdk.system.reference_model import Reference

        return Reference[kind, kind.__name__]().instantiate(**kwargs)

    @classmethod
    def get_resource_source(cls, bucket, name: str) -> str:
        try:
            return cls._get_or_load_resources()[bucket][name][1]
        except KeyError:
            raise ValueError(f"Resource {name} not found in bucket {bucket}")

    @classmethod
    def reset(cls):
        cls._resources = ...
        AgentOS.file_memory = ...
        AgentOS.symbolic_memory = ...
        AgentOS.similarity_memory = ...
        AgentOS.embedder = ...
