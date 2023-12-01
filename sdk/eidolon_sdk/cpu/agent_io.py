from __future__ import annotations

from abc import abstractmethod, ABC
from typing import List, Any, Dict, Literal

from pydantic import BaseModel, validate_call

from eidolon_sdk.cpu.call_context import CallContext
from eidolon_sdk.cpu.llm_message import UserMessageText, SystemMessage, UserMessageImageURL, UserMessage
from eidolon_sdk.cpu.processing_unit import ProcessingUnit


class ResponseHandler(ABC):
    @abstractmethod
    async def handle(self, process_id: str, response: Dict[str, Any]):
        pass


class CPUMessage(BaseModel):
    type: str
    prompt: str
    is_boot_prompt: str = False


class UserTextCPUMessage(CPUMessage):
    type: Literal['user'] = "user"


class SystemCPUMessage(CPUMessage):
    type: Literal['system'] = "system"
    is_boot_prompt: str = True


class ImageURLCPUMessage(CPUMessage):
    type: Literal['image_url'] = "image_url"


CPUMessageTypes = UserTextCPUMessage | SystemCPUMessage | ImageURLCPUMessage


class IOUnit(ProcessingUnit):
    @validate_call
    async def process_request(self, prompts: List[CPUMessageTypes]):
        # convert the prompts to a list of strings
        boot_event_prompts = []
        boot_user_message_parts = []
        conv_user_message_parts = []
        for prompt in prompts:
            if prompt.type == "user":
                if prompt.is_boot_prompt:
                    boot_user_message_parts.append(UserMessageText(text=prompt))
                else:
                    conv_user_message_parts.append(UserMessageText(text=prompt))
            elif prompt.type == "system":
                boot_event_prompts.append(SystemMessage(content=prompt))
            elif prompt.type == "image_url":
                if prompt.is_boot_prompt:
                    boot_user_message_parts.append(UserMessageImageURL(image_url=prompt))
                else:
                    conv_user_message_parts.append(UserMessageImageURL(image_url=prompt))
            else:
                raise ValueError(f"Unknown prompt type {prompt.type}")

        if len(boot_user_message_parts) > 0:
            boot_event_prompts.append(UserMessage(content=boot_user_message_parts))

        conv_message = []
        if len(conv_user_message_parts) > 0:
            conv_message = UserMessage(content=conv_user_message_parts)

        return boot_event_prompts, conv_message

    @validate_call
    async def process_response(self, call_context: CallContext, response: Dict[str, Any]):
        return response
