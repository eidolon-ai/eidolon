from __future__ import annotations

from abc import ABC
from enum import Enum
from pydantic import BaseModel, TypeAdapter, field_serializer
from typing import List, TypeVar, Generic, Any, AsyncIterator, Type, Literal, Dict, Optional


class Category(Enum):
    START = "start"
    INPUT = "input"
    END = "end"
    OUTPUT = "output"
    TRANSFORM = "transform"


T = TypeVar("T")


class BaseStreamEvent(BaseModel, ABC):
    stream_context: Optional[str] = None
    category: Category
    event_type: str

    def is_root_event(self):
        return self.stream_context is None

    def is_root_and_type(self, event_type: type):
        return self.stream_context is None and isinstance(self, event_type)

    def is_root_end_event(self):
        return self.is_root_and_type(EndStreamEvent)

    @classmethod
    def from_dict(cls, event_dict: Dict[str, Any]):
        # remove fields that are set automatically
        event_type = event_dict.pop("event_type")
        if "category" in event_dict:
            del event_dict["category"]
        if event_dict.get("stream_context", ...) is None:
            del event_dict["stream_context"]

        return _type_mapping[event_type](**event_dict)


class UserInputEvent(BaseStreamEvent):
    category: Literal[Category.INPUT] = Category.INPUT
    event_type: Literal["user_input"] = "user_input"
    input: Dict[str, Any]


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


class ToolCallStartEvent(StartStreamContextEvent):
    event_type: Literal["tool_call_start"] = "tool_call_start"
    tool_call: ToolCall
    title: str
    sub_title: str = ""
    is_agent_call: bool = False


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
    event_type: Literal["llm_tool_call_request"] = "llm_tool_call_request"
    tool_call: ToolCall


class StringOutputEvent(OutputEvent):
    event_type: Literal["string"] = "string"
    content: str


class ObjectOutputEvent(OutputEvent, Generic[T]):
    event_type: Literal["object"] = "object"
    content: T


# note EndStreamEvent does not need to reference the type of event it ends since this is captured by context
class EndStreamEvent(BaseStreamEvent, ABC):
    category: Literal[Category.END] = Category.END
    event_type: Literal["error", "success", "canceled"]


class SuccessEvent(EndStreamEvent):
    event_type: Literal["success"] = "success"


class CanceledEvent(EndStreamEvent):
    event_type: Literal["canceled"] = "canceled"


class ErrorEvent(EndStreamEvent):
    event_type: Literal["error"] = "error"
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
    StartAgentCallEvent  # todo, this smells like UserInputEvent and StartAgentCallEvent
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
    | UserInputEvent
)

_type_mapping = {c.model_fields["event_type"].annotation.__args__[0]: c for c in StreamEvent.__args__}


async def convert_output_object(it: AsyncIterator[StreamEvent], output_format: Type[T]) -> AsyncIterator[StreamEvent]:
    model = TypeAdapter(output_format)
    async for event in it:
        if event.is_root_and_type(ObjectOutputEvent):
            event.content = model.validate_python(event.content)
        yield event


class ToolCall(BaseModel):
    tool_call_id: str
    name: str
    arguments: Dict[str, Any]
