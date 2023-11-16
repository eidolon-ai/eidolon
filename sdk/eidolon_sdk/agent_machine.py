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


class AgentMachine:
    agent_memory: AgentMemory
    agent_programs: List[AgentProgram]

    def __init__(self, agent_memory: AgentMemory, agent_programs: List[AgentProgram]):
        self.agent_memory = agent_memory
        self.agent_programs = agent_programs

    @staticmethod
    def from_yaml(machine_yaml):
        model = MachineModel(**(yaml.safe_load(machine_yaml)))
        machine = AgentMachine(
            agent_memory=AgentMemory(**{k: v.instantiate() for k, v in model.agent_memory.__dict__.items()}),
            agent_programs=[]
        )
        machine.agent_programs = [AgentProgram(
            name=program.name,
            agent=program.agent.instantiate(agent_machine=machine)
            # todo add cpu
        ) for program in model.agent_programs]
        return machine
