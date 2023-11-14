from typing import List, Dict, Any

from pydantic import BaseModel


class LLMMessage(BaseModel):
    type: str


class SystemMessage(LLMMessage):
    content: str
    role: str = "system"


class UserMessageContentPart(BaseModel):
    type: str


class UserMessageText(UserMessageContentPart):
    text: str
    type: str = "text"


class UserMessageImageURL(UserMessageContentPart):
    image_url: str
    type: str = "image_url"


class UserMessage(LLMMessage):
    content: List[UserMessageContentPart]
    role: str = "user"


class ToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any]


class AssistantMessage(LLMMessage):
    content: str
    role: str = "assistant"
    tool_calls: List[ToolCall]


class ToolCallMessage(LLMMessage):
    tool_calls: List[ToolCall]
    role: str = "tool"
