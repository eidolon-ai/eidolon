from typing import List

import yaml
from pydantic import Field, BaseModel

from .agent_io import AgentIO
from .agent_memory import AgentMemory
from .agent_program import AgentProgram
from .machine_model import MachineModel

base_class_dict = {
    "agent_memory": AgentMemory,
    "agent_io": AgentIO,
}


class AgentMachine(BaseModel):
    agent_memory: AgentMemory = Field(default=..., description="The Agent Memory to use.")
    agent_programs: List[AgentProgram] = Field(..., description="The list of Agent Programs to run on this machine.")


class YamlAgentMachine(AgentMachine):
    def __init__(self, machine_description: str):
        """
        Parses a YAML string describing an AgentMachine into an AgentMachine instance.

        Args:
            machine_description (str): A string in YAML format that describes the
                configuration and components of the AgentMachine.

        Returns:
            AgentMachine: An instantiated AgentMachine object based on the parsed
                description.
        """

        machine_descriptor = yaml.safe_load(machine_description)
        model = MachineModel(**machine_descriptor)
        super().__init__(
            agent_memory={k: v.get_reference_class(
                **({'spec': v.build_reference_spec()} if v.build_reference_spec() is None else {})
            ) for k, v in model.agent_memory.__dict__.items()},
            agent_programs=[AgentProgram(
                name=program.name,
                agent_cpu=program.cpu,
                agent={k: v.get_reference_class(
                    **({'machine': self, 'spec': v.build_reference_spec()} if v.build_reference_spec() is None else {'machine': self})
                ) for k, v in program.agent.__dict__.items()}
            ) for program in model.agent_programs]
        )
