from __future__ import annotations

import json
from abc import abstractmethod, ABC
from pydantic import BaseModel, Field, TypeAdapter
from typing import Any, List, Dict, Literal, Union, TypeVar, Type, cast, AsyncGenerator

from eidos_sdk.cpu.agent_io import CPUMessageTypes
from eidos_sdk.cpu.call_context import CallContext
from eidos_sdk.io.events import StreamEvent, convert_output_object, ObjectOutputEvent, ErrorEvent, StringOutputEvent
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
    ) -> AsyncGenerator[StreamEvent, None]:
        yield None

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

    async def run_request(
            self,
            prompts: List[CPUMessageTypes],
            output_format: Union[Literal["str"], Dict[str, Any], Type[T]] = "str",
    ) -> T:
        stream = self.stream_request(prompts, output_format)
        result = None
        error = None

        string_output = ""
        async for event in stream:
            if len(event.stream_context) == 1 and event.stream_context[0] == self._call_context.process_id:
                if isinstance(event, ObjectOutputEvent):
                    result = event.content
                elif isinstance(event, StringOutputEvent):
                    string_output += event.content
                elif isinstance(event, ErrorEvent):
                    error = event.reason

        if len(string_output) > 0:
            result = string_output

        if error is not None:
            raise error

        return result

    def stream_request(
            self,
            prompts: List[CPUMessageTypes],
            output_format: Union[Literal["str"], Dict[str, Any], Type[T]] = "str"
    ) -> AsyncGenerator[StreamEvent, None]:
        if isinstance(output_format, type):
            model = TypeAdapter(output_format)
            schema = model.json_schema()
            s = convert_output_object(self._cpu.schedule_request(self._call_context, prompts, schema), cast(Type[T], output_format))
        else:
            s = self._cpu.schedule_request(self._call_context, prompts, output_format)

        return s

    def call_context(self) -> CallContext:
        return self._call_context

    async def clone(self) -> Thread:
        return await self._cpu.clone_thread(self._call_context)
