from __future__ import annotations

from typing import List, Optional

from fastapi import FastAPI

from .agent_machine import AgentMachine


class AgentCallContext:
    conversation_id: str
    agent_name: str
    state_name: str


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

        self.machine.agent_memory.start()

    def stop(self):
        for process in self.processes:
            process.stop(self.app)
        self.processes = []
        self.machine.agent_memory.stop()

    def startProcess(self, callback_url: Optional[str]):
        return "123"

from .agent_process import AgentProcess
