from __future__ import annotations

from abc import ABC
from enum import Enum
from pydantic import BaseModel, TypeAdapter
from typing import List, TypeVar, Generic, Any, Dict, AsyncIterator, Type


class StopReason(Enum):
    ERROR = "error"
    COMPLETED = "completed"
    CANCELED = "canceled"


T = TypeVar("T")


class BaseStreamEvent(ABC, BaseModel):
    stream_context: List[str] = None


class StartStreamEvent(BaseStreamEvent):
    pass


class EndStreamEvent(BaseStreamEvent):
    stop_reason: StopReason


class StringOutputEvent(BaseStreamEvent):
    content: str


class ObjectOutputEvent(BaseStreamEvent, Generic[T]):
    content: T


class ToolCallEvent(StartStreamEvent):
    tool_call_id: str
    tool_name: str
    tool_args: Dict[str, Any]


class ToolEndEvent(EndStreamEvent):
    tool_name: str


class ErrorEvent(EndStreamEvent):
    reason: Any
    stop_reason: StopReason = StopReason.ERROR


class StartAgentCallEvent(StartStreamEvent):
    pass


class EndAgentCallEvent(EndStreamEvent):
    stop_reason: StopReason = StopReason.COMPLETED


class AgentStateEvent(BaseStreamEvent):
    state: str


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
