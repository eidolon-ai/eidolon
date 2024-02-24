from typing import List, Type, Dict, Any, Union, Literal, AsyncIterator

from eidolon_ai_sdk.cpu.agent_cpu import AgentCPU, AgentCPUSpec, Thread, CPUException
from eidolon_ai_sdk.cpu.agent_io import IOUnit, CPUMessageTypes
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.llm_message import AssistantMessage, ToolResponseMessage, LLMMessage
from eidolon_ai_sdk.cpu.llm_unit import LLMUnit
from eidolon_ai_sdk.cpu.logic_unit import LogicUnit, LLMToolWrapper
from eidolon_ai_sdk.cpu.memory_unit import MemoryUnit
from eidolon_ai_sdk.cpu.processing_unit import ProcessingUnitLocator, PU_T
from eidolon_ai_client.events import (
    StreamEvent,
    LLMToolCallRequestEvent,
    ToolCallStartEvent,
)
from eidolon_ai_sdk.system.reference_model import Reference, AnnotatedReference, Specable
from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.util.stream_collector import StreamCollector, stream_manager, ManagedContextError
from eidolon_ai_client.util.stream_collector import merge_streams


class ConversationalAgentCPUSpec(AgentCPUSpec):
    io_unit: AnnotatedReference[IOUnit]
    memory_unit: AnnotatedReference[MemoryUnit]
    llm_unit: AnnotatedReference[LLMUnit]
    logic_units: List[Reference[LogicUnit]] = []
    record_conversation: bool = True
    allow_tool_errors: bool = True


class ConversationalAgentCPU(AgentCPU, Specable[ConversationalAgentCPUSpec], ProcessingUnitLocator):
    io_unit: IOUnit
    memory_unit: MemoryUnit
    logic_units: List[LogicUnit]

    def __init__(self, spec: ConversationalAgentCPUSpec = None):
        super().__init__(spec)
        kwargs = dict(processing_unit_locator=self)
        self.io_unit = self.spec.io_unit.instantiate(**kwargs)
        self.memory_unit = self.spec.memory_unit.instantiate(**kwargs)
        self.llm_unit = self.spec.llm_unit.instantiate(**kwargs)
        self.logic_units = [logic_unit.instantiate(**kwargs) for logic_unit in self.spec.logic_units]
        self.record_memory = self.spec.record_conversation

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
        conversation_messages = await self.io_unit.process_request(call_context, boot_messages)
        await self.memory_unit.storeBootMessages(call_context, conversation_messages)

    async def schedule_request(
        self,
        call_context: CallContext,
        prompts: List[CPUMessageTypes],
        output_format: Union[Literal["str"], Dict[str, Any]] = "str",
    ) -> AsyncIterator[StreamEvent]:
        try:
            conversation = await self.memory_unit.getConversationHistory(call_context)
            conversation_messages = await self.io_unit.process_request(call_context, prompts)
            if self.record_memory:
                await self.memory_unit.storeMessages(call_context, conversation_messages)
            conversation.extend(conversation_messages)
            async for event in self._llm_execution_cycle(call_context, output_format, conversation):
                yield event
        except CPUException as e:
            raise e
        except Exception as e:
            raise CPUException(f"error while processing request ({e.__class__.__name__})") from e

    async def _llm_execution_cycle(
        self,
        call_context: CallContext,
        output_format: Union[Literal["str"], Dict[str, Any]],
        conversation: List[LLMMessage],
    ) -> AsyncIterator[StreamEvent]:
        num_iterations = 0
        while num_iterations < self.spec.max_num_function_calls:
            tool_defs = await LLMToolWrapper.from_logic_units(call_context, self.logic_units)
            tool_call_events = []
            execute_llm_ = self.llm_unit.execute_llm(
                call_context, conversation, [w.llm_message for w in tool_defs.values()], output_format
            )
            # yield the events but capture the output, so it can be rolled into one event for memory.
            stream_collector = StreamCollector(execute_llm_)
            async for event in stream_collector:
                if event.is_root_and_type(LLMToolCallRequestEvent):
                    tool_call_events.append(event)
                yield event
            if stream_collector.get_content():
                logger.info(f"LLM Response: {stream_collector.get_content()}")

            assistant_message = AssistantMessage(
                type="assistant",
                content=stream_collector.get_content() or "",
                tool_calls=[tce.tool_call for tce in tool_call_events],
            )
            if self.record_memory:
                await self.memory_unit.storeMessages(call_context, [assistant_message])
            conversation.append(assistant_message)

            # process tool calls
            async for e in merge_streams(
                [self._call_tool(call_context, tce, tool_defs, conversation) for tce in tool_call_events]
            ):
                yield e
            if not tool_call_events:
                return

        raise CPUException(f"exceeded maximum number of function calls ({self.spec.max_num_function_calls})")

    async def _call_tool(
        self,
        call_context: CallContext,
        tool_call_event: LLMToolCallRequestEvent,
        tool_defs,
        conversation: List[LLMMessage],
    ):
        tc = tool_call_event.tool_call
        logic_unit_wrapper = ["NaN"]

        tool_def = tool_defs[tc.name]

        def tool_event_stream():
            try:
                logic_unit_wrapper[0] = tool_def.logic_unit.__class__.__name__
                return tool_def.execute(tool_call=tc)
            except KeyError:
                raise ValueError(f"Tool {tool_call_event.tool_call.name} not found. Available tools: {tool_defs.keys()}")

        tool_stream = stream_manager(
            tool_event_stream,
            ToolCallStartEvent(
                tool_call=tc,
                context_id=tc.tool_call_id,
                title=tool_def.eidolon_handler.extra["title"],
                sub_title=tool_def.eidolon_handler.extra.get("sub_title", ""),
                is_agent_call=tool_def.eidolon_handler.extra.get("agent_call", False),
            ),
        )
        try:
            async for event in tool_stream:
                yield event
        except ManagedContextError:
            if self.spec.allow_tool_errors:
                logger.warning("Error calling tool " + tool_call_event.tool_call.name, exc_info=True)
            else:
                raise

        message = ToolResponseMessage(
            logic_unit_name=logic_unit_wrapper[0],
            tool_call_id=tc.tool_call_id,
            result=tool_stream.get_content() or "",
            name=tc.name,
        )
        if self.record_memory:
            await self.memory_unit.storeMessages(call_context, [message])
        conversation.append(message)

    async def clone_thread(self, call_context: CallContext) -> Thread:
        new_context = call_context.derive_call_context()
        await self.io_unit.clone_thread(call_context, new_context)
        await self.memory_unit.clone_thread(call_context, new_context)
        for processor in self.logic_units:
            await processor.clone_thread(call_context, new_context)

        return Thread(call_context=new_context, cpu=self)
