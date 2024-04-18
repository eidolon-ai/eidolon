from typing import List, Type, Dict, Any, Union, Literal, AsyncIterator

from fastapi import HTTPException
from opentelemetry import trace

from eidolon_ai_client.events import (
    StreamEvent,
    LLMToolCallRequestEvent,
    ToolCallStartEvent,
)
from eidolon_ai_client.util.logger import logger
from eidolon_ai_client.util.stream_collector import merge_streams
from eidolon_ai_sdk.agent.doc_manager.document_processor import DocumentProcessor
from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import FileInfo
from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DataBlob
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.cpu.agent_cpu import APU, APUSpec, Thread, APUException, APUCapabilities
from eidolon_ai_sdk.cpu.agent_io import IOUnit, CPUMessageTypes
from eidolon_ai_sdk.cpu.audio_unit import AudioUnit
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.image_unit import ImageUnit
from eidolon_ai_sdk.cpu.llm_message import (
    AssistantMessage,
    ToolResponseMessage,
    LLMMessage,
    UserMessageFile,
    UserMessageAudio,
    UserMessageImage,
    UserMessageText,
    UserMessage,
)
from eidolon_ai_sdk.cpu.llm_unit import LLMUnit
from eidolon_ai_sdk.cpu.logic_unit import LogicUnit, LLMToolWrapper
from eidolon_ai_sdk.cpu.memory_unit import MemoryUnit
from eidolon_ai_sdk.cpu.processing_unit import ProcessingUnitLocator, PU_T
from eidolon_ai_sdk.system.reference_model import Reference, AnnotatedReference, Specable
from eidolon_ai_sdk.util.stream_collector import StreamCollector, stream_manager, ManagedContextError

tracer = trace.get_tracer("cpu")


class ConversationalAPUSpec(APUSpec):
    io_unit: AnnotatedReference[IOUnit]
    memory_unit: AnnotatedReference[MemoryUnit]
    llm_unit: AnnotatedReference[LLMUnit]
    logic_units: List[Reference[LogicUnit]] = []
    audio_unit: Reference[AudioUnit] = None
    image_unit: Reference[ImageUnit] = None
    record_conversation: bool = True
    allow_tool_errors: bool = True
    document_processor: AnnotatedReference[DocumentProcessor]


class ConversationalAPU(APU, Specable[ConversationalAPUSpec], ProcessingUnitLocator):
    io_unit: IOUnit
    memory_unit: MemoryUnit
    logic_units: List[LogicUnit]
    llm_unit: LLMUnit
    audio_unit: AudioUnit
    image_unit: ImageUnit
    document_processor: DocumentProcessor

    def __init__(self, spec: ConversationalAPUSpec = None):
        super().__init__(spec)
        kwargs = dict(processing_unit_locator=self)
        self.io_unit = self.spec.io_unit.instantiate(**kwargs)
        self.memory_unit = self.spec.memory_unit.instantiate(**kwargs)
        self.llm_unit = self.spec.llm_unit.instantiate(**kwargs)
        self.logic_units = [logic_unit.instantiate(**kwargs) for logic_unit in self.spec.logic_units]
        self.audio_unit = self.spec.audio_unit.instantiate(**kwargs) if self.spec.audio_unit else None
        self.image_unit = self.spec.image_unit.instantiate(**kwargs) if self.spec.image_unit else None
        self.record_memory = self.spec.record_conversation
        self.document_processor = self.spec.document_processor.instantiate()
        if self.audio_unit:
            self.logic_units.append(self.audio_unit)
        if self.image_unit:
            self.logic_units.append(self.image_unit)

    def get_capabilities(self) -> APUCapabilities:
        llm_props = self.llm_unit.get_llm_capabilities()
        return APUCapabilities(
            input_context_limit=llm_props.input_context_limit,
            output_context_limit=llm_props.output_context_limit,
            supports_tools=llm_props.supports_tools,
            supports_image_input=llm_props.supports_image_input or self.spec.image_unit is not None,
            supports_audio_input=llm_props.supports_audio_input or self.spec.audio_unit is not None,
            supports_file_search=llm_props.supports_tools and self.document_processor is not None,
            supports_audio_generation=self.spec.audio_unit is not None,
            supports_image_generation=self.spec.image_unit is not None,
        )

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

        if isinstance(self.audio_unit, unit_type):
            return self.audio_unit

        if isinstance(self.image_unit, unit_type):
            return self.image_unit

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
        except HTTPException as e:
            raise e
        except APUException as e:
            raise e
        except Exception as e:
            logger.exception(e)
            raise APUException(f"{e.__class__.__name__} while processing request") from e

    async def _llm_execution_cycle(
        self,
        call_context: CallContext,
        output_format: Union[Literal["str"], Dict[str, Any]],
        conversation: List[LLMMessage],
    ) -> AsyncIterator[StreamEvent]:
        # first convert the conversation to fill in file data
        converted_conversation = []
        for event in conversation:
            if isinstance(event, UserMessage):
                converted_messages = []
                for message in event.content:
                    if isinstance(message, UserMessageFile) and message.include_directly:
                        converted_messages.extend(await self.process_file_message(call_context.process_id, message))
                    elif isinstance(message, UserMessageAudio):
                        converted_messages.extend(await self.process_audio_message(message))
                    elif isinstance(message, UserMessageImage):
                        converted_messages.extend(await self.process_image_message(message))
                    else:
                        converted_messages.append(message)
                converted_conversation.append(UserMessage(content=converted_messages))
            else:
                converted_conversation.append(event)

        num_iterations = 0
        while num_iterations < self.spec.max_num_function_calls:
            with tracer.start_as_current_span("building tools"):
                tool_defs = await LLMToolWrapper.from_logic_units(call_context, self.logic_units)
                tool_call_events = []
                llm_facing_tools = [w.llm_message for w in tool_defs.values()]
            with tracer.start_as_current_span("llm execution"):
                execute_llm_ = self.llm_unit.execute_llm(
                    call_context, converted_conversation, llm_facing_tools, output_format
                )
                # yield the events but capture the output, so it can be rolled into one event for memory.
                # noinspection PyTypeChecker
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
            converted_conversation.append(assistant_message)

            if tool_call_events:
                with tracer.start_as_current_span("tool calls"):
                    streams = [
                        self._call_tool(call_context, tce, tool_defs, converted_conversation) for tce in tool_call_events
                    ]
                    async for e in merge_streams(streams):
                        yield e
            else:
                return

        raise APUException(f"exceeded maximum number of function calls ({self.spec.max_num_function_calls})")

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
                title=tool_def.eidolon_handler.extra.get("title", tool_def.eidolon_handler.name),
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

    async def process_audio_message(self, message: UserMessageAudio):
        if self.audio_unit is None:
            raise ValueError("No audio unit available")
        message = f"The user uploaded an audio clip with the file handle of {message.file.model_dump()}. Use the text_to_speech tool to process this audio file. Always process the audio file!"
        return [UserMessageText(text=message)]

    async def process_image_message(self, message: UserMessageImage):
        if self.image_unit is not None:
            message = f"The user uploaded an image with the file handle of {message.file.model_dump()}. Use the image_to_text tool to process this image file. Always process the image file!"
            return [UserMessageText(text=message)]
        elif self.get_capabilities().supports_image_input:
            return [message]
        else:
            raise ValueError("Image processing not supported")

    async def process_file_message(self, process_id: str, message: UserMessageFile):
        parts = []
        if message.include_directly:
            data, metadata = await AgentOS.process_file_system.read_file(process_id, message.file.file_id)
            path = metadata.get("path") or metadata.get("filename") or None
            mimetype = metadata.get("mimetype")
            message = f"The file {path} was uploaded. The text of the file is:\n"
            for docs in self.document_processor.parse(data, mimetype, path):
                message += docs.page_content + "\n"

            parts.append(UserMessageText(text=message))
        else:
            data, metadata = await AgentOS.process_file_system.read_file(process_id, message.file.file_id)
            path = metadata.get("path") or metadata.get("filename") or None
            mimetype = metadata.get("mimetype")
            blob = DataBlob.from_bytes(data=data, mimetype=mimetype, path=path)
            await self.document_processor.addFile(
                f"pf_pid_{process_id}", FileInfo(data=blob, path="", metadata=metadata)
            )
            message = f"The file {path} is available to search. Use the provided search tool to find information contained in the file\n"
            parts.append(UserMessageText(text=message))

        return parts

    async def clone_thread(self, call_context: CallContext) -> Thread:
        new_context = call_context.derive_call_context()
        await self.io_unit.clone_thread(call_context, new_context)
        await self.memory_unit.clone_thread(call_context, new_context)
        for processor in self.logic_units:
            await processor.clone_thread(call_context, new_context)

        return Thread(call_context=new_context, cpu=self)
