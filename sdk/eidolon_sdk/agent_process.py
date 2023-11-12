from __future__ import annotations

import importlib
from typing import Type, Callable, Any

from fastapi import FastAPI, Body
from pydantic import ValidationError, BaseModel

from agent import Agent
from agent_program import AgentProgram


class AgentProcess:
    agent: Agent

    def __init__(self, agent_program: AgentProgram):
        self.agent_program = agent_program

    def start(self, app: FastAPI):
        # First create the Agent implementation
        module_name, class_name = self.agent_program.implementation.rsplit(".", 1)
        try:
            module = importlib.import_module(module_name)
            impl_class = getattr(module, class_name)
        except (ImportError, AttributeError):
            raise ValidationError(f"Unable to import {self.agent_program.implementation}")

        self.agent = impl_class()

        # Then create the endpoints
        def create_endpoint(model: Type[BaseModel], fn: Callable[..., Any]):
            async def endpoint(body: model = Body(...)):
                return fn(**body.model_dump())

            return endpoint

        program = self.agent_program
        # Register a POST endpoint for each Pydantic model in the dictionary
        app.add_api_route(f"/{program.name}", create_endpoint(program.states[program.initial_state].input_schema_model, self.agent.state_mapping[self.agent.starting_state]),
                          methods=["POST"])
        for state_name, state in program.states.items():
            app.add_api_route(f"/{program.name}/{state_name}", create_endpoint(state.input_schema_model, self.agent.state_mapping[state_name]), methods=["POST"])

    def stop(self, app: FastAPI):
        pass

    def restart(self, app: FastAPI):
        self.stop(app)
        self.start(app)
