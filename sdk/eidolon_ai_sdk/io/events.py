from __future__ import annotations

from abc import ABC
from enum import Enum
from pydantic import BaseModel, TypeAdapter, field_serializer
from typing import List, TypeVar, Generic, Any, AsyncIterator, Type, Literal, Dict, Optional

from eidolon_ai_sdk.cpu.llm_message import ToolCall


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
    stream_context: Optional[str] = None
    category: Category
    event_type: str

    def is_root_event(self):
        return self.stream_context is None

    def is_root_and_type(self, event_type: type):
        return self.stream_context is None and isinstance(self, event_type)

    @classmethod
    def from_dict(cls, event_dict: Dict[str, Any]):
        event_type = event_dict["event_type"]
        # remove fields that are set automatically
        del event_dict["event_type"]
        del event_dict["category"]
        if event_dict["stream_context"] is None:
            del event_dict["stream_context"]
        if event_type == "string":
            return StringOutputEvent(**event_dict)
        elif event_type == "object":
            return ObjectOutputEvent(**event_dict)
        elif event_type == "tool_call_start":
            return ToolCallStartEvent(**event_dict)
        elif event_type == "context_start":
            return StartStreamContextEvent(**event_dict)
        elif event_type == "context_end":
            return EndStreamContextEvent(**event_dict)
        elif event_type == "llm_tool_call_request":
            return LLMToolCallRequestEvent(**event_dict)
        elif event_type == "agent_call":
            return StartAgentCallEvent(**event_dict)
        elif event_type == "llm":
            return StartLLMEvent(**event_dict)
        elif event_type == "success":
            return SuccessEvent(**event_dict)
        elif event_type == "canceled":
            return CanceledEvent(**event_dict)
        elif event_type == "error":
            return ErrorEvent(**event_dict)
        elif event_type == "agent_state":
            return AgentStateEvent(**event_dict)
        else:
            raise ValueError(f"Unknown event type {event_type}")


class StartStreamContextEvent(BaseStreamEvent):
    category: Literal[Category.START] = Category.START
    event_type: Literal["context_start"] = "context_start"
    context_id: str

    def get_nested_context(self):
        context = self.stream_context + "." if self.stream_context else ""
        return context + self.context_id


class EndStreamContextEvent(BaseStreamEvent):
    category: Literal[Category.START] = Category.END
    event_type: Literal["context_end"] = "context_end"
    context_id: str


class StartLLMEvent(BaseStreamEvent):
    event_type: Literal["llm"] = "llm"
    category: Literal[Category.START] = Category.START


class ToolCallStartEvent(StartStreamContextEvent):
    event_type: Literal["tool_call"] = "tool_call_start"
    tool_call: ToolCall


class StartAgentCallEvent(BaseStreamEvent):
    category: Literal[Category.START] = Category.START
    event_type: Literal["agent_call"] = "agent_call"
    machine: str
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


class LLMToolCallRequestEvent(BaseStreamEvent):
    category: Literal[Category.OUTPUT] = Category.OUTPUT
    event_type: Literal["tool_call"] = "llm_tool_call_request"
    tool_call: ToolCall


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

    @field_serializer("reason")
    def serialize_reason(self, reason: Any):
        if isinstance(reason, Exception):
            return f"{type(reason).__name__}: {reason}"
        else:
            return reason


class AgentStateEvent(BaseStreamEvent):
    category: Literal[Category.TRANSFORM] = Category.TRANSFORM
    event_type: Literal["agent_state"] = "agent_state"
    state: str
    available_actions: List[str] = None  # this is filled in by the server, agents should leave the default


StreamEvent = (
    StartAgentCallEvent
    | StartLLMEvent
    | ToolCallStartEvent
    | StartStreamContextEvent
    | EndStreamContextEvent
    | LLMToolCallRequestEvent
    | StringOutputEvent
    | ObjectOutputEvent
    | SuccessEvent
    | CanceledEvent
    | ErrorEvent
    | AgentStateEvent
)


async def convert_output_object(it: AsyncIterator[StreamEvent], output_format: Type[T]) -> AsyncIterator[StreamEvent]:
    model = TypeAdapter(output_format)
    async for event in it:
        if event.is_root_and_type(ObjectOutputEvent):
            event.content = model.validate_python(event.content)
        yield event
