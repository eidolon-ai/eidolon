from typing import Annotated

import pytest
from fastapi import Body

from eidos.agent.agent import register_program, AgentState, register_action


class HelloWorld:
    @register_program()
    async def idle(self, name: Annotated[str, Body()]):
        if name.lower() == "hello":
            raise Exception("hello is not a name")
        return f"Hello, {name}!"


class TestHelloWorld:
    @pytest.fixture(scope="class")
    def client(self, client_builder):
        with client_builder(HelloWorld) as client:
            yield client

    def test_can_start(self, client):
        docs = client.get("/docs")
        assert docs.status_code == 200

    def test_hello_world(self, client):
        post = client.post("/agents/HelloWorld/programs/idle", json="world")
        assert post.status_code == 200
        assert post.json()["data"] == "Hello, world!"

    def test_automatic_state_transition(self, client):
        post = client.post("/agents/HelloWorld/programs/idle", json="world")
        assert post.status_code == 200
        assert post.json()["state"] == "terminated"


# todo, we have a bug with defaults in str Body fields like below


class StateMachine:
    @register_action("ap")
    @register_program()
    async def action_program(self):
        return AgentState[str](name="ap", data="default response")

    @register_program()
    # async def idle(self, desired_state: Annotated[str, Body()], response: Annotated[str, Body()] = "default response"):
    async def idle(self, desired_state: Annotated[str, Body()], response: Annotated[str, Body()]):
        return AgentState(name=desired_state, data=response)

    @register_action("foo", "bar")
    async def to_bar(self):
        return AgentState(name="bar", data="heading to the bar")

    @register_action("foo")
    async def to_church(self):
        return AgentState(name="church", data="man of god")

    @register_action("church")
    async def terminate(self):
        return "Only God can terminate me"


class TestStateMachine:
    @pytest.fixture(scope="class")
    def client(self, client_builder):
        with client_builder(StateMachine) as client:
            yield client

    def test_can_list_processes(self, client):
        url = "/agents/StateMachine/programs/idle"

        first = client.post(url, json=dict(desired_state="church", response="blurb")).json()["process_id"]
        second = client.post(url, json=dict(desired_state="foo", response="blurb")).json()["process_id"]
        third = client.post(url, json=dict(desired_state="foo", response="blurb")).json()["process_id"]

        processes = client.get("/agents/StateMachine/processes/")
        assert processes.status_code == 200
        assert processes.json()["total"] == 3
        assert {p["process_id"] for p in processes.json()["processes"]} == {first, second, third}

        # update the first process: it should be at end of list now
        assert first == client.post(f"/agents/StateMachine/processes/{first}/actions/terminate").json()["process_id"]

        processes = client.get("/agents/StateMachine/processes/")
        assert processes.json()["total"] == 3
        assert [p["process_id"] for p in processes.json()["processes"]] == [second, third, first]

    def test_can_start(self, client):
        post = client.post(
            "/agents/StateMachine/programs/idle",
            json=dict(desired_state="bar", response="low man on the totem pole"),
        )
        assert post.status_code == 200
        assert post.json()["state"] == "bar"
        assert post.json()["data"] == "low man on the totem pole"

    def test_can_transition_state(self, client):
        init = client.post(
            "/agents/StateMachine/programs/idle",
            json=dict(desired_state="foo", response="low man on the totem pole"),
        )
        assert init.status_code == 200
        assert init.json()["state"] == "foo"

        to_bar = client.post(f"/agents/StateMachine/processes/{init.json()['process_id']}/actions/to_bar")
        assert to_bar.status_code == 200
        assert to_bar.json()["state"] == "bar"

    def test_allowed_actions(self, client):
        init = client.post(
            "/agents/StateMachine/programs/idle",
            json=dict(desired_state="foo", response="low man on the totem pole"),
        )
        assert "to_church" in init.json()["available_actions"]

        to_bar = client.post(f"/agents/StateMachine/processes/{init.json()['process_id']}/actions/to_bar")
        assert "to_church" not in to_bar.json()["available_actions"]

        to_church = client.post(f"/agents/StateMachine/processes/{init.json()['process_id']}/actions/to_church")
        assert to_church.status_code == 409

    @pytest.mark.skip(reason="un comment idle signature when bug is fixed")
    def test_default_in_body(self, client):
        init = client.post(
            "/agents/StateMachine/programs/idle",
            json=dict(desired_state="foo", response="low man on the totem pole"),
        )
        init.raise_for_status()
        assert init.json()["data"] == "default response"

    def test_state_machine_termination(self, client):
        init = client.post(
            "/agents/StateMachine/programs/idle",
            json=dict(desired_state="church", response="blurb"),
        )
        assert init.status_code == 200
        assert init.json()["state"] == "church"

        terminated = client.post(f"/agents/StateMachine/processes/{init.json()['process_id']}/actions/terminate")
        assert terminated.status_code == 200
        assert terminated.json()["state"] == "terminated"
        assert terminated.json()["data"] == "Only God can terminate me"
        assert terminated.json()["available_actions"] == []

    def test_can_register_function_as_action_and_program(self, client):
        program = client.post("/agents/StateMachine/programs/action_program")
        assert program.status_code == 200
        action = client.post(f"/agents/StateMachine/processes/{program.json()['process_id']}/actions/action_program",)
        assert action.status_code == 200
