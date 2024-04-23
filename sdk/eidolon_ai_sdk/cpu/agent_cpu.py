from __future__ import annotations

import json
from abc import abstractmethod, ABC
from pydantic import BaseModel, Field, TypeAdapter
from typing import Any, List, Dict, Literal, Union, TypeVar, Type, cast, AsyncIterator

from eidolon_ai_sdk.cpu.agent_io import CPUMessageTypes
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_client.events import StreamEvent, convert_output_object, ObjectOutputEvent, ErrorEvent, StringOutputEvent
from eidolon_ai_sdk.system.reference_model import Specable


class APUCapabilities(BaseModel):
    input_context_limit: int
    output_context_limit: int
    supports_tools: bool
    supports_image_input: bool
    supports_audio_input: bool
    supports_file_search: bool
    supports_image_generation: bool
    supports_audio_generation: bool


class APUSpec(BaseModel):
    max_num_function_calls: int = Field(
        10,
        description="The maximum number of function calls to make in a single request.",
    )


class APU(Specable[APUSpec], ABC):
    title: str

    def __init__(self, spec: T, **kwargs: object):
        super().__init__(spec, **kwargs)
        self.title = "default"

    @abstractmethod
    def get_capabilities(self) -> APUCapabilities:
        pass

    @abstractmethod
    async def set_boot_messages(self, call_context: CallContext, boot_messages: List[CPUMessageTypes]):
        pass

    @abstractmethod
    async def schedule_request(
        self,
        call_context: CallContext,
        prompts: List[CPUMessageTypes],
        output_format: Union[Literal["str"], Dict[str, Any]],
    ) -> AsyncIterator[StreamEvent]:
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

    async def main_thread(self, process_id: str) -> Thread:
        return Thread(CallContext(process_id=process_id), self)

    async def new_thread(self, process_id) -> Thread:
        return Thread(CallContext(process_id=process_id).derive_call_context(), self)

    @abstractmethod
    async def clone_thread(self, call_context: CallContext) -> Thread:
        pass


T = TypeVar("T")


class Thread:
    _call_context: CallContext
    _cpu: APU

    def __init__(self, call_context: CallContext, cpu: APU):
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

        is_string_call = not isinstance(output_format, type) and (
            output_format == "str" or output_format["type"] == "string"
        )
        string_output = ""
        async for event in stream:
            if event.is_root_and_type(ObjectOutputEvent):
                result = event.content
            elif event.is_root_and_type(StringOutputEvent):
                string_output += event.content
            elif event.is_root_and_type(ErrorEvent):
                error = event.reason

        if is_string_call:
            result = string_output

        if error is not None:
            if isinstance(error, Exception):
                raise error
            else:
                raise Exception(error)

        return result

    def stream_request(
        self, prompts: List[CPUMessageTypes], output_format: Union[Literal["str"], Dict[str, Any], Type[T]] = "str"
    ) -> AsyncIterator[StreamEvent]:
        if isinstance(output_format, type):
            model = TypeAdapter(output_format)
            schema = model.json_schema()
            s = convert_output_object(
                self._cpu.schedule_request(self._call_context, prompts, schema), cast(Type[T], output_format)
            )
        else:
            s = self._cpu.schedule_request(self._call_context, prompts, output_format)

        return s

    def call_context(self) -> CallContext:
        return self._call_context

    async def clone(self) -> Thread:
        return await self._cpu.clone_thread(self._call_context)


class APUException(Exception):
    def __init__(self, description):
        super().__init__("CPU Error: " + description)
