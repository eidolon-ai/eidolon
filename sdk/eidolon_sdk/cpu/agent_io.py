from abc import abstractmethod, ABC
from typing import List, Union, Any, Dict

from jinja2 import Environment, StrictUndefined
from pydantic import BaseModel, validate_call, Field

from eidolon_sdk.cpu.agent_bus import BusEvent, CallContext
from eidolon_sdk.cpu.processing_unit import ProcessingUnit
from eidolon_sdk.cpu.bus_messages import WRITE_PORT
from eidolon_sdk.cpu.llm_message import UserMessageText, SystemMessage, UserMessageImageURL, UserMessage
from eidolon_sdk.cpu.memory_unit import MemoryUnitConfig
from eidolon_sdk.reference_model import Specable


class ResponseHandler(ABC):
    @abstractmethod
    async def handle(self, process_id: str, response: Dict[str, Any]):
        pass


class CPUMessage(BaseModel):
    type: str
    prompt: str


class UserTextCPUMessage(CPUMessage):
    type: str = "user"


class SystemCPUMessage(CPUMessage):
    type: str = "system"


class ImageURLCPUMessage(CPUMessage):
    type: str = "image_url"


class IOUnitConfig(BaseModel):
    io_write: WRITE_PORT = Field(description="A port that, when bound to an event, will write the input request to the event bus.")
    io_read: WRITE_PORT = Field(description="A port that, when bound to an event, will read the output response from the event bus.")
    pass


class IOUnit(ProcessingUnit, Specable[IOUnitConfig]):
    env = Environment(undefined=StrictUndefined)
    response_handler: ResponseHandler = None

    def __init__(self, spec: MemoryUnitConfig = None):
        self.spec = spec

    def start(self, response_handler: ResponseHandler):
        self.response_handler = response_handler

    async def bus_read(self, event: BusEvent):
        if event.event_type == self.spec.io_read:
            # todo -- should we assert this? We are assuming this is an AssistantMessage
            await self.process_response(event.call_context.process_id, event.messages[0].content)

    @validate_call
    def process_request(self, process_id: str, prompts: List[Union[UserTextCPUMessage, ImageURLCPUMessage, SystemCPUMessage]], input_data: Dict[str, Any],
                        output_format: Dict[str, Any]):
        # convert the prompts to a list of strings
        event_prompts = []
        user_message_parts = []
        for prompt in prompts:
            converted_prompt = self.env.from_string(prompt.prompt).render(**input_data)
            if prompt.type == "user":
                user_message_parts.append(UserMessageText(text=converted_prompt))
            elif prompt.type == "system":
                event_prompts.append(SystemMessage(content=prompt.prompt))
            elif prompt.type == "image_url":
                user_message_parts.append(UserMessageImageURL(image_url=converted_prompt))
            else:
                raise ValueError(f"Unknown prompt type {prompt.type}")

        if len(user_message_parts) > 0:
            event_prompts.append(UserMessage(content=user_message_parts))

        print("event_prompts" + str(event_prompts))
        self.request_write(BusEvent(CallContext(process_id, 0, output_format), self.spec.io_write, event_prompts))

    async def process_response(self, process_id: str, response: Dict[str, Any]):
        await self.response_handler.handle(process_id, response)
