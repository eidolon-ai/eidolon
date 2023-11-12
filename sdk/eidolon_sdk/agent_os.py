from __future__ import annotations

from typing import TypeVar

from fastapi import FastAPI

import eidolon_sdk
from agent_cpu import Agent
from eidolon_sdk.agent_machine import AgentMachine
from eidolon_sdk.agent_program import AgentProgram

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

    def __init__(self, machine_yaml: str):
        self.machine = AgentMachine.parse(machine_yaml)

    def start(self):
        app = FastAPI()

        # Register a POST endpoint for each Pydantic model in the dictionary
        for program in self.machine.agent_programs:
            agent = find_agent(program)
            app.add_api_route(f"/{program.name}", agent.state_mapping[agent.starting_state], methods=["POST"])
            for state, function in agent.state_mapping.items():
                app.add_api_route(f"/{program.name}/{state}", function, methods=["POST"])
