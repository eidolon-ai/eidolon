import logging
from typing import List

import yaml
from pydantic import ValidationError

from .agent_memory import AgentMemory
from .agent_program import AgentProgram
from .machine_model import MachineModel


class AgentMachine:
    agent_memory: AgentMemory
    agent_programs: List[AgentProgram]

    def __init__(self, agent_memory: AgentMemory, agent_programs: List[AgentProgram]):
        self.agent_memory = agent_memory
        self.agent_programs = agent_programs
        self.logger = logging.getLogger("eidolon")

    @staticmethod
    def from_yaml(machine_yaml):
        try:
            model = MachineModel(**(yaml.safe_load(machine_yaml)))
            memory = AgentMemory(**{k: v.instantiate() for k, v in model.agent_memory.__dict__.items()})
            machine = AgentMachine(agent_memory=memory, agent_programs=[])

            machine.agent_programs = [
                AgentProgram(name=name, agent=program.agent.instantiate(
                    agent_machine=machine, cpu=_make_cpu(program.cpu, machine)
                )) for name, program in model.agent_programs.items()
            ]
            return machine
        except ValidationError as e:
            logger = logging.getLogger("eidolon")
            logger.exception("Invalid machine model")
            raise Exception(f"Invalid machine model: {e}")


def _make_cpu(cpu_model, machine):
    try:
        return cpu_model.instantiate(agent_memory=machine.agent_memory)
    except Exception as e:
        logger = logging.getLogger("eidolon")
        logger.exception(f"Failed to make cpu {cpu_model}")
        raise e
