from __future__ import annotations

import importlib
from typing import Type, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field, create_model

from eidolon_sdk.util.dynamic_endpoint import add_dynamic_route
from .agent import Agent
from .agent_os import AgentOS
from .agent_program import AgentProgram


class AgentProcess:
    agent: Agent

    def __init__(self, agent_program: AgentProgram, agent_os: AgentOS):
        self.agent_program = agent_program
        self.agent_os = agent_os

    def start(self, app: FastAPI):
        # First create the Agent implementation
        module_name, class_name = self.agent_program.implementation.rsplit(".", 1)
        module = importlib.import_module(module_name)
        impl_class = getattr(module, class_name)

        self.agent = impl_class(self)

        program = self.agent_program
        # Register a POST endpoint for each Pydantic model in the dictionary
        for state_name, state in program.states.items():
            path = f"/{program.name}/{{conversation_id}}/{state_name}"
            if state_name == program.initial_state:
                path = f"/{program.name}"
            add_dynamic_route(app, path, self.create_request_model(state_name, state_name != program.initial_state, state.input_schema_model),
                              self.create_response_model(state_name), self.processRoute(state_name))

    def stop(self):
        pass

    def restart(self):
        self.stop()
        self.start()

    def processRoute(self, state: str):
        def processStateRoute(body: dict):
            print(state)
            print(body)
            conversation_id = self.agent_os.startProcess(body.callback_url)
            return {"conversation_id": conversation_id}

        return processStateRoute

    def create_request_model(self, name: str, include_conversation_id: bool, input_model: Type[BaseModel]):
        fields = {
            "callback_url": (str, Field(..., description="The URL to call when the agent is done.")),
            "args": (input_model, Field(..., description="The arguments for the agent call.")),
        }
        if include_conversation_id:
            fields['conversation_id'] = (str, Field(..., description="The ID of the conversation."))

        return create_model(f'{name.capitalize()}RequestModel', **fields)

    def create_response_model(self, state: str):
        fields = {
            "conversation_id": (str, Field(..., description="The ID of the conversation.")),
        }
        for t_name, t_model in self.agent_program.states[state].transitions_to_models.items():
            fields[t_name] = (Optional[t_model], Field(default=None, description="The answer for {t_name} transition state."))

        return create_model(f'{state.capitalize()}ResponseModel', **fields)


class ConversationResponse(BaseModel):
    conversation_id: str = Field(..., description="The ID of the conversation.")
