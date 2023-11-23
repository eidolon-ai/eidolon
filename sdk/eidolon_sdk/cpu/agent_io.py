from abc import abstractmethod, ABC
from typing import List, Union, Any, Dict

from jinja2 import Environment, StrictUndefined
from pydantic import BaseModel, validate_call

from eidolon_sdk.cpu.call_context import CallContext
from eidolon_sdk.cpu.llm_message import UserMessageText, SystemMessage, UserMessageImageURL, UserMessage
from eidolon_sdk.cpu.processing_unit import ProcessingUnit
from eidolon_sdk.reference_model import Specable


class ResponseHandler(ABC):
    @abstractmethod
    async def handle(self, process_id: str, response: Dict[str, Any]):
        pass


class CPUMessage(BaseModel):
    type: str
    prompt: str
    is_boot_prompt: str = False


class UserTextCPUMessage(CPUMessage):
    type: str = "user"


class SystemCPUMessage(CPUMessage):
    type: str = "system"
    is_boot_prompt: str = True


class ImageURLCPUMessage(CPUMessage):
    type: str = "image_url"


class IOUnitConfig(BaseModel):
    pass


class IOUnit(ProcessingUnit, Specable[IOUnitConfig]):
    env = Environment(undefined=StrictUndefined)

    @validate_call
    async def process_request(self, call_context: CallContext, prompts: List[Union[UserTextCPUMessage, ImageURLCPUMessage, SystemCPUMessage]], input_data: Dict[str, Any]):
        # convert the prompts to a list of strings
        boot_event_prompts = []
        boot_user_message_parts = []
        conv_user_message_parts = []
        for prompt in prompts:
            converted_prompt = self.env.from_string(prompt.prompt).render(**input_data)
            if prompt.type == "user":
                if prompt.is_boot_prompt:
                    boot_user_message_parts.append(UserMessageText(text=converted_prompt))
                else:
                    conv_user_message_parts.append(UserMessageText(text=converted_prompt))
            elif prompt.type == "system":
                boot_event_prompts.append(SystemMessage(content=converted_prompt))
            elif prompt.type == "image_url":
                if prompt.is_boot_prompt:
                    boot_user_message_parts.append(UserMessageImageURL(image_url=converted_prompt))
                else:
                    conv_user_message_parts.append(UserMessageImageURL(image_url=converted_prompt))
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
