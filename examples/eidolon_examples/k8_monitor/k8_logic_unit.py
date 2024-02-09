from typing import Literal

import kubernetes
from kubernetes.client import CoreV1Api
from pydantic import BaseModel
from pydantic_core import to_jsonable_python

from eidolon_ai_sdk.cpu.logic_unit import LogicUnit, llm_function
from eidolon_ai_sdk.io.events import StringOutputEvent, ObjectOutputEvent
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.util.logger import logger
from eidolon_examples.k8_monitor.k8_function_groups import safe_operations, dangerous_operations, safe_with_dry_run


class K8LogicUnitSpec(BaseModel):
    safety_level: Literal["read_only", "no_mutations", "unrestricted"] = "no_mutations"


class K8LogicUnit(Specable[K8LogicUnitSpec], LogicUnit):
    _client: CoreV1Api = None

    def client(self):
        if not self._client:
            kubernetes.config.load_kube_config()
            self._client = CoreV1Api()
        return self._client

    @llm_function()
    async def core_v1_api(self, function_name: str, kwargs: dict = None):
        """
        This function is a wrapper around kubernetes.client.CoreV1Api. It will call functions on the CoreV1Api object
        and return the results. For example, to list pods function_name would be "list_namespaced_pod" and kwargs may be
        {"namespace": "default", "limit": 20}

        impl: getattr(self.client(), function_name)(**kwargs)
        """
        kwargs = kwargs or {}
        if function_name.startswith("_"):
            raise ValueError("Private functions are not allowed")
        bad_keys = ["async_req", "watch"]
        for key in bad_keys:
            if key in kwargs:
                del kwargs[key]

        if (
            function_name not in safe_operations
            and function_name not in dangerous_operations
            and function_name not in safe_with_dry_run
        ):
            if self.spec.safety_level == "unrestricted":
                logger.warning(f"Function {function_name} is not recognized")
            else:
                raise ValueError(f"Function {function_name} is not recognized")

        if self.spec.safety_level == "read_only":
            if function_name not in safe_operations:
                raise ValueError(f"Cannot perform {function_name} with current safety level {self.spec.safety_level}")
        elif self.spec.safety_level == "no_mutations":
            if function_name in dangerous_operations:
                raise ValueError(f"Cannot perform {function_name} with current safety level {self.spec.safety_level}")
            elif function_name in safe_with_dry_run and kwargs.get("dry_run") != "All":
                raise ValueError(
                    f"Must set dry_run='All' to perform {function_name} with current safety level {self.spec.safety_level}"
                )

        resp = getattr(self.client(), function_name)(**kwargs)
        try:
            yield ObjectOutputEvent(content=to_jsonable_python(resp))
        except Exception:
            yield StringOutputEvent(content=str(resp))

    # @llm_function()
    async def help(self, function_name: str):
        """
        This function is a wrapper around kubernetes.client.CoreV1Api. It will call functions on the CoreV1Api object
        and return the results.

        impl: getattr(self.client(), function_name).__doc__
        """
        return getattr(self.client(), function_name).__doc__

    # @llm_function()
    async def list_functions(self):
        """
        This function will list the functions that are available to be called on the CoreV1Api object.

        impl: dir(CoreV1Api)
        """
        return [f for f in dir(CoreV1Api) if not f.startswith("_")]
