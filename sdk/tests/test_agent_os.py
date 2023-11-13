from __future__ import annotations

from typing import Dict, Any

import yaml
from fastapi.testclient import TestClient
from pydantic import BaseModel

from eidolon_sdk.agent import CodeAgent
from eidolon_sdk.agent_program import AgentProgram, AgentIOState
from eidolon_sdk.agent_machine import AgentMachine
from eidolon_sdk.agent_os import AgentOS


def get_client(machine):
    os = AgentOS(yaml.dump(machine.model_dump()))
    os.start()
    return TestClient(os.app)


class HelloWorldResponse(BaseModel):
    question: str
    answer: str


class TestHelloWorldAgent(CodeAgent):
    async def execute(self, state_name: str, input: Dict[str, Any]):
        if input["question"] == "hello":
            return HelloWorldResponse(question=input["question"], answer="world")
        else:
            raise ValueError("Invalid Question")


def test_empty_start():
    client = get_client(AgentMachine(agent_memory={}, agent_io={}, agent_programs=[]))
    docs = client.get("/docs")
    assert docs.status_code == 200


def test_program():
    # setattr(eidolon_sdk.agent_program, "CodeAgent", TestHelloWorldAgent)

    machine = AgentMachine(agent_memory={}, agent_io={}, agent_programs=[AgentProgram(
        name="hello_world",
        implementation=TestHelloWorldAgent.__qualname__,
        initial_state="idle",
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
    client = get_client(machine)
    response = client.post("/hello_world", json={"question": "hello"})
    assert response.status_code == 202
    state_response = client.get(f"/hello_world/{response.json()['conversation_id']}")
    assert response.status_code == 200
    assert state_response.json() == {
        "question": "hello",
        "answer": "world"
    }
