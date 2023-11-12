from __future__ import annotations
import yaml
from pydantic import BaseModel

import eidolon_sdk.agent_program
from agent import Agent
from agent_program import AgentProgram, AgentIOState
from eidolon_sdk.agent_machine import AgentMachine
from eidolon_sdk.agent_os import AgentOS
from fastapi.testclient import TestClient


def get_client(machine):
    os = AgentOS(yaml.dump(machine.model_dump()))
    os.start()
    return TestClient(os.app)


class HelloWorldResponse(BaseModel):
    question: str
    answer: str


class TestHelloWorldAgent(Agent):
    # todo, mapping and state should be handled via annotations
    def __init__(self):
        super().__init__()
        self.state_mapping = {"idle": self.idle}
        self.starting_state = "idle"

    @staticmethod
    async def idle(question) -> HelloWorldResponse:
        if question == "hello":
            return HelloWorldResponse(question=question, answer="world")
        else:
            raise ValueError("Invalid Question")


def test_empty_start():
    client = get_client(AgentMachine(agent_memory={}, agent_io={}, agent_programs=[]))
    docs = client.get("/docs")
    assert docs.status_code == 200


def test_program():
    setattr(eidolon_sdk.agent_program, "CodeAgent", TestHelloWorldAgent)

    machine = AgentMachine(agent_memory={}, agent_io={}, agent_programs=[AgentProgram(
        name="hello_world",
        implementation="eidolon_sdk.agent_program.CodeAgent",
        agent_cpu=None,
        # todo, state transitions should be defined on agent, and constructed on machine automatically
        states={"idle": AgentIOState(
            state_name="idle",
            input_schema={"question": "str"},
            transitions_to={"idle": {"answer": "str"}},
        )},
    )])
    client = get_client(machine)
    response = client.post("/hello_world", json={"question": "hello"})
    assert response.status_code == 202
    state_response = client.get(f"/hello_world/{response.json()['conversation_id']}")
    assert response.status_code == 200
    assert state_response.json() == {
        "question": "hello",
        "answer": "world"
    }
