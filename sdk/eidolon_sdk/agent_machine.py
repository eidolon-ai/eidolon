import logging
import os
from typing import List

import yaml

from .agent_controller import AgentController
from .agent_memory import AgentMemory
from .resource_models import MachineResource, resources
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
            with open(file_loc) as resource_yaml:
                resource_object = yaml.safe_load(resource_yaml)
                kind = resource_object.get('kind')
                resource_model = resources.get(kind)
                if not resource_model:
                    raise ValueError(f'Unsupported kind "{kind}" not in resource list {resources.keys()}')
                try:
                    resource = resource_model.model_validate(resource_object)
                    if isinstance(resource, MachineResource):
                        machine = resource
                    else:
                        if resource.metadata.name in programs:
                            logger.warning(f"Overwriting existing program {resource.metadata.name}")
                        programs[resource.metadata.name] = resource
                except Exception as e:
                    raise ValueError(f"Error parsing {file_loc}") from e

        if not machine:
            raise FileNotFoundError(f"Could not find Machine Resource in {read_dir}")
        memory = machine.spec.get_agent_memory()
        return AgentMachine(
            agent_memory=memory,
            agent_programs=[AgentController(p.metadata.name, p.instantiate(memory=memory)) for p in programs.values()]
        )
