from __future__ import annotations

from abc import ABC
from enum import Enum
from pydantic import BaseModel, TypeAdapter
from typing import List, TypeVar, Generic, Any, AsyncIterator, Type, Literal

from eidos_sdk.cpu.llm_message import ToolCall


class Category(Enum):
    START = "start"
    END = "end"
    OUTPUT = "output"
    TRANSFORM = "transform"


class StopReason(Enum):
    ERROR = "error"
    SUCCESS = "success"
    CANCELED = "canceled"


T = TypeVar("T")


class BaseStreamEvent(BaseModel, ABC):
    stream_context: List[str] = None
    category: Category
    event_type: str

    def extend_context(self, context: str):
        if self.stream_context is None:
            return [context]
        else:
            return [*self.stream_context, context]


class StartStreamEvent(BaseStreamEvent, ABC):
    category: Literal[Category.START] = Category.START


class StartLLMEvent(StartStreamEvent):
    event_type: Literal["llm"] = "llm"


class ToolCallEvent(StartStreamEvent):
    event_type: Literal["tool_call"] = "tool_call"
    tool_call: ToolCall


class StartAgentCallEvent(StartStreamEvent):
    event_type: Literal["agent_call"] = "agent_call"
    agent_name: str
    call_name: str
    process_id: str


class OutputEvent(BaseStreamEvent, ABC):
    category: Literal[Category.OUTPUT] = Category.OUTPUT
    content: Any

    @staticmethod
    def get(content: T, **kwargs):
        if isinstance(content, str):
            return StringOutputEvent(content=content, **kwargs)
        else:
            return ObjectOutputEvent[T](content=content, **kwargs)


class StringOutputEvent(OutputEvent):
    event_type: Literal["string_output"] = "string"
    content: str


class ObjectOutputEvent(OutputEvent, Generic[T]):
    event_type: Literal["object_output"] = "object"
    content: T


# note EndStreamEvent does not need to reference the type of event it ends since this is captured by context
class EndStreamEvent(BaseStreamEvent, ABC):
    category: Literal[Category.END] = Category.END
    event_type: StopReason


class SuccessEvent(EndStreamEvent):
    event_type: Literal[StopReason.SUCCESS] = StopReason.SUCCESS


class CanceledEvent(EndStreamEvent):
    event_type: Literal[StopReason.CANCELED] = StopReason.CANCELED


class ErrorEvent(EndStreamEvent):
    event_type: Literal[StopReason.ERROR] = StopReason.ERROR
    reason: Any


class AgentStateEvent(BaseStreamEvent):
    category: Literal[Category.TRANSFORM] = Category.TRANSFORM
    event_type: Literal["agent_state"] = "agent_state"
    state: str
    available_actions: List[str] = None  # this is filled in by the server, agents should leave the default


StreamEvent = StartAgentCallEvent | StartLLMEvent | ToolCallEvent | \
              StringOutputEvent | ObjectOutputEvent | \
              SuccessEvent | CanceledEvent | ErrorEvent | \
              AgentStateEvent


async def with_context(context: List[str], it: AsyncIterator[StreamEvent]) -> AsyncIterator[StreamEvent]:
    async for event in it:
        if event.stream_context is None:
            event.stream_context = [*context]
        else:
            event.stream_context = [*context, *event.stream_context]
        yield event


async def convert_output_object(it: AsyncIterator[StreamEvent], output_format: Type[T]) -> AsyncIterator[StreamEvent]:
    model = TypeAdapter(output_format)
    async for event in it:
        if isinstance(event, ObjectOutputEvent):
            event.content = model.validate_python(event.content)
        yield event
