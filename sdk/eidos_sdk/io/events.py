from __future__ import annotations

from abc import ABC
from enum import Enum
from pydantic import BaseModel, TypeAdapter
from typing import List, TypeVar, Generic, Any, Dict, AsyncIterator, Type, Literal


class StopReason(Enum):
    ERROR = "error"
    COMPLETED = "completed"
    CANCELED = "canceled"


T = TypeVar("T")


class BaseStreamEvent(ABC, BaseModel):
    stream_context: List[str] = None
    event_type: Literal["start", "end", "string_output", "object_output", "tool_call", "tool_end", "error", "agent_call", "agent_end"]


class StartStreamEvent(BaseStreamEvent):
    event_type: str = "start"


class EndStreamEvent(BaseStreamEvent):
    event_type: str = "end"
    stop_reason: StopReason


class StringOutputEvent(BaseStreamEvent):
    event_type: str = "string_output"
    content: str


class ObjectOutputEvent(BaseStreamEvent, Generic[T]):
    event_type: str = "object_output"
    content: T


class ToolCallEvent(StartStreamEvent):
    event_type: str = "tool_call"
    tool_call_id: str
    tool_name: str
    tool_args: Dict[str, Any]


class ToolEndEvent(EndStreamEvent):
    event_type: str = "tool_end"
    tool_name: str


class ErrorEvent(EndStreamEvent):
    event_type: str = "error"
    reason: Any
    stop_reason: StopReason = StopReason.ERROR


class StartAgentCallEvent(StartStreamEvent):
    event_type: str = "agent_call"
    agent_name: str
    call_name: str
    process_id: str


class EndAgentCallEvent(EndStreamEvent):
    event_type: str = "agent_end"
    stop_reason: StopReason = StopReason.COMPLETED


class AgentStateEvent(BaseStreamEvent):
    event_type: str = "agent_state"
    state: str
    available_actions: List[str] = []


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
