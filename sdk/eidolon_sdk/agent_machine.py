from typing import List

import yaml

from .agent import Agent
from .agent_memory import AgentMemory
from .agent_program import AgentProgram
from .cpu.agent_cpu import AgentCPU
from .machine_model import MachineModel


class AgentMachine:
    agent_memory: AgentMemory
    agent_programs: List[AgentProgram]

    def __init__(self, agent_memory: AgentMemory, agent_programs: List[AgentProgram]):
        self.agent_memory = agent_memory
        self.agent_programs = agent_programs

    @staticmethod
    def from_yaml(machine_yaml):
        model = MachineModel(**(yaml.safe_load(machine_yaml)))
        memory = AgentMemory(**{k: v.instantiate() for k, v in model.agent_memory.__dict__.items()})
        machine = AgentMachine(agent_memory=memory, agent_programs=[])
        machine.agent_programs = [
            AgentProgram(name=name, agent=(program.agent.instantiate(agent_machine=machine, cpu=AgentCPU(agent_machine=machine))))
            for name, program in model.agent_programs.items()
        ]
        return machine
