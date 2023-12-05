import logging
import os
from itertools import groupby
from typing import List, Dict

import yaml

from .agent_controller import AgentController
from .agent_memory import AgentMemory
from .resource_models import MachineResource, agent_resources, Resource, CPUResource
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
        resources = []
        for file in os.listdir(read_dir):
            file_loc = os.path.join(read_dir, file)
            with open(file_loc) as resource_yaml:
                resource_object = yaml.safe_load(resource_yaml)
                resources.append(Resource.model_validate(resource_object))

        grouped_resources: Dict[str, List[Resource]] = {k: list(xs) for k, xs in groupby(resources, lambda r: r.kind)}
        if not MachineResource.kind_literal() in grouped_resources:
            raise FileNotFoundError(f"Could not find Machine Resource in {read_dir}")
        machine = [machine.promote(MachineResource) for machine in grouped_resources.pop(MachineResource.kind_literal())].pop()
        cpus = {cpu.metadata.name: cpu.promote(CPUResource) for cpu in grouped_resources.pop(CPUResource.kind_literal())}
        agents = {}
        for kind, agent in ((k, a) for k, xs in grouped_resources.items() for a in xs):
            resource_model = agent_resources.get(kind)
            if not resource_model:
                raise ValueError(f'Unsupported kind "{kind}"')
            cpu = agent.spec.get('cpu', None)
            if not cpu and 'DEFAULT' in cpus:
                agent.spec['cpu'] = cpus['DEFAULT'].spec
            elif isinstance(cpu, str):
                if cpu not in cpus:
                    raise ValueError(f'Undefined cpu "{agent.spec.cpu}"')
                agent.spec['cpu'] = cpus[cpu].spec
            if agent.metadata.name in agents:
                logger.warning(f"Overwriting existing agent {agent.metadata.name}")
            agents[agent.metadata.name] = agent.promote(resource_model)
        memory = machine.spec.get_agent_memory()
        return AgentMachine(
            agent_memory=memory,
            agent_programs=[AgentController(p.metadata.name, p.instantiate(memory=memory)) for p in agents.values()]
        )
