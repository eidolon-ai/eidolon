import base64
from typing import List, Dict, Any, Literal

from pydantic import BaseModel

from eidolon_ai_client.events import ToolCall, FileHandle
from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DocumentParser, DataBlob
from eidolon_ai_sdk.agent_os import AgentOS


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


class UserMessageFileHandle(BaseModel):
    type: Literal["image", "audio", "file"]
    file: FileHandle


class UserMessageImage(UserMessageFileHandle):
    type: Literal["image"] = "image"

    def getBytes(self, process_id: str) -> bytes:
        data, _metadata = AgentOS.process_file_system.read_file(process_id, self.file.file_id)
        return data

    def getB64(self, process_id: str):
        data = self.getBytes(process_id)
        return base64.b64encode(data).decode("utf-8")


class UserMessageAudio(UserMessageFileHandle):
    type: Literal["audio"] = "audio"

    def getBytes(self, process_id: str) -> bytes:
        data, _metadata = AgentOS.process_file_system.read_file(process_id, self.file.file_id)
        return data

    def getB64(self, process_id: str):
        data = self.getBytes(process_id)
        return base64.b64encode(data).decode("utf-8")


class UserMessageFile(UserMessageFileHandle):
    type: Literal["file"] = "file"
    include_directly: bool

    def getDocParts(self, process_id: str, parser: DocumentParser):
        data, metadata = AgentOS.process_file_system.read_file(process_id, self.file.file_id)
        path = metadata.get("path") or metadata.get("filename") or None

        messages = []
        for doc in parser.parse(DataBlob.from_bytes(data=data, mimetype=metadata.get("mimetype"), path=path)):
            messages.append(doc.page_content)

        return messages


# Derived UserMessage class
class UserMessage(LLMMessage):
    type: str = "user"
    content: List[UserMessageText | UserMessageFileHandle]


# ToolCall class


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
