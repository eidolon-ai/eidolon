from typing import List, Union, Any

from jinja2 import Environment, StrictUndefined
from pydantic import BaseModel, validate_call

from eidolon_sdk.cpu.agent_bus import BusParticipant, Bus, BusEvent
from eidolon_sdk.cpu.llm_message import UserMessageText, SystemMessage, UserMessageImageURL, UserMessage


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

    def __init__(self, agent_cpu: "AgentCPU"):
        self.agent_cpu = agent_cpu

    async def bus_read(self, bus: Bus):
        if bus.current_event.event_type == "output_response":
            await self.agent_cpu.respond(bus.current_event.process_id, bus.current_event.event_data["response"])

    @validate_call
    def process_request(self, process_id: str, prompts: List[Union[UserTextCPUMessage, ImageURLCPUMessage, SystemCPUMessage]], input_data: dict[str, Any]):
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

        self.request_write(BusEvent(process_id, 0, "input_request", {"messages": event_prompts}))
