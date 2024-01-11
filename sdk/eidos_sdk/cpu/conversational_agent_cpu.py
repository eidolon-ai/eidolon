from typing import List, Type, Dict, Any, Union, Literal

from fastapi import HTTPException

from eidos_sdk.cpu.agent_cpu import AgentCPU, AgentCPUSpec, Thread
from eidos_sdk.cpu.agent_io import IOUnit, CPUMessageTypes
from eidos_sdk.cpu.call_context import CallContext
from eidos_sdk.cpu.llm_message import LLMMessage, AssistantMessage, ToolResponseMessage
from eidos_sdk.cpu.llm_unit import LLMUnit
from eidos_sdk.cpu.logic_unit import LogicUnit, LLMToolWrapper
from eidos_sdk.cpu.memory_unit import MemoryUnit
from eidos_sdk.cpu.processing_unit import ProcessingUnitLocator, PU_T
from eidos_sdk.system.reference_model import Reference, AnnotatedReference, Specable


class ConversationalAgentCPUSpec(AgentCPUSpec):
    io_unit: AnnotatedReference[IOUnit]
    memory_unit: AnnotatedReference[MemoryUnit]
    llm_unit: AnnotatedReference[LLMUnit]
    logic_units: List[Reference[LogicUnit]] = []


class ConversationalAgentCPU(AgentCPU, Specable[ConversationalAgentCPUSpec], ProcessingUnitLocator):
    io_unit: IOUnit
    memory_unit: MemoryUnit
    logic_units: List[LogicUnit] = None

    def __init__(self, spec: ConversationalAgentCPUSpec = None):
        super().__init__(spec)
        kwargs = dict(processing_unit_locator=self)
        self.io_unit = self.spec.io_unit.instantiate(**kwargs)
        self.memory_unit = self.spec.memory_unit.instantiate(**kwargs)
        self.llm_unit = self.spec.llm_unit.instantiate(**kwargs)
        self.logic_units = [logic_unit.instantiate(**kwargs) for logic_unit in self.spec.logic_units]

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

    async def set_boot_messages(self, call_context: CallContext, boot_messages: List[CPUMessageTypes]):
        conversation_messages = await self.io_unit.process_request(boot_messages)
        await self.memory_unit.storeBootMessages(call_context, conversation_messages)

    async def schedule_request(
        self,
        call_context: CallContext,
        prompts: List[CPUMessageTypes],
        output_format: Union[Literal["str"], Dict[str, Any]] = "str",
    ) -> Any:
        try:
            conversation_messages = await self.io_unit.process_request(prompts)
            conversation = await self.memory_unit.storeAndFetch(call_context, conversation_messages)
            assistant_message = await self._llm_execution_cycle(call_context, conversation, output_format)
            return await self.io_unit.process_response(call_context, assistant_message.content)
        except HTTPException:
            raise
        except Exception as e:
            raise RuntimeError("Error in cpu while processing request") from e

    async def _llm_execution_cycle(
        self,
        call_context: CallContext,
        conversation: List[LLMMessage],
        output_format: Union[Literal["str"], Dict[str, Any]],
    ) -> AssistantMessage:
        num_iterations = 0
        while num_iterations < self.spec.max_num_function_calls:
            tool_defs = await LLMToolWrapper.from_logic_units(self.logic_units, conversation=conversation)
            assistant_message = await self.llm_unit.execute_llm(
                call_context, conversation, [w.llm_message for w in tool_defs.values()], output_format
            )
            await self.memory_unit.storeMessages(call_context, [assistant_message])
            if assistant_message.tool_calls:
                results = []
                for tool_call in assistant_message.tool_calls:
                    tool_def = tool_defs[tool_call.name]
                    tool_result = await tool_def.execute(call_context=call_context, args=tool_call.arguments)
                    # todo, store tool response result as Any (must be json serializable) so that it can be retrieved symmetrically
                    message = ToolResponseMessage(
                        tool_call_id=tool_call.tool_call_id,
                        result=self._to_json(tool_result),
                        name=tool_call.name,
                    )
                    await self.memory_unit.storeMessages(call_context, [message])
                    results.append(message)

                conversation = conversation + [assistant_message] + results
                num_iterations += 1
            else:
                return assistant_message

        raise ValueError(f"Exceeded maximum number of function calls {self.spec.max_num_function_calls}")

    async def main_thread(self, process_id: str) -> Thread:
        return Thread(CallContext(process_id=process_id), self)

    async def new_thread(self, process_id) -> Thread:
        return Thread(CallContext(process_id=process_id).derive_call_context(), self)

    async def clone_thread(self, call_context: CallContext) -> Thread:
        new_context = call_context.derive_call_context()
        messages = await self.memory_unit.getConversationHistory(call_context)
        for m in messages:
            m["thread_id"] = new_context.thread_id
        await self.memory_unit.storeMessages(new_context, messages)
        return Thread(call_context=new_context, cpu=self)
