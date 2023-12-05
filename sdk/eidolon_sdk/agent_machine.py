import logging
import os
from typing import List

import yaml

from .agent_controller import AgentController
from .agent_memory import AgentMemory
from .resourece_models import AgentResource, MachineResource
from .util.logger import logger


class AgentMachine:
    memory: AgentMemory
    agent_controllers: List[AgentController]

    def __init__(self, agent_memory: AgentMemory, agent_programs: List[AgentController] = None):
        self.memory = agent_memory
        self.agent_controllers = agent_programs or []
        self.logger = logging.getLogger("eidolon")
        self.app = None

    async def start(self, app):
        if self.app:
            raise Exception("Machine already started")
        for program in self.agent_controllers:
            await program.start(app)
        self.memory.start()
        self.app = app

    def stop(self):
        if self.app:
            for program in self.agent_controllers:
                program.stop(self.app)
            self.memory.stop()
            self.app = None

    @staticmethod
    def from_dir(read_dir: str):
        machine = None
        programs = {}
        for file in os.listdir(read_dir):
            file_loc = os.path.join(read_dir, file)
            with open(file_loc) as stream:
                resource_yaml = yaml.safe_load(stream)
                try:
                    if resource_yaml.get('type') == 'eidolon/machine':
                        machine = MachineResource.model_validate(resource_yaml)
                    else:
                        program = AgentResource.model_validate(resource_yaml)
                        if program.metadata.name in programs:
                            logger.warning(f"Overwriting existing program {program.metadata.name}")
                        programs[program.metadata.name] = program
                except Exception as e:
                    raise ValueError(f"Error parsing {file_loc}") from e

        if not machine:
            raise FileNotFoundError(f"Could not find Machine Resource in {read_dir}")
        memory = machine.spec.to_agent_memory()
        return AgentMachine(
            agent_memory=memory,
            agent_programs=[AgentController(p.metadata.name, p.instantiate(memory=memory)) for p in programs.values()]
        )
