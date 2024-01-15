from __future__ import annotations

import json
from abc import abstractmethod, ABC
from typing import Any, List, Dict, Literal, Union, TypeVar, Type

from pydantic import BaseModel, Field, TypeAdapter

from eidos_sdk.cpu.agent_io import CPUMessageTypes
from eidos_sdk.cpu.call_context import CallContext
from eidos_sdk.system.reference_model import Specable


class AgentCPUSpec(BaseModel):
    max_num_function_calls: int = Field(
        10,
        description="The maximum number of function calls to make in a single request.",
    )


class AgentCPU(Specable[AgentCPUSpec], ABC):
    @abstractmethod
    async def set_boot_messages(self, call_context: CallContext, boot_messages: List[CPUMessageTypes]):
        pass

    @abstractmethod
    async def schedule_request(
        self,
        call_context: CallContext,
        prompts: List[CPUMessageTypes],
        output_format: Union[Literal["str"], Dict[str, Any]],
    ) -> Any:
        pass

    def _to_json(self, obj):
        if obj is None:
            return ""
        elif isinstance(obj, BaseModel):
            return obj.model_dump_json()
        elif isinstance(obj, list):
            return "[" + (",".join([self._to_json(o) for o in obj])) + "]"
        else:
            return json.dumps(obj)

    @abstractmethod
    async def main_thread(self, process_id: str) -> Thread:
        pass

    @abstractmethod
    async def new_thread(self, process_id) -> Thread:
        pass

    @abstractmethod
    async def clone_thread(self, call_context: CallContext) -> Thread:
        pass


T = TypeVar("T")


class Thread:
    _call_context: CallContext
    _cpu: AgentCPU

    def __init__(self, call_context: CallContext, cpu: AgentCPU):
        self._call_context = call_context
        self._cpu = cpu

    async def set_boot_messages(
        self,
        prompts: List[CPUMessageTypes],
    ):
        return await self._cpu.set_boot_messages(self._call_context, list(prompts))

    async def schedule_request(
            self,
            prompts: List[CPUMessageTypes],
            output_format: Type[T],
    ) -> T:
        model = TypeAdapter(output_format)
        schema = model.json_schema()
        rtn = await self._cpu.schedule_request(self._call_context, prompts, schema)
        return model.validate_python(rtn)

    async def schedule_request_raw(
            self,
            prompts: List[CPUMessageTypes],
            output_format: Union[Literal["str"], Dict[str, Any]] = "str",
    ) -> Any:
        return await self._cpu.schedule_request(self._call_context, prompts, output_format)

    def call_context(self) -> CallContext:
        return self._call_context

    async def clone(self) -> Thread:
        return await self._cpu.clone_thread(self._call_context)
