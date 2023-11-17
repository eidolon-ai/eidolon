from typing import List, Dict, Any, Optional

from pydantic import BaseModel, Field, SerializeAsAny, field_validator


# Base LLMMessage class
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
            return ToolCallMessage.model_validate(data)
        else:
            raise ValueError(f"Unknown message type {data.get('type')}")


# Derived SystemMessage class
class SystemMessage(LLMMessage):
    content: str
    type: str = "system"


# Base class for message content parts
class UserMessageContentPart(BaseModel):
    type: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        if data.get("type") == "text":
            return UserMessageText.model_validate(data)
        elif data.get("type") == "image_url":
            return UserMessageImageURL.model_validate(data)
        else:
            raise ValueError(f"Unknown message content part type {data.get('type')}")


# Derived classes for different types of message content parts
class UserMessageText(UserMessageContentPart):
    text: str
    type: str = "text"


class UserMessageImageURL(UserMessageContentPart):
    image_url: str
    type: str = "image_url"


# Derived UserMessage class
class UserMessage(LLMMessage):
    content: List[SerializeAsAny[UserMessageContentPart]]
    type: str = "user"

    @field_validator('content', mode="before")
    def validate_content(cls, value):
        if not isinstance(value, list):
            raise ValueError("content must be a list")
        ret_list = []
        for part in value:
            if isinstance(part, UserMessageContentPart):
                ret_list.append(part)
            elif isinstance(part, dict):
                ret_list.append(UserMessageContentPart.from_dict(part))
        return ret_list


# ToolCall class
class ToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any]


# Derived AssistantMessage class
class AssistantMessage(LLMMessage):
    content: Dict[str, Any]
    type: str = "assistant"
    tool_calls: Optional[List[ToolCall]]


# Derived ToolCallMessage class
class ToolCallMessage(LLMMessage):
    tool_calls: List[ToolCall]
    type: str = "tool"
