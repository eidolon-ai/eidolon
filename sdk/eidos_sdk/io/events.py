from __future__ import annotations

from abc import ABC
from enum import Enum
from pydantic import BaseModel, TypeAdapter
from typing import List, TypeVar, Generic, Any, AsyncIterator, Type, Literal

from eidos_sdk.cpu.llm_message import ToolCall


class StopReason(Enum):
    ERROR = "error"
    COMPLETED = "completed"
    CANCELED = "canceled"


T = TypeVar("T")


class BaseStreamEvent(BaseModel, ABC):
    stream_context: List[str] = None
    event_type: Literal["start", "end", "string_output", "object_output"]


class StartStreamEvent(BaseStreamEvent, ABC):
    event_type: str = "start"
    start_type: str


class EndStreamEvent(BaseStreamEvent, ABC):
    event_type: str = "end"
    end_type: str
    stop_reason: StopReason


class StartLLMEvent(StartStreamEvent):
    start_type: str = "llm"


class EndLLMEvent(EndStreamEvent):
    end_type: str = "llm"
    stop_reason: StopReason = StopReason.COMPLETED


class StringOutputEvent(BaseStreamEvent):
    event_type: str = "string_output"
    content: str


class ObjectOutputEvent(BaseStreamEvent, Generic[T]):
    event_type: str = "object_output"
    content: T


class ToolCallEvent(StartStreamEvent):
    start_type: str = "tool_call"
    tool_call: ToolCall


class ToolEndEvent(EndStreamEvent):
    event_type: str = "tool_end"
    tool_name: str
    stop_reason: StopReason = StopReason.COMPLETED


class ErrorEvent(EndStreamEvent):
    end_type: str = "error"
    reason: Any
    stop_reason: StopReason = StopReason.ERROR


class StartAgentCallEvent(StartStreamEvent):
    start_type: str = "agent_call"
    agent_name: str
    call_name: str
    process_id: str


class EndAgentCallEvent(EndStreamEvent):
    end_type: str = "agent_end"
    stop_reason: StopReason = StopReason.COMPLETED


class AgentStateEvent(BaseStreamEvent):
    event_type: str = "agent_state"
    state: str
    available_actions: List[str] = None  # this is filled in by the server, agents should leave the default


StreamEvent = StartStreamEvent | EndStreamEvent | StringOutputEvent | ObjectOutputEvent | ToolCallEvent | ToolEndEvent | ErrorEvent


async def with_context(context: str, it: AsyncIterator[StreamEvent]) -> AsyncIterator[StreamEvent]:
    async for event in it:
        if event.stream_context is None:
            event.stream_context = [context]
        else:
            event.stream_context = [context, *event.stream_context]
        yield event


async def convert_output_object(it: AsyncIterator[StreamEvent], output_format: Type[T]) -> AsyncIterator[StreamEvent]:
    model = TypeAdapter(output_format)
    async for event in it:
        if isinstance(event, ObjectOutputEvent):
            event.content = model.validate_python(event.content)
        yield event
