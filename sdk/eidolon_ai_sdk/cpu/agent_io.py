from __future__ import annotations

import asyncio
from abc import abstractmethod, ABC
from typing import List, Any, Dict, Literal

from pydantic import BaseModel

from eidolon_ai_client.events import FileHandle
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.llm_message import (
    UserMessageText,
    SystemMessage,
    UserMessage,
    LLMMessage,
    UserMessageFileHandle,
)
from eidolon_ai_sdk.cpu.processing_unit import ProcessingUnit


class ResponseHandler(ABC):
    @abstractmethod
    async def handle(self, process_id: str, response: Dict[str, Any]):
        pass


class APUMessage(BaseModel):
    type: str


class UserTextAPUMessage(APUMessage):
    type: Literal["user"] = "user"
    prompt: str
    is_boot_prompt: bool = False


class SystemAPUMessage(APUMessage):
    type: Literal["system"] = "system"
    is_boot_prompt: bool = True
    prompt: str


class AttachedFileMessage(APUMessage):
    type: Literal["image_url"] = "file"
    file: FileHandle
    include_directly: bool


CPUMessageTypes = UserTextAPUMessage | SystemAPUMessage | AttachedFileMessage


class IOUnit(ProcessingUnit):
    async def process_request(self, call_context: CallContext, prompts: List[CPUMessageTypes]) -> List[LLMMessage]:
        # convert the prompts to a list of strings
        conv_messages = []
        user_message_parts = []
        for prompt in prompts:
            if prompt.type == "user":
                user_message_parts.append(UserMessageText(text=prompt.prompt))
            elif prompt.type == "system":
                conv_messages.append(SystemMessage(content=prompt.prompt))
            elif prompt.type == "file":
                user_message_parts.append(
                    await UserMessageFileHandle.create(
                        file=prompt.file, process_id=call_context.process_id, include_directly=prompt.include_directly
                    )
                )
            else:
                raise ValueError(f"Unknown prompt type {prompt.type}")

        if len(user_message_parts) > 0:
            conv_messages.append(UserMessage(content=user_message_parts))

        return conv_messages

    async def process_response(self, call_context: CallContext, response: Any):
        return response

    @classmethod
    async def delete_process(cls, process_id: str):
        found = await AgentOS.file_memory.glob(f"uploaded_images/{process_id}/**/*")
        await asyncio.gather(*[AgentOS.file_memory.delete_file(file) for file in found])
