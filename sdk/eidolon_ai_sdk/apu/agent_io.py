from __future__ import annotations

from typing import List, Any, Literal

from pydantic import BaseModel, Field

from eidolon_ai_client.events import FileHandle
from eidolon_ai_sdk.apu.call_context import CallContext
from eidolon_ai_sdk.apu.llm_message import (
    UserMessageText,
    SystemMessage,
    UserMessage,
    LLMMessage,
    UserMessageFileHandle,
)
from eidolon_ai_sdk.apu.processing_unit import ProcessingUnit


class APUMessage(BaseModel):
    """
    Base message type for APU input
    """

    type: str


class UserTextAPUMessage(APUMessage):
    """
    A user message to the APU.
    """

    type: Literal["user"] = "user"
    prompt: str


class SystemAPUMessage(APUMessage):
    """
    A system message to the APU
    """

    type: Literal["system"] = "system"
    prompt: str


class FileHandleWithInclude(FileHandle):
    include_directly: bool = Field(default=True, description="Include the file directly in the llm context")


class AttachedFileMessage(APUMessage):
    """
    A file attachment message to the APU.
    """

    type: Literal["image_url"] = "file"
    file: FileHandle
    include_directly: bool


APUMessageTypes = UserTextAPUMessage | SystemAPUMessage | AttachedFileMessage


class IOUnit(ProcessingUnit):
    """
    This is the IO unit for the APU. It is responsible for converting the prompts from the User to the LLM

    This can be overridden to provide custom IO handling.
    """

    async def process_request(self, call_context: CallContext, prompts: List[APUMessageTypes]) -> List[LLMMessage]:
        """
        Converts the external prompts to the internal LLM messages.

        :param call_context: The current call context including process id and thread id.
        :param prompts: The prompts to send to the LLM
        :return: A list of LLM messages
        """
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
        """
        Converts the LLM response to the external response. Base implementation just returns the response but can be overridden to provide custom response handling.
        :param call_context: The current call context including process id and thread id.
        :param response: The response from the LLM
        :return: The converted response
        """

        return response
