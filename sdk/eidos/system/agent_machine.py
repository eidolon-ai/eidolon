import os
from collections import defaultdict
from contextlib import contextmanager
from typing import List, Dict

import yaml

from eidos.memory.agent_memory import AgentMemory
from eidos.util.logger import logger
from .agent_controller import AgentController
from .resource_models import MachineResource, agent_resources, Resource, CPUResource


class AgentMachine:
    memory: AgentMemory
    agent_controllers: List[AgentController]
    cpus: Dict[str, CPUResource]

    def __init__(self, agent_memory: AgentMemory, agent_programs: List[AgentController] = None, cpus=None):
        self.memory = agent_memory
        self.cpus = cpus or {}
        self.agent_controllers = agent_programs or []
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
        source_map = {}
        resources: List[Resource] = []
        for file in os.listdir(read_dir):
            file_loc = os.path.join(read_dir, file)
            with open(file_loc) as resource_yaml:
                resource_object = yaml.safe_load(resource_yaml)
                resource = Resource.model_validate(resource_object)
                source_map[(resource.kind, resource.metadata.name)] = file_loc
                resources.append(resource)

        grouped_resources = defaultdict(list)
        for r in resources:
            grouped_resources[r.kind].append(r)
        if not MachineResource.kind_literal() in grouped_resources:
            raise FileNotFoundError(f"Could not find Machine Resource in {read_dir}")
        resource = grouped_resources.pop(MachineResource.kind_literal()).pop()
        with _error_wrapper(resource, source_map):
            machine = resource.promote(MachineResource)
        cpus = {
            r.metadata.name: _error_wrapped_fn(r, source_map, lambda: r.promote(CPUResource))
            for r in grouped_resources.pop(CPUResource.kind_literal())
        } if CPUResource.kind_literal() in grouped_resources else {}

        agents = {}
        for kind, agent in ((k, a) for k, xs in grouped_resources.items() for a in xs):
            with _error_wrapper(agent, source_map):
                resource_model = agent_resources.get(kind)
                if not resource_model:
                    raise ValueError(f'Unsupported kind "{kind}"')
                if agent.metadata.name in agents:
                    logger.warning(f"Overwriting existing agent {agent.metadata.name}")
                agents[agent.metadata.name] = agent.promote(resource_model)

        return AgentMachine(
            agent_memory=(machine.spec.get_agent_memory()),
            agent_programs=[AgentController(p) for p in agents.values()],
            cpus=cpus,
        )


@contextmanager
def _error_wrapper(resource: Resource, source_map):
    try:
        yield
    except Exception as e:
        raise ValueError(f"Error building resource {source_map[(resource.kind, resource.metadata.name)]}") from e


def _error_wrapped_fn(resource, source_map, fn):
    with _error_wrapper(resource, source_map):
        return fn()
