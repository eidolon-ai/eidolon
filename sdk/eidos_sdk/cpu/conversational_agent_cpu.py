from typing import List, Type, Dict, Any, Union, Literal, AsyncIterator, AsyncGenerator

from aiostream import stream
from fastapi import HTTPException

from eidos_sdk.cpu.agent_cpu import AgentCPU, AgentCPUSpec, Thread
from eidos_sdk.cpu.agent_io import IOUnit, CPUMessageTypes
from eidos_sdk.cpu.call_context import CallContext
from eidos_sdk.cpu.llm_message import AssistantMessage, ToolResponseMessage, LLMMessage
from eidos_sdk.cpu.llm_unit import LLMUnit
from eidos_sdk.cpu.logic_unit import LogicUnit, LLMToolWrapper
from eidos_sdk.cpu.memory_unit import MemoryUnit
from eidos_sdk.cpu.processing_unit import ProcessingUnitLocator, PU_T
from eidos_sdk.io.events import ToolCallEvent, StringOutputEvent, ObjectOutputEvent, ErrorEvent, StreamEvent, \
    StartLLMEvent, EndStreamEvent, StopReason, SuccessEvent
from eidos_sdk.system.reference_model import Reference, AnnotatedReference, Specable


class ConversationalAgentCPUSpec(AgentCPUSpec):
    io_unit: AnnotatedReference[IOUnit]
    memory_unit: AnnotatedReference[MemoryUnit]
    llm_unit: AnnotatedReference[LLMUnit]
    logic_units: List[Reference[LogicUnit]] = []
    record_conversation: bool = True


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
        conversation_messages = await self.io_unit.process_request(boot_messages)
        await self.memory_unit.storeBootMessages(call_context, conversation_messages)

    async def schedule_request(
            self,
            call_context: CallContext,
            prompts: List[CPUMessageTypes],
            output_format: Union[Literal["str"], Dict[str, Any]] = "str",
    ) -> AsyncGenerator[StreamEvent, None]:
        try:
            conversation = await self.memory_unit.getConversationHistory(call_context)
            conversation_messages = await self.io_unit.process_request(prompts)
            if self.record_memory:
                await self.memory_unit.storeMessages(call_context, conversation_messages)
            conversation.extend(conversation_messages)
            llm_it = self._llm_execution_cycle(call_context, output_format, conversation)
            async for event in llm_it:
                yield event
        except HTTPException:
            raise
        except Exception as e:
            yield ErrorEvent(reason=e)

    async def _llm_execution_cycle(
            self,
            call_context: CallContext,
            output_format: Union[Literal["str"], Dict[str, Any]],
            conversation: List[LLMMessage]
    ) -> AsyncIterator[StreamEvent]:
        num_iterations = 0
        while num_iterations < self.spec.max_num_function_calls:
            tool_defs = await LLMToolWrapper.from_logic_units(self.logic_units, conversation=conversation)
            tool_call_events = []
            end_stream_event = None
            got_error = False
            execute_llm_ = self.llm_unit.execute_llm(call_context, conversation, [w.llm_message for w in tool_defs.values()], output_format)
            # yield the events but capture the output, so it can be rolled into one event for memory.
            output = None
            async for event in execute_llm_:
                if isinstance(event, ToolCallEvent):
                    tool_call_events.append(event)
                elif isinstance(event, StartLLMEvent):
                    yield event
                elif isinstance(event, StringOutputEvent):
                    if output is None:
                        output = event.content
                    elif isinstance(output, str):
                        output += event.content
                    else:
                        output = str(output) + event.content
                    yield event
                elif isinstance(event, ObjectOutputEvent):
                    if output is None:
                        output = event.content
                    else:
                        output = str(output) + str(event.content)
                    yield event
                elif isinstance(event, EndStreamEvent):
                    end_stream_event = event
                    if end_stream_event.event_type != StopReason.SUCCESS:
                        if end_stream_event.event_type == StopReason.ERROR:
                            got_error = True
                        yield event
                        break
                else:
                    yield event

            assistant_message = AssistantMessage(
                type="assistant",
                content=output,
                tool_calls=[tce.tool_call for tce in tool_call_events]
            )
            if self.record_memory:
                await self.memory_unit.storeMessages(call_context, [assistant_message])
            conversation.append(assistant_message)

            if got_error:
                return

            # process tool calls
            if len(tool_call_events) > 0:
                calls = []
                for tce in tool_call_events:
                    calls.append(self._call_tool(call_context, tce, tool_defs, conversation))

                combined_calls = stream.merge(calls[0], *calls[1:])
                async with combined_calls.stream() as streamer:
                    async for event in streamer:
                        yield event
            else:
                yield end_stream_event
                return

        yield ErrorEvent(reason="Exceeded maximum number of function calls")

    async def _call_tool(self, call_context: CallContext, tool_call_event: ToolCallEvent, tool_defs, conversation: List[LLMMessage]):
        parent_stream_context = tool_call_event.stream_context
        tool_def = tool_defs[tool_call_event.tool_call.name]
        tool_context = tool_call_event.extend_context(tool_call_event.tool_call.tool_call_id)
        try:
            tc = tool_call_event.tool_call
            yield ToolCallEvent(stream_context=tool_context, tool_call=tc)

            # todo -- change this into a stream on output -- this is so we can flow the output to the user
            tool_result = await tool_def.execute(call_context=parent_stream_context, args=tc.arguments)
            message = ToolResponseMessage(
                logic_unit_name=tool_def.logic_unit.__class__.__name__,
                tool_call_id=tc.tool_call_id,
                result=tool_result,
                name=tc.name,
            )
            if self.record_memory:
                await self.memory_unit.storeMessages(call_context, [message])
            conversation.append(message)
            # If the call returns a string just stream, else collect and return an object
            yield ObjectOutputEvent(stream_context=tool_context, content=tool_result)
            yield SuccessEvent(stream_context=tool_context)
        except Exception as e:
            yield ErrorEvent(stream_context=tool_context, reason=e)

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
