from typing import List

import yaml
from pydantic import Field, BaseModel, field_validator

from eidolon_sdk.agent_memory import AgentMemory
from eidolon_sdk.agent_program import AgentProgram
from eidolon_sdk.agent_io import AgentIO

base_class_dict = {
    "agent_memory": AgentMemory,
    "agent_io": AgentIO,
}


class AgentMachine(BaseModel):
    agent_memory: AgentMemory = Field(..., description="The Agent Memory to use.")
    agent_io: AgentIO = Field(..., description="The Agent IO configured on this machine.")
    agent_programs: List[AgentProgram] = Field(..., description="The list of Agent Programs to run on this machine.")

    @classmethod
    @field_validator('agent_memory', 'agent_io')
    def validate_units(cls, value, field):
        if 'implementation' in value:
            base_class = base_class_dict.get(field.name)
            implementation_class = globals().get(value['implementation'])
            if implementation_class and issubclass(implementation_class, base_class):
                return implementation_class()
            else:
                raise ValueError(f"Implementation class '{value['implementation']}' not found or is not a subclass of {field.name}.")
        raise ValueError("Implementation not provided.")

    @staticmethod
    def parse(machine_description: str):
        machine_descriptor = yaml.safe_load(machine_description)
        return AgentMachine(**machine_descriptor)

