from __future__ import annotations

import json
from abc import abstractmethod, ABC
from typing import Any, List, Dict, Literal, Union

from pydantic import BaseModel, Field

from eidos.cpu.agent_io import CPUMessageTypes
from eidos.cpu.call_context import CallContext
from eidos.system.reference_model import Specable


class AgentCPUSpec(BaseModel):
    max_num_function_calls: int = Field(
        10,
        description="The maximum number of function calls to make in a single request.",
    )


class AgentCPU(Specable[AgentCPUSpec], ABC):
    @abstractmethod
    async def set_boot_messages(
        self,
        call_context: CallContext,
        boot_messages: List[CPUMessageTypes],
        output_format: Union[Literal["str"], Dict[str, Any]],
    ):
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


class Thread:
    _call_context: CallContext
    _cpu: AgentCPU

    def __init__(self, call_context: CallContext, cpu: AgentCPU):
        self._call_context = call_context
        self._cpu = cpu

    async def set_boot_messages(
        self,
        output_format: Union[Literal["str"], Dict[str, Any]],
        *prompts: CPUMessageTypes,
    ):
        return await self._cpu.set_boot_messages(self._call_context, list(prompts), output_format)

    async def schedule_request(
        self,
        prompts: List[CPUMessageTypes],
        output_format: Union[Literal["str"], Dict[str, Any]],
    ) -> Any:
        return await self._cpu.schedule_request(self._call_context, prompts, output_format)

    async def clone(self) -> Thread:
        return await self._cpu.clone_thread(self._call_context)
