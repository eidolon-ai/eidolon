from typing import Literal

import kubernetes
from kubernetes.client import CoreV1Api, ApiException, OpenApiException
from pydantic import BaseModel
from pydantic_core import to_jsonable_python

from eidolon_ai_sdk.cpu.logic_unit import LogicUnit, llm_function
from eidolon_ai_sdk.io.events import StringOutputEvent, OutputEvent
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
    async def core_v1_api(self, core_v1_api_function_name: str, kwargs: dict = None):
        """
        This function is a wrapper around kubernetes.client.CoreV1Api. It will call functions on the CoreV1Api object
        and return the results. For example, to list pods core_v1_api_function_name would be "list_namespaced_pod" and
        kwargs may be {"namespace": "default", "limit": 20}

        impl: getattr(self.client(), core_v1_api_function_name)(**kwargs)
        """
        fn = core_v1_api_function_name
        kwargs = kwargs or {}

        self.check_args(fn, kwargs)

        try:
            resp = getattr(self.client(), fn)(**kwargs)
        except OpenApiException as e:
            if not isinstance(e, ApiException):
                # give agent some more information on the endpoint if they are calling it improperly
                yield StringOutputEvent(content=getattr(self.client(), core_v1_api_function_name).__doc__)
            raise e
        yield OutputEvent.get(content=(to_jsonable_python(resp, fallback=str)))

    def check_args(self, fn, kwargs):
        if fn.startswith("_"):
            raise ValueError("Private functions are not allowed")
        if fn.startswith("_"):
            raise ValueError("Private functions are not allowed")
        if not hasattr(self.client(), fn) or not callable(getattr(self.client(), fn)):
            raise ValueError(f"Function {fn} is not recognized")
        is_safe = fn in safe_operations
        is_dangerous = fn in dangerous_operations
        is_safe_with_dry_run = fn in safe_with_dry_run
        if not (is_safe or is_dangerous or is_safe_with_dry_run):
            if self.spec.safety_level == "unrestricted":
                logger.warning(f"Function {fn} is not recognized")
            else:
                raise ValueError(f"Function {fn} is not recognized")

        if self.spec.safety_level == "read_only":
            if fn not in safe_operations:
                raise ValueError(f"Cannot perform {fn} with current safety level {self.spec.safety_level}")
        elif self.spec.safety_level == "no_mutations":
            if is_dangerous:
                raise ValueError(f"Cannot perform {fn} with current safety level {self.spec.safety_level}")
            elif is_safe_with_dry_run and kwargs.get("dry_run") != "All":
                raise ValueError(
                    f"Must set dry_run='All' to perform {fn} with current safety level {self.spec.safety_level}"
                )
