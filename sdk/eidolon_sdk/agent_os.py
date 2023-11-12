from __future__ import annotations

from typing import TypeVar, Type, Callable, Any

from fastapi import FastAPI, Body
from pydantic import BaseModel

import eidolon_sdk
from agent import Agent
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


class AgentProcess:
    def __init__(self, agent_program: AgentProgram):
        self.agent_program = agent_program

    def start(self):
        pass

    def stop(self):
        pass

    def restart(self):
        pass


def find_agent(model: AgentProgram) -> Agent:
    # todo, we should probably do some validation here
    return getattr(eidolon_sdk, model.implementation)


class AgentOS:
    machine: AgentMachine
    app: FastAPI

    def __init__(self, machine_yaml: str):
        self.machine = AgentMachine.parse(machine_yaml)

    def start(self):
        app = FastAPI()

        def create_endpoint(model: Type[BaseModel], fn: Callable[..., Any]):
            async def endpoint(body: model = Body(...)):
                return fn(**body.model_dump())

            return endpoint

        # Register a POST endpoint for each Pydantic model in the dictionary
        for program in self.machine.agent_programs:
            agent = find_agent(program)
            app.add_api_route(f"/{program.name}", create_endpoint(program.states[program.initial_state].input_schema_model, agent.state_mapping[agent.starting_state]),
                              methods=["POST"])
            for state_name, state in program.states.items():
                app.add_api_route(f"/{program.name}/{state_name}", create_endpoint(state.input_schema_model, agent.state_mapping[state_name]), methods=["POST"])

        self.app = app
