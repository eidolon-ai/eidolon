from typing import Any, Union, List

from jinja2 import Environment
from pydantic import BaseModel

from eidolon_sdk.agent_machine import AgentMachine
from eidolon_sdk.cpu.agent_bus import BusController, BusEvent, BusParticipant, Bus
from eidolon_sdk.cpu.llm_message import UserMessage, SystemMessage, UserMessageText, UserMessageImageURL
from eidolon_sdk.cpu.memory_unit import MemoryUnit, ConversationalMemoryUnit


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
    env = Environment()

    def __init__(self, agent_machine: AgentMachine):
        self.agent_machine = agent_machine

    async def bus_read(self, bus: Bus):
        # todo: process response
        pass

    def process_request(self, process_id: str, prompts: List[Union[UserTextCPUMessage, ImageURLCPUMessage, SystemCPUMessage]], input_data: dict[str, Any]):
        # convert the prompts to a list of strings
        event_prompts = []
        user_message_parts = []
        for prompt in prompts:
            converted_prompt = self.env.from_string(prompt.prompt).render(**input_data)
            if prompt.type == "user":
                user_message_parts.append(UserMessageText(text = converted_prompt))
            elif prompt.type == "system":
                event_prompts.append(SystemMessage(content=prompt.prompt))
            elif prompt.type == "image_url":
                user_message_parts.append(UserMessageImageURL(image_url=converted_prompt))
            else:
                raise ValueError(f"Unknown prompt type {prompt.type}")

        if len(user_message_parts) > 0:
            event_prompts.append(UserMessage(content=user_message_parts))

        self.request_write(BusEvent(process_id, 0, "input_request", {"messages": event_prompts}))


class AgentCPU:
    bus_controller: BusController = BusController()
    io_unit: IOUnit
    memory_unit: MemoryUnit

    def __init__(self, agent_machine: AgentMachine):
        self.agent_machine = agent_machine
        self.io_unit = IOUnit(agent_machine)
        self.memory_unit = ConversationalMemoryUnit(agent_machine)

    def schedule_request(self, process_id: str, prompts: List[Union[UserTextCPUMessage, ImageURLCPUMessage, SystemCPUMessage]], input_data: dict[str, Any]):
        self.io_unit.process_request(process_id, prompts, input_data)
