from typing import List, Dict, Any, Optional

from pydantic import BaseModel, SerializeAsAny, field_validator


# Base LLMMessage class
class LLMMessage(BaseModel):
    type: str
    is_boot_message: bool = False

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
    is_boot_message: bool = True


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
    type: str = "user"
    content: List[SerializeAsAny[UserMessageContentPart]]

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
    tool_call_id: str
    name: str
    arguments: Dict[str, Any]


# Derived AssistantMessage class
class AssistantMessage(LLMMessage):
    type: str = "assistant"
    content: Dict[str, Any]
    tool_calls: List[ToolCall]


class ToolResponseMessage(LLMMessage):
    type: str = "tool"
    tool_call_id: str
    result: str
