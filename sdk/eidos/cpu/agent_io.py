from __future__ import annotations

from abc import abstractmethod, ABC
from typing import List, Any, Dict, Literal

from pydantic import BaseModel, validate_call

from eidos.cpu.call_context import CallContext
from eidos.cpu.llm_message import UserMessageText, SystemMessage, UserMessageImageURL, UserMessage
from eidos.cpu.processing_unit import ProcessingUnit


class ResponseHandler(ABC):
    @abstractmethod
    async def handle(self, process_id: str, response: Dict[str, Any]):
        pass


class CPUMessage(BaseModel):
    type: str
    prompt: str
    is_boot_prompt: bool = False


class UserTextCPUMessage(CPUMessage):
    type: Literal['user'] = "user"


class SystemCPUMessage(CPUMessage):
    type: Literal['system'] = "system"
    is_boot_prompt: bool = True


class ImageURLCPUMessage(CPUMessage):
    type: Literal['image_url'] = "image_url"


CPUMessageTypes = UserTextCPUMessage | SystemCPUMessage | ImageURLCPUMessage


class IOUnit(ProcessingUnit):
    @validate_call
    async def process_request(self, prompts: List[CPUMessageTypes]):
        # convert the prompts to a list of strings
        conv_message = []
        user_message_parts = []
        for prompt in prompts:
            if prompt.type == "user":
                user_message_parts.append(UserMessageText(text=prompt.prompt))
            elif prompt.type == "system":
                conv_message.append(SystemMessage(content=prompt.prompt))
            elif prompt.type == "image_url":
                user_message_parts.append(UserMessageImageURL(image_url=prompt.prompt))
            else:
                raise ValueError(f"Unknown prompt type {prompt.type}")

        if len(user_message_parts) > 0:
            conv_message = UserMessage(content=user_message_parts)

        return conv_message

    @validate_call
    async def process_response(self, call_context: CallContext, response: Dict[str, Any]):
        return response
