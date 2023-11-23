import json
from typing import Any, Union, List, Dict, Type

from pydantic import BaseModel, Field

from eidolon_sdk.agent_memory import AgentMemory
from eidolon_sdk.cpu.call_context import CallContext
from eidolon_sdk.cpu.agent_io import UserTextCPUMessage, SystemCPUMessage, ImageURLCPUMessage, ResponseHandler, IOUnit
from eidolon_sdk.cpu.llm_message import LLMMessage, ToolResponseMessage
from eidolon_sdk.cpu.llm_unit import LLMUnit
from eidolon_sdk.cpu.logic_unit import MethodInfo, ToolDefType, LogicUnit
from eidolon_sdk.cpu.memory_unit import MemoryUnit
from eidolon_sdk.cpu.processing_unit import ProcessingUnitLocator, PU_T
from eidolon_sdk.impl.conversation_memory_unit import ConversationalMemoryUnit
from eidolon_sdk.impl.open_ai_llm_unit import OpenAIGPT
from eidolon_sdk.reference_model import Specable, Reference
from eidolon_sdk.util.class_utils import fqn


class AgentCPUConfig(BaseModel):
    io_unit: Reference[IOUnit] = Reference(implementation=fqn(IOUnit))
    memory_unit: Reference[MemoryUnit] = Reference(implementation=fqn(ConversationalMemoryUnit))
    llm_unit: Reference[LLMUnit] = Reference(implementation=fqn(OpenAIGPT))
    logic_units: List[Reference[LogicUnit]] = {}

    max_num_function_calls: int = Field(10, description="The maximum number of function calls to make in a single request.")


class AgentCPU(ProcessingUnitLocator, Specable[AgentCPUConfig]):
    io_unit: IOUnit
    memory_unit: MemoryUnit
    logic_units: List[LogicUnit] = None,
    tools: Dict[str, MethodInfo]

    def __init__(
            self,
            agent_memory: AgentMemory,
            spec: AgentCPUConfig = None
    ):
        self.tool_defs = None
        self.agent_memory = agent_memory
        self.spec = spec
        kwargs = dict(agent_memory=agent_memory, processing_unit_locator=self)
        self.io_unit = spec.io_unit.instantiate(**kwargs)
        self.memory_unit = spec.memory_unit.instantiate(**kwargs)
        self.llm_unit = spec.llm_unit.instantiate(**kwargs)
        self.logic_units = [logic_unit.instantiate(**kwargs) for logic_unit in spec.logic_units]

    async def start(self, response_handler: ResponseHandler):
        pass

    async def stop(self):
        pass

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

    async def schedule_request(
            self,
            process_id: str,
            prompts: List[Union[UserTextCPUMessage, ImageURLCPUMessage, SystemCPUMessage]],
            input_data: Dict[str, Any],
            output_format: Dict[str, Any]
    ):
        try:
            call_context = CallContext(process_id=process_id, thread_id=None)
            boot_messages, conversation_message = await self.io_unit.process_request(call_context, prompts, input_data)
            # todo -- change to store in agent memory directly or pass in every time...
            boot_conversation = await self.memory_unit.storeAndFetch(call_context, [conversation_message])
            conversation = await self.memory_unit.storeAndFetch(call_context, [conversation_message])
            assistant_message = await self.process_llm_requests(call_context, boot_conversation, conversation, True, output_format)
            response = await self.io_unit.process_response(call_context, assistant_message.content)
            return response
        except Exception as e:
            raise RuntimeError("Error in control unit while processing request") from e

    async def get_tools(self, conversation) -> Dict[str, ToolDefType]:
        self.tool_defs = {}
        for logic_unit in self.logic_units:
            self.tool_defs.update(await logic_unit.build_tools(conversation))
        return self.tool_defs

    async def process_llm_requests(self, call_context: CallContext, boot_conversation: List[LLMMessage], conversation: List[LLMMessage],
                                   should_store_tool_calls: bool, output_format: Dict[str, Any]):
        full_conversation = boot_conversation + conversation
        num_iterations = 0
        while num_iterations < self.spec.max_num_function_calls:
            tool_defs = await self.get_tools(full_conversation)
            tool_list = [d.llm_call_function for d in tool_defs.values()]
            assistant_message = await self.llm_unit.execute_llm(call_context, full_conversation, tool_list, output_format)
            if should_store_tool_calls:
                await self.memory_unit.storeMessages(call_context, [assistant_message])
            if assistant_message.tool_calls:
                results = []
                for tool_call in assistant_message.tool_calls:
                    tool_def = tool_defs[tool_call.name]
                    # noinspection PyProtectedMember
                    tool_result = await tool_def.logic_unit._execute(call_context=call_context, method_info=tool_def.method_info, args=tool_call.arguments)
                    message = ToolResponseMessage(tool_call_id=tool_call.tool_call_id, result=json.dumps(tool_result), name=tool_call.name)
                    if should_store_tool_calls:
                        await self.memory_unit.storeMessages(call_context, [message])
                    results.append(message)

                full_conversation = full_conversation + [assistant_message] + results
                num_iterations += 1
            else:
                return assistant_message

        raise ValueError(f"Exceeded maximum number of function calls {self.spec.max_num_function_calls}")
