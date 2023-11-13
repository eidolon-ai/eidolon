from __future__ import annotations

from typing import List, Optional

from fastapi import FastAPI

import eidolon_sdk
from .agent import Agent
from .agent_machine import AgentMachine
from .agent_program import AgentProgram


def find_agent(model: AgentProgram) -> Agent:
    # todo, we should probably do some validation here
    return getattr(eidolon_sdk, model.implementation)


class AgentOS:
    machine: AgentMachine
    app: FastAPI = None
    processes: List[AgentProcess]

    def __init__(self, machine_yaml: str, machine: Optional[AgentMachine] = None):
        self.machine = machine or AgentMachine.parse(machine_yaml)
        self.processes = []

    def start(self, app: FastAPI):
        self.app = app
        self.processes = [AgentProcess(program, self) for program in self.machine.agent_programs]
        for process in self.processes:
            process.start(app)

    def stop(self):
        for process in self.processes:
            process.stop(self.app)
        self.processes = []

    def startProcess(self, callback_url: str):
        return "123"

from .agent_process import AgentProcess
