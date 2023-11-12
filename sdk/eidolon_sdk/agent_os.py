from __future__ import annotations

from typing import TypeVar, Type

from fastapi import FastAPI, Body

from .agent_machine import AgentMachine
from .agent_program import AgentProgram

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


class Agent:
    pass


def create_endpoint(model: Type[AgentProgram]):
    async def endpoint(body: model = Body(...)):
        return body

    return endpoint


class AgentOS:
    machine: AgentMachine = None

    def initialize(self, machine_yaml: str):
        self.machine = AgentMachine.parse(machine_yaml)

    def start(self):
        app = FastAPI()

        # Register a POST endpoint for each Pydantic model in the dictionary
        for program in self.machine.agent_programs:
            endpoint = create_endpoint(program)
            app.add_api_route(f"/{name}", endpoint, methods=["POST"])

        pass
