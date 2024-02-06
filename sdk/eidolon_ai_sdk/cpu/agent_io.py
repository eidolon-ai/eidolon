from __future__ import annotations

import uuid
from abc import abstractmethod, ABC
from io import IOBase
from typing import List, Any, Dict, Literal

from pydantic import BaseModel

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.llm_message import (
    UserMessageText,
    SystemMessage,
    UserMessageImageURL,
    UserMessage,
    LLMMessage,
)
from eidolon_ai_sdk.cpu.processing_unit import ProcessingUnit


class ResponseHandler(ABC):
    @abstractmethod
    async def handle(self, process_id: str, response: Dict[str, Any]):
        pass


class CPUMessage(BaseModel):
    type: str
    prompt: str
    is_boot_prompt: bool = False


class UserTextCPUMessage(CPUMessage):
    type: Literal["user"] = "user"


class SystemCPUMessage(CPUMessage):
    type: Literal["system"] = "system"
    is_boot_prompt: bool = True


class ImageCPUMessage(CPUMessage):
    type: Literal["image_url"] = "image"
    image: IOBase

    class Config:
        arbitrary_types_allowed = True


CPUMessageTypes = UserTextCPUMessage | SystemCPUMessage | ImageCPUMessage


class IOUnit(ProcessingUnit):
    async def process_request(self, prompts: List[CPUMessageTypes]) -> List[LLMMessage]:
        # convert the prompts to a list of strings
        conv_messages = []
        user_message_parts = []
        for prompt in prompts:
            if prompt.type == "user":
                user_message_parts.append(UserMessageText(text=prompt.prompt))
            elif prompt.type == "system":
                conv_messages.append(SystemMessage(content=prompt.prompt))
            elif prompt.type == "image":
                file_memory = AgentOS.file_memory
                image_file: IOBase = prompt.image
                # read the prompt.image file into memory
                image_data = image_file.read()
                tmp_path = "uploaded_images/" + str(uuid.uuid4())
                file_memory.mkdir("uploaded_images", True)
                file_memory.write_file(tmp_path, image_data)
                user_message_parts.append(UserMessageImageURL(image_url=tmp_path))
            else:
                raise ValueError(f"Unknown prompt type {prompt.type}")

        if len(user_message_parts) > 0:
            conv_messages.append(UserMessage(content=user_message_parts))

        return conv_messages

    async def process_response(self, call_context: CallContext, response: Any):
        return response
