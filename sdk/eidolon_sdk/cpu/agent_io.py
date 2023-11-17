from abc import abstractmethod, ABC
from typing import List, Union, Any, Dict

from jinja2 import Environment, StrictUndefined
from pydantic import BaseModel, validate_call

from eidolon_sdk.cpu.agent_bus import BusParticipant, BusEvent, BusController
from eidolon_sdk.cpu.bus_messages import InputRequest
from eidolon_sdk.cpu.llm_message import UserMessageText, SystemMessage, UserMessageImageURL, UserMessage


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


class IOUnit(BusParticipant):
    env = Environment(undefined=StrictUndefined)
    response_handler: ResponseHandler = None

    def start(self, response_handler: ResponseHandler):
        self.response_handler = response_handler

    async def bus_read(self, event: BusEvent):
        if event.message.event_type == "output_response":
            print("output_response" + str(event.message.response))
            await self.response_handler.handle(event.process_id, event.message.response)

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
        self.request_write(BusEvent(process_id, 0, InputRequest(messages=event_prompts, output_format=output_format)))
