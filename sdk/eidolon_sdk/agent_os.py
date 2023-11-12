from __future__ import annotations

from typing import TypeVar

from fastapi import FastAPI

import eidolon_sdk
from agent import Agent
from agent_process import AgentProcess
from agent_machine import AgentMachine
from agent_program import AgentProgram

T = TypeVar('T')
V = TypeVar('V')

myDict = {
    "/route1": {
        "input_schema": {
            "title": "Route1Input",
            "type": "object",
            "properties": {
                "question": {
                    "title": "Question",
                    "description": "The question to ask the user.",
                    "type": "string"
                }
            },
            "required": ["question"]
        },
        "output_schema": {
            "title": "Route1Output",
            "type": "object",
            "properties": {
                "answer": {
                    "title": "Answer",
                    "description": "The answer to the question.",
                    "type": "string"
                }
            },
            "required": ["answer"]
        }
    },
    "/route2": {
        "input_schema": {
            "title": "Route1Input",
            "type": "object",
            "properties": {
                "question": {
                    "title": "Question",
                    "description": "The question to ask the user.",
                    "type": "string"
                }
            },
            "required": ["question"]
        },
        "output_schema": {
            "title": "Route1Output",
            "type": "object",
            "properties": {
                "answer": {
                    "title": "Answer",
                    "description": "The answer to the question.",
                    "type": "string"
                }
            },
            "required": ["answer"]
        }
    },

}


def find_agent(model: AgentProgram) -> Agent:
    # todo, we should probably do some validation here
    return getattr(eidolon_sdk, model.implementation)


class AgentOS:
    machine: AgentMachine
    app: FastAPI
    processes: list[AgentProcess]

    def __init__(self, machine_yaml: str):
        self.machine = AgentMachine.parse(machine_yaml)

    def start(self):
        self.app = FastAPI()
        self.processes = [AgentProcess(program) for program in self.machine.agent_programs]
        for process in self.processes:
            process.start(self.app)

