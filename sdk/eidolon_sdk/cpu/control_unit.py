import json
from abc import ABC
from dataclasses import dataclass
from typing import List, Union, Dict, Any, Type

from bson import ObjectId
from pydantic import BaseModel, Field

from eidolon_sdk.cpu.agent_bus import CallContext
from eidolon_sdk.cpu.agent_io import UserTextCPUMessage, ImageURLCPUMessage, SystemCPUMessage, IOUnit
from eidolon_sdk.cpu.llm_message import ToolResponseMessage, LLMMessage
from eidolon_sdk.cpu.llm_unit import LLMUnit, LLMCallFunction
from eidolon_sdk.cpu.logic_unit import LogicUnit, MethodInfo, ToolDefType
from eidolon_sdk.cpu.memory_unit import MemoryUnit
from eidolon_sdk.cpu.processing_unit import ProcessingUnit, T
from eidolon_sdk.reference_model import Specable


class ControlUnitConfig(BaseModel):
    max_num_function_calls: int = Field(10, description="The maximum number of function calls to make in a single request.")



class ControlUnit(ProcessingUnit, Specable[ControlUnitConfig], ABC):
    io_unit: IOUnit
    memory_unit: MemoryUnit
    llm_unit: LLMUnit
    logic_units: List[LogicUnit]
    tool_defs: Dict[str, ToolDefType] = None

    def __init__(self,
                 io_unit: IOUnit,
                 memory_unit: MemoryUnit,
                 llm_unit: LLMUnit,
                 logic_units: List[LLMUnit] = None,
                 spec: ControlUnitConfig = None, **kwargs):
        super().__init__(**kwargs)
        self.spec = spec
        self.io_unit = io_unit
        self.memory_unit = memory_unit
        self.llm_unit = llm_unit
        self.logic_units = logic_units or []

    def locate_unit(self, unit_type: Type[T]) -> T:
        for unit in self.logic_units:
            if isinstance(unit, unit_type):
                return unit
        if isinstance(self.io_unit, unit_type):
            return self.io_unit

        if isinstance(self.memory_unit, unit_type):
            return self.memory_unit

        if isinstance(self.llm_unit, unit_type):
            return self.llm_unit

        raise ValueError(f"Could not locate {unit_type}")

    def get_tools(self, conversation) -> Dict[str, ToolDefType]:
        self.tool_defs = {}
        for logic_unit in self.logic_units:
            self.tool_defs.update(logic_unit.build_tools(conversation))
        return self.tool_defs

    async def process_request(self, process_id: str, prompts: List[Union[UserTextCPUMessage, ImageURLCPUMessage, SystemCPUMessage]], input_data: Dict[str, Any],
                              output_format: Dict[str, Any]):
        call_context = CallContext(process_id=process_id, thread_id=None)
        transformed_messages = await self.io_unit.process_request(call_context, prompts, input_data)
        conversation = await self.memory_unit.processStoreAndFetchEvent(call_context, transformed_messages)
        assistant_message = await self.process_llm_requests(call_context, conversation, output_format)
        response = await self.io_unit.process_response(call_context, assistant_message.content)
        return response

    async def process_llm_requests(self, call_context: CallContext, conversation: List[LLMMessage], output_format: Dict[str, Any]):
        num_iterations = 0
        while num_iterations < self.spec.max_num_function_calls:
            tool_defs = self.get_tools(conversation)
            tool_list = [d.llm_call_function for d in tool_defs.values()]
            assistant_message = await self.llm_unit.execute_llm(call_context, conversation, tool_list, output_format)
            await self.memory_unit.processStoreEvent(call_context, [assistant_message])
            if assistant_message.tool_calls:
                results = []
                for tool_call in assistant_message.tool_calls:
                    tool_def = tool_defs[tool_call.name]
                    tool_result = await tool_def.logic_unit._execute(call_context=call_context, method_info=tool_def.method_info, args=tool_call.arguments)
                    message = ToolResponseMessage(tool_call_id=tool_call.tool_call_id, result=json.dumps(tool_result))
                    await self.memory_unit.processStoreEvent(call_context, [message])
                    results.append(message)

                conversation = conversation + [assistant_message] + results
                num_iterations += 1
            else:
                return assistant_message

        raise ValueError(f"Exceeded maximum number of function calls {self.spec.max_num_function_calls}")
