from __future__ import annotations

import contextlib
from typing import Dict, Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from eidolon_sdk.agent import CodeAgent, register
from eidolon_sdk.agent_machine import AgentMachine
from eidolon_sdk.agent_os import AgentOS
from eidolon_sdk.agent_program import AgentProgram, AgentIOState

app = FastAPI()
client = TestClient(app)


@contextlib.contextmanager
def os_manager(machine: AgentMachine):
    os = AgentOS(machine=machine, machine_yaml="")
    os.start(app)
    try:
        yield
    finally:
        os.stop()


class HelloWorldResponse(BaseModel):
    question: str
    answer: str


class TestHelloWorldAgent(CodeAgent):
    @register()
    async def execute(self, question: str) -> HelloWorldResponse:
        if question == "hello":
            return HelloWorldResponse(question=question, answer="world")
        else:
            raise ValueError("Invalid Question")


@pytest.fixture
def hello_world_machine():
    return AgentMachine(agent_memory={}, agent_io={}, agent_programs=[AgentProgram(
        name="hello_world",
        implementation="tests.test_agent_os." + TestHelloWorldAgent.__qualname__,
        # todo, state transitions should be defined on agent, and constructed on machine automatically
        states={"idle": AgentIOState(
            state_name="idle",
            description="The agent is waiting for a question",
            input_schema={
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string"
                    }
                }
            },
            transitions_to={"idle": {
                "type": "object",
                "properties": {
                    "answer": {
                        "type": "string"
                    }
                }
            }},
        )},
    )])


def test_empty_start():
    with os_manager(AgentMachine(agent_memory={}, agent_io={}, agent_programs=[])):
        docs = client.get("/docs")
        assert docs.status_code == 200


def test_program(hello_world_machine):
    # setattr(eidolon_sdk.agent_program, "CodeAgent", TestHelloWorldAgent)
    with os_manager(hello_world_machine):
        response = client.post("/hello_world", json=dict(question="hello"))
        assert response.status_code == 202
