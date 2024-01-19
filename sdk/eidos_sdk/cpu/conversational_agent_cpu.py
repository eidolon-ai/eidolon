from aiostream import stream
from fastapi import HTTPException
from typing import List, Type, Dict, Any, Union, Literal, AsyncIterator, AsyncGenerator

from eidos_sdk.cpu.agent_cpu import AgentCPU, AgentCPUSpec, Thread
from eidos_sdk.cpu.agent_io import IOUnit, CPUMessageTypes
from eidos_sdk.cpu.call_context import CallContext
from eidos_sdk.cpu.llm_message import AssistantMessage, ToolResponseMessage, ToolCall
from eidos_sdk.cpu.llm_unit import LLMUnit
from eidos_sdk.cpu.logic_unit import LogicUnit, LLMToolWrapper
from eidos_sdk.cpu.memory_unit import MemoryUnit
from eidos_sdk.cpu.processing_unit import ProcessingUnitLocator, PU_T
from eidos_sdk.io.events import ToolCallEvent, EndStreamEvent, StartStreamEvent, StringOutputEvent, ObjectOutputEvent, StopReason, ErrorEvent, StreamEvent, with_context
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
    ) -> AsyncGenerator[StreamEvent, None]:
        try:
            conversation_messages = await self.io_unit.process_request(prompts)
            await self.memory_unit.storeMessages(call_context, conversation_messages)
            context = f"{call_context.process_id}"
            if call_context.thread_id:
                context += f":{call_context.thread_id}"
            llm_it = with_context(context, self._llm_execution_cycle(call_context, output_format))
            async for event in llm_it:
                yield event
        except HTTPException:
            raise
        except Exception as e:
            yield ErrorEvent(reason=str(e))

    async def _call_tool(self, call_context: CallContext, tool_call_event: ToolCallEvent, tool_defs):
        parent_stream_context = tool_call_event.stream_context
        tool_def = tool_defs[tool_call_event.tool_name]
        tool_context = [*tool_call_event.stream_context, tool_call_event.tool_call_id]
        try:
            tc = ToolCall(
                tool_call_id=tool_call_event.tool_call_id,
                name=tool_call_event.tool_name,
                arguments=tool_call_event.tool_args,
            )
            yield ToolCallEvent(stream_context=tool_context,
                                tool_call_id=tool_call_event.tool_call_id,
                                tool_name=tool_call_event.tool_name,
                                tool_args=tool_call_event.tool_args)

            # todo -- change this into a stream on output
            tool_result = await tool_def.execute(call_context=parent_stream_context, args=tc.arguments)
            message = ToolResponseMessage(
                logic_unit_name=tool_def.logic_unit.__class__.__name__,
                tool_call_id=tc.tool_call_id,
                result=tool_result,
                name=tc.name,
            )
            await self.memory_unit.storeMessages(call_context, [message])
            yield ObjectOutputEvent(stream_context=tool_context, content=tool_result)
            yield EndStreamEvent(stream_context=tool_context, stop_reason=StopReason.COMPLETED)
        except Exception as e:
            yield ErrorEvent(stream_context=tool_context, reason=str(e))

    async def _llm_execution_cycle(
            self,
            call_context: CallContext,
            output_format: Union[Literal["str"], Dict[str, Any]],
    ) -> AsyncIterator[StreamEvent]:
        num_iterations = 0
        while num_iterations < self.spec.max_num_function_calls:
            conversation = await self.memory_unit.getConversationHistory(call_context)
            tool_defs = await LLMToolWrapper.from_logic_units(self.logic_units, conversation=conversation)
            tool_call_events = []
            end_stream_event = None
            execute_llm_ = self.llm_unit.execute_llm2(call_context, conversation, [w.llm_message for w in tool_defs.values()], output_format)
            async for event in execute_llm_:
                if isinstance(event, ToolCallEvent):
                    tool_call_events.append(event)
                elif isinstance(event, StartStreamEvent):
                    yield event
                elif isinstance(event, StringOutputEvent) or isinstance(event, ObjectOutputEvent):
                    # todo -- change memory unit to store events...
                    assistant_message = AssistantMessage(
                        type="assistant",
                        content=event.content,
                        tool_calls=[],
                    )
                    await self.memory_unit.storeMessages(call_context, [assistant_message])

                    yield event
                elif isinstance(event, EndStreamEvent):
                    end_stream_event = event
                else:
                    yield event

            # process tool calls
            if len(tool_call_events) > 0:
                tool_calls = []
                for tce in tool_call_events:
                    tool_calls.append(
                        ToolCall(
                            tool_call_id=tce.tool_call_id,
                            name=tce.tool_name,
                            arguments=tce.tool_args,
                        )
                    )
                assistant_message = AssistantMessage(
                    type="assistant",
                    content=None,
                    tool_calls=tool_calls,
                )
                await self.memory_unit.storeMessages(call_context, [assistant_message])

                calls = []
                for tce in tool_call_events:
                    calls.append(self._call_tool(call_context, tce, tool_defs))

                combined_calls = stream.merge(calls[0], *calls[1:])
                async with combined_calls.stream() as streamer:
                    async for event in streamer:
                        yield event
            else:
                yield end_stream_event
                return

        yield ErrorEvent(reason="Exceeded maximum number of function calls")

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
