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

    def extend_context(self, context: str):
        if self.stream_context is None:
            return [context]
        else:
            return [*self.stream_context, context]


class StartStreamEvent(BaseStreamEvent, ABC):
    event_type: Literal['start'] = "start"
    start_type: str


class EndStreamEvent(BaseStreamEvent, ABC):
    event_type: Literal['end'] = "end"
    end_type: str
    stop_reason: StopReason


class StartLLMEvent(StartStreamEvent):
    start_type: Literal["llm"] = "llm"


class EndLLMEvent(EndStreamEvent):
    end_type: Literal["llm"] = "llm"
    stop_reason: Literal[StopReason.COMPLETED] = StopReason.COMPLETED


class StringOutputEvent(BaseStreamEvent):
    event_type: Literal["string_output"] = "string_output"
    content: str


class ObjectOutputEvent(BaseStreamEvent, Generic[T]):
    event_type: Literal["object_output"] = "object_output"
    content: T


class ToolCallEvent(StartStreamEvent):
    start_type: Literal["tool_call"] = "tool_call"
    tool_call: ToolCall


class ToolEndEvent(EndStreamEvent):
    end_type: Literal["tool_end"] = "tool_end"
    tool_name: str
    stop_reason: Literal[StopReason.COMPLETED] = StopReason.COMPLETED


class ErrorEvent(EndStreamEvent):
    end_type: Literal["error"] = "error"
    reason: Any
    stop_reason: Literal[StopReason.ERROR] = StopReason.ERROR


class StartAgentCallEvent(StartStreamEvent):
    start_type: Literal["agent_call"] = "agent_call"
    agent_name: str
    call_name: str
    process_id: str


class EndAgentCallEvent(EndStreamEvent):
    end_type: Literal["agent_end"] = "agent_end"
    stop_reason: Literal[StopReason.COMPLETED] = StopReason.COMPLETED


class AgentStateEvent(BaseStreamEvent):
    event_type: Literal["agent_state"] = "agent_state"
    state: str
    available_actions: List[str] = None  # this is filled in by the server, agents should leave the default


StreamEvent = StartAgentCallEvent | \
              StartLLMEvent | \
              ToolCallEvent | \
              StringOutputEvent | \
              ObjectOutputEvent | \
              AgentStateEvent | \
              EndAgentCallEvent | \
              ToolEndEvent | \
              EndLLMEvent | \
              ErrorEvent


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
