from typing import List, Dict, Any, Optional

from pydantic import BaseModel, Field


# Base LLMMessage class
class LLMMessage(BaseModel):
    type: str


# Derived SystemMessage class
class SystemMessage(LLMMessage):
    content: str
    type: str = "system"


# Base class for message content parts
class UserMessageContentPart(BaseModel):
    type: str


# Derived classes for different types of message content parts
class UserMessageText(UserMessageContentPart):
    text: str
    type: str = "text"


class UserMessageImageURL(UserMessageContentPart):
    image_url: str
    type: str = "image_url"


# Derived UserMessage class
class UserMessage(LLMMessage):
    content: List[UserMessageContentPart]
    type: str = "user"


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
