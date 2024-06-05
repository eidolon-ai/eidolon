from collections import deque, defaultdict
from datetime import datetime
from functools import cache
from typing import Literal

import kubernetes
from kubernetes.client import (
    CoreV1Api,
    ApiException,
    OpenApiException,
    AppsV1Api,
    RbacAuthorizationV1Api,
    StorageV1Api,
    NetworkingV1Api,
)
from pydantic import BaseModel
from pydantic_core import to_jsonable_python

from eidolon_ai_client.events import StringOutputEvent, OutputEvent
from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.apu.logic_unit import LogicUnit, llm_function
from eidolon_ai_sdk.system.reference_model import Specable


class K8LogicUnitSpec(BaseModel):
    safety_level: Literal["read_only", "no_mutations", "unrestricted"] = "no_mutations"
    condense_output: bool = True
    soft_character_limit: int = 16000


class K8LogicUnit(Specable[K8LogicUnitSpec], LogicUnit):
    loaded = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not K8LogicUnit.loaded:
            kubernetes.config.load_kube_config()
            K8LogicUnit.loaded = True
        for api in [CoreV1Api, AppsV1Api, NetworkingV1Api, StorageV1Api, RbacAuthorizationV1Api]:
            description = (
                f"This tool gives access to query and modify a kubernetes cluster.\n"
                f"It is a wrapper around kubernetes.client.api.\n"
                f"It will call functions on the {api.__name__} object and return the results.\n\n"
                'Example:\nfunction_name="list_namespaced_pod", kwargs='
                '\{"namespace": "default", "limit": 20\}\n\n'
                f"When called, this tool will execute the following logic: getattr({api.__name__}(), function_name)(**kwargs)"
            )
            setattr(
                self,
                api.__name__,
                llm_function(name=api.__name__, description=description)(K8LogicUnit._tool_builder(api)),
            )

    @staticmethod
    def _tool_builder(api):
        async def _tool_fn(self, function_name: str, kwargs: dict = None):
            """
            This tool gives access to query and modify a kubernetes cluster.
            It is a wrapper around kubernetes.client.CoreV1Api.
            It will call functions on the CoreV1Api object and return the results.

            Example:
                function_name="list_namespaced_pod", kwargs={"namespace": "default", "limit": 20}

            When called, this tool will execute the following logic: getattr(CoreV1Api(), function_name)(**kwargs)
            """
            fn = function_name
            kwargs = kwargs or {}

            self.check_args(api, fn, kwargs)

            api_instance = api()
            try:
                resp = getattr(api_instance, fn)(**kwargs)
            except OpenApiException as e:
                if not isinstance(e, ApiException):
                    # give agent some more information on the endpoint if they are calling it improperly
                    yield StringOutputEvent(content=f"{fn} docs:\n" + getattr(api_instance, fn).__doc__)
                raise e
            resp = to_jsonable_python(resp.to_dict())
            if self.spec.condense_output:
                resp = _condense(resp)
            limited = False
            if self.spec.soft_character_limit and 0 < self.spec.soft_character_limit < len(str(resp)):
                limited = _limit_obj(resp, self.spec.soft_character_limit)

            content = dict(request_time_iso=datetime.now().isoformat(), response=resp)
            if limited:
                content[
                    "extra"
                ] = "Portions of the response were too large and were replaced with '...'. Request specific resources for more details"
            yield OutputEvent.get(content=content)

        return _tool_fn

    def check_args(self, api, fn, kwargs):
        if fn.startswith("_"):
            raise ValueError("Private functions are not allowed")
        if fn.startswith("_"):
            raise ValueError("Private functions are not allowed")
        if not hasattr(api, fn) or not callable(getattr(api, fn)):
            raise ValueError(f"Function {fn} is not recognized")
        is_safe = fn in K8LogicUnit.safe_operations(api)
        is_dangerous = fn in K8LogicUnit.dangerous_operations(api)
        is_safe_with_dry_run = fn in K8LogicUnit.safe_with_dry_run(api)
        if not (is_safe or is_dangerous or is_safe_with_dry_run):
            if self.spec.safety_level == "unrestricted":
                logger.warning(f"Function {fn} is not recognized")
            else:
                raise ValueError(f"Function {fn} is not recognized")

        if self.spec.safety_level == "read_only":
            if fn not in K8LogicUnit.safe_operations(api):
                raise ValueError(f"Cannot perform {fn} with current safety level {self.spec.safety_level}")
        elif self.spec.safety_level == "no_mutations":
            if is_dangerous:
                raise ValueError(f"Cannot perform {fn} with current safety level {self.spec.safety_level}")
            elif is_safe_with_dry_run and kwargs.get("dry_run") != "All":
                raise ValueError(
                    f"Must set dry_run='All' to perform {fn} with current safety level {self.spec.safety_level}"
                )

    @staticmethod
    @cache
    def _operations(api):
        return [(f, getattr(api, f)) for f in dir(api) if not f.startswith("_") and callable(getattr(api, f))]

    @staticmethod
    @cache
    def safe_operations(api=CoreV1Api):
        return {
            o
            for o, f in K8LogicUnit._operations(api)
            if o.startswith("list") or o.startswith("read") or o.startswith("get")
        }

    @staticmethod
    @cache
    def safe_with_dry_run(api=CoreV1Api):
        return {
            o
            for o, f in K8LogicUnit._operations(api)
            if o.startswith("create") or o.startswith("replace") or o.startswith("patch") or o.startswith("delete")
        }

    @staticmethod
    @cache
    def dangerous_operations(api=CoreV1Api):
        return {o for o, f in K8LogicUnit._operations(api) if o.startswith("connect")}


def _condense(obj):
    if isinstance(obj, dict):
        acc = {}
        for k, v in obj.items():
            new_v = _condense(v)
            if new_v or new_v is False:
                acc[k] = _condense(v)
        return acc
    elif isinstance(obj, list):
        acc = []
        for v in obj:
            new_v = _condense(v)
            if new_v or new_v is False:
                acc.append(new_v)
        return acc
    else:
        return obj


def _limit_obj(obj, limit):
    """
    Takes a jsonable python object and prunes depth at a limit near json string representation.
    1. iterate by breadth, counting contents to see which level pops us over the limit.
    2. rebuild object to that level, replacing further nested objects with "..."
    """
    counter = 0
    acc = deque([(obj, 0)])
    level_acc = defaultdict(list)
    while acc and counter < limit:
        v, level = acc.popleft()
        level_acc[level].append(v)
        if isinstance(v, dict):
            counter += 2
            for k, v in v.items():
                counter += len(str(k)) + 2
                acc.append((v, level + 1))
        elif isinstance(v, list):
            counter += 2
            for v in v:
                counter += 2
                acc.append((v, level + 1))
        elif isinstance(v, str):
            counter += len(v) + 2
        else:
            counter += len(str(v))

    if counter > limit:
        over_level = max(level_acc.keys())
        desired_level = max(0, over_level - 1)
        for v in level_acc[desired_level] if desired_level >= 0 else []:
            if isinstance(v, dict):
                for k in v.keys():
                    v[k] = "..."
            elif isinstance(v, list):
                v.clear()
                v.append("...")
    return counter > limit
