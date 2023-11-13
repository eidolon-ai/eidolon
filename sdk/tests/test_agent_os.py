from __future__ import annotations

import contextlib
from typing import Annotated, Dict

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from eidolon_sdk.agent import CodeAgent, register
from eidolon_sdk.agent_machine import AgentMachine
from eidolon_sdk.agent_os import AgentOS
from eidolon_sdk.agent_program import AgentProgram

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
    counter = 0  # todo, this is a hack to make sure function is called. Should wrap with mock instead

    @register(state="idle", transition_to=['idle', 'terminated'])
    async def idle(self, question: Annotated[str, Field(description="The question to ask. Can be anything, but it better be hello")]):
        TestHelloWorldAgent.counter += 1
        if question == "hello":
            return HelloWorldResponse(question=question, answer="world")
        else:
            raise Exception("Invalid Question")


@pytest.fixture
def hello_world_machine():
    TestHelloWorldAgent.counter = 0
    return AgentMachine(agent_memory={}, agent_io={}, agent_programs=[AgentProgram(
        name="hello_world",
        implementation="tests.test_agent_os." + TestHelloWorldAgent.__qualname__,
    )])


def test_empty_start():
    with os_manager(AgentMachine(agent_memory={}, agent_io={}, agent_programs=[])):
        docs = client.get("/docs")
        assert docs.status_code == 200


def test_program(hello_world_machine):
    with os_manager(hello_world_machine):
        response = client.post("/hello_world", json=dict(question="hello"))
        assert response.status_code == 202


def test_program_actually_calls_code(hello_world_machine):
    with os_manager(hello_world_machine):
        client.post("/hello_world", json=dict(question="hello"))
        assert TestHelloWorldAgent.counter == 1


@pytest.mark.skip(reason="todo, we should not need to anotate args on registered methods. It should hook up with no description")
def test_non_annotated_args_on_registered_method():
    ...


@pytest.mark.skip(reason="this doesn't work yet, we need an error handler")
def test_program_error(hello_world_machine):
    with os_manager(hello_world_machine):
        response = client.post("/hello_world", json=dict(question="hola"))
        assert response.status_code == 500
