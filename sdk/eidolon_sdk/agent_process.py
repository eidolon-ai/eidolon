from __future__ import annotations

import asyncio
import importlib
import typing
from typing import Annotated

from fastapi import FastAPI, Header
from pydantic import BaseModel, Field, create_model
from pydantic.fields import FieldInfo

from eidolon_sdk.util.dynamic_endpoint import add_dynamic_route
from .agent import Agent
from .agent_os import AgentOS
from .agent_program import AgentProgram


class ProcessResponse(BaseModel):
    conversation_id: str = Field(..., description="The ID of the conversation.")


class AgentProcess:
    agent: Agent
    agent_program: AgentProgram
    agent_os: AgentOS

    def __init__(self, agent_program: AgentProgram, agent_os: AgentOS):
        self.agent_program = agent_program
        self.agent_os = agent_os

    def start(self, app: FastAPI):
        # First create the Agent implementation
        module_name, class_name = self.agent_program.implementation.rsplit(".", 1)
        module = importlib.import_module(module_name)
        impl_class = getattr(module, class_name)

        self.agent = impl_class(self)

        add_dynamic_route(
            app=app,
            path=f"/{self.agent_program.name}",
            input_model=self.create_input_model(self.agent_program.initial_state),
            response_model=ProcessResponse,
            fn=self.processRoute(self.agent_program.initial_state),
            status_code=202,
        )

        for state_name, handler in self.agent.handlers.items():
            # the endpoint to hit to process/continue the current state
            add_dynamic_route(
                app=app,
                path=f"/{self.agent_program.name}/{{conversation_id}}/{state_name}",
                input_model=self.create_input_model(state_name),
                response_model=ProcessResponse,
                fn=self.processRoute(state_name),
                status_code=202,
            )

            # the endpoint to hit to retrieve the results after transitioning to the next state
            if handler.state_representation:
                app.add_api_route(
                    f"/{self.agent_program.name}/{{conversation_id}}/{state_name}",
                    endpoint=lambda *args, **kwargs: (asyncio.sleep(0)),
                    # todo, hook up state retrieval once memory is implemented
                    methods=["GET"],
                    response_model=handler.state_representation
                )

    def create_input_model(self, state_name):
        hints = typing.get_type_hints(self.agent.handlers[state_name].fn, include_extras=True)
        fields = {
            k: (v.__origin__, meta_record)
            for k, v in hints.items() if k != 'return'
            for meta_record in v.__metadata__ if isinstance(meta_record, FieldInfo)
        }
        input_model = create_model(f'{state_name.capitalize()}InputModel', **fields)
        return input_model

    def stop(self, app: FastAPI):
        pass

    def restart(self, app: FastAPI):
        self.stop(app)
        self.start(app)

    def processRoute(self, state: str):
        async def processStateRoute(body: BaseModel, callback_url: Annotated[str | None, Header()] = None):
            print(state)
            print(body)
            await self.agent.handlers[state].fn(self.agent, **body.model_dump())
            conversation_id = self.agent_os.startProcess(callback_url)
            return {"conversation_id": conversation_id}

        return processStateRoute


class ConversationResponse(BaseModel):
    conversation_id: str = Field(..., description="The ID of the conversation.")
