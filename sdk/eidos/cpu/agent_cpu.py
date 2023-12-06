from __future__ import annotations

import contextvars
import json
from typing import Any, List, Dict, Type

from fastapi import HTTPException
from pydantic import BaseModel, Field

from eidos.cpu.agent_io import IOUnit, CPUMessageTypes
from eidos.cpu.call_context import CallContext
from eidos.cpu.conversation_memory_unit import ConversationalMemoryUnit
from eidos.cpu.llm.open_ai_llm_unit import OpenAIGPT
from eidos.cpu.llm_message import LLMMessage, ToolResponseMessage, AssistantMessage
from eidos.cpu.llm_unit import LLMUnit
from eidos.cpu.logic_unit import ToolDefType, LogicUnit
from eidos.cpu.memory_unit import MemoryUnit
from eidos.cpu.processing_unit import ProcessingUnitLocator, PU_T
from eidos.system.reference_model import Specable, Reference
from eidos.util.class_utils import fqn


class AgentCPUConfig(BaseModel):
    io_unit: Reference[IOUnit] = Reference(implementation=fqn(IOUnit))
    memory_unit: Reference[MemoryUnit] = Reference(implementation=fqn(ConversationalMemoryUnit))
    llm_unit: Reference[LLMUnit] = Reference(implementation=fqn(OpenAIGPT))
    logic_units: List[Reference[LogicUnit]] = []

    max_num_function_calls: int = Field(10, description="The maximum number of function calls to make in a single request.")


class AgentCPU(ProcessingUnitLocator, Specable[AgentCPUConfig]):
    io_unit: IOUnit
    memory_unit: MemoryUnit
    logic_units: List[LogicUnit] = None,
    process_id: contextvars.ContextVar

    def __init__(self, spec: AgentCPUConfig = None):
        super().__init__(spec)
        self.tool_defs = None
        kwargs = dict(processing_unit_locator=self)
        self.io_unit = self.spec.io_unit.instantiate(**kwargs)
        self.memory_unit = self.spec.memory_unit.instantiate(**kwargs)
        self.llm_unit = self.spec.llm_unit.instantiate(**kwargs)
        self.logic_units = [logic_unit.instantiate(**kwargs) for logic_unit in self.spec.logic_units]
        self.process_id = contextvars.ContextVar('process_id', default=None)

    def locate_unit(self, unit_type: Type[PU_T]) -> PU_T:
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

    async def set_boot_messages(
            self,
            call_context: CallContext,
            boot_messages: List[CPUMessageTypes]
    ):
        await self.memory_unit.storeBootMessages(call_context, boot_messages)

    async def schedule_request(
            self,
            call_context: CallContext,
            prompts: List[CPUMessageTypes],
            output_format: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        output_format = output_format or dict(type="str")
        try:
            conversation_message = await self.io_unit.process_request(prompts)
            conversation = await self.memory_unit.storeAndFetch(call_context, [conversation_message])
            assistant_message = await self._llm_execution_cycle(call_context, conversation, output_format)
            return await self.io_unit.process_response(call_context, assistant_message.content)
        except HTTPException:
            raise
        except Exception as e:
            raise RuntimeError("Error in cpu while processing request") from e

    async def get_tools(self, conversation) -> Dict[str, ToolDefType]:
        self.tool_defs = {}
        for logic_unit in self.logic_units:
            self.tool_defs.update(await logic_unit.build_tools(conversation))
        return self.tool_defs

    def _to_json(self, obj):
        if obj is None:
            return ""
        elif isinstance(obj, BaseModel):
            return obj.model_dump_json()
        elif isinstance(obj, list):
            return "[" + (",".join([self._to_json(o) for o in obj])) + "]"
        else:
            return json.dumps(obj)

    async def _llm_execution_cycle(self, call_context: CallContext, conversation: List[LLMMessage], output_format: Dict[str, Any]) -> AssistantMessage:
        num_iterations = 0
        while num_iterations < self.spec.max_num_function_calls:
            tool_defs = await self.get_tools(conversation)
            assistant_message = await self.llm_unit.execute_llm(call_context, conversation, list(tool_defs.values()), output_format)
            await self.memory_unit.storeMessages(call_context, [assistant_message])
            if assistant_message.tool_calls:
                results = []
                for tool_call in assistant_message.tool_calls:
                    print("executing tool " + tool_call.name + " with args " + str(tool_call.arguments))
                    tool_def = tool_defs[tool_call.name]
                    tool_result = await tool_def.execute(call_context=call_context, args=tool_call.arguments)
                    # todo, store tool response result as Any (must be json serializable) so that it can be retrieved symmetrically
                    message = ToolResponseMessage(tool_call_id=tool_call.tool_call_id, result=self._to_json(tool_result), name=tool_call.name)
                    await self.memory_unit.storeMessages(call_context, [message])
                    results.append(message)

                conversation = conversation + [assistant_message] + results
                num_iterations += 1
            else:
                return assistant_message

        raise ValueError(f"Exceeded maximum number of function calls {self.spec.max_num_function_calls}")

    @property
    def main_thread(self) -> Thread:
        return Thread(CallContext(process_id=self.process_id.get()), self)

    @property
    def new_thread(self) -> Thread:
        return Thread(CallContext(process_id=self.process_id.get()).derive_call_context(), self)


class Thread:
    _call_context: CallContext
    _cpu: AgentCPU

    def __init__(self, call_context: CallContext, cpu: AgentCPU):
        self._call_context = call_context
        self._cpu = cpu

    async def set_boot_messages(self, *prompts: CPUMessageTypes):
        return await self._cpu.set_boot_messages(self._call_context, list(prompts))

    async def schedule_request(self, prompts: List[CPUMessageTypes], output_format: Dict[str, Any] = None) -> Dict[str, Any]:
        return await self._cpu.schedule_request(self._call_context, prompts, output_format)

    async def clone(self) -> Thread:
        new_context = self._call_context.derive_call_context()
        messages = await self._cpu.memory_unit.getConversationHistory(self._call_context)
        for m in messages:
            m['thread_id'] = new_context.thread_id
        await self._cpu.memory_unit.storeMessages(new_context, messages)
        return Thread(call_context=new_context, cpu=self._cpu)
