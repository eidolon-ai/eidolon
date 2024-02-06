from typing import List, Dict, Any, Literal

from pydantic import BaseModel


# Base LLMMessage class
# todo, replace LLMMessage with LLMMessageTypes
class LLMMessage(BaseModel):
    type: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        if data.get("type") == "system":
            return SystemMessage.model_validate(data)
        elif data.get("type") == "user":
            return UserMessage.model_validate(data)
        elif data.get("type") == "assistant":
            return AssistantMessage.model_validate(data)
        elif data.get("type") == "tool":
            return ToolResponseMessage.model_validate(data)
        else:
            raise ValueError(f"Unknown message type {data.get('type')}")


# Derived SystemMessage class
class SystemMessage(LLMMessage):
    type: str = "system"
    content: str


# Derived classes for different types of message content parts
class UserMessageText(BaseModel):
    text: str
    type: Literal["text"] = "text"


class UserMessageImageURL(BaseModel):
    image_url: str
    type: Literal["image_url"] = "image_url"


# Derived UserMessage class
class UserMessage(LLMMessage):
    type: str = "user"
    content: List[UserMessageText | UserMessageImageURL]


# ToolCall class
class ToolCall(BaseModel):
    tool_call_id: str
    name: str
    arguments: Dict[str, Any]


# Derived AssistantMessage class
class AssistantMessage(LLMMessage):
    type: str = "assistant"
    content: Any
    tool_calls: List[ToolCall]


class ToolResponseMessage(LLMMessage):
    type: str = "tool"
    logic_unit_name: str
    name: str
    tool_call_id: str
    result: Any


LLMMessageTypes = SystemMessage | UserMessage | AssistantMessage | ToolResponseMessage
