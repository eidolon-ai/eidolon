from typing import Annotated

import httpx
import pytest
import pytest_asyncio
from fastapi import Body, HTTPException
from httpx import HTTPStatusError

from eidolon_ai_sdk.agent.agent import register_program, AgentState, register_action
from eidolon_ai_sdk.agent.client import Agent, Process, ProcessStatus
from eidolon_ai_sdk.io.events import (
    ErrorEvent,
    AgentStateEvent,
    StringOutputEvent,
    StartStreamContextEvent,
    EndStreamContextEvent,
)
from eidolon_ai_sdk.util.stream_collector import stream_manager


class HelloWorld:
    @register_program()
    async def idle(self, name: Annotated[str, Body()]):
        if name.lower() == "hello":
            raise HTTPException(418, "hello is not a name")
        if name.lower() == "error":
            raise Exception("big bad server error")
        return f"Hello, {name}!"

    @register_program()
    async def idle_streaming(self, name: Annotated[str, Body()]):
        if name.lower() == "hello":
            raise HTTPException(418, "hello is not a name")
        if name.lower() == "error":
            raise Exception("big bad server error")
        yield StringOutputEvent(content=f"Hello, {name}!")

    @register_program()
    async def lots_o_context(self):
        yield StringOutputEvent(content="1")
        yield StringOutputEvent(content="2")
        async for e in _m(_s(3, 4), context="c1"):
            yield e
        async for e in _m(_s(5, 6, after=_m(_s(7, 8), context="c3")), context="c2"):
            yield e


async def _s(*_args, after=None):
    for a in _args:
        yield StringOutputEvent(content=str(a))
    if after:
        async for a in after:
            yield a


def _m(stream, context: str):
    return stream_manager(stream, StartStreamContextEvent(context_id=context))


class TestHelloWorld:
    @pytest_asyncio.fixture(scope="class")
    async def server(self, run_app):
        async with run_app(HelloWorld) as ra:
            yield ra

    @pytest_asyncio.fixture(scope="function")
    async def client(self, server):
        with httpx.Client(base_url=server, timeout=httpx.Timeout(60)) as client:
            yield client

    @pytest.fixture(scope="function")
    def agent(self, server):
        return Agent.get("HelloWorld")

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

    @pytest.mark.parametrize("program", ["idle", "idle_streaming"])
    async def test_http_error(self, server, program):
        with pytest.raises(HTTPStatusError) as exc:
            await Agent.get("HelloWorld").program(program, "hello")
        assert exc.value.response.status_code == 418
        assert exc.value.response.json() == "hello is not a name"

    @pytest.mark.parametrize("program", ["idle", "idle_streaming"])
    async def test_streaming_http_error(self, server, program):
        stream = Agent.get("HelloWorld").stream_program(program, "hello")
        events = {type(e): e async for e in stream}
        assert ErrorEvent in events
        assert events[ErrorEvent].reason == dict(detail="hello is not a name", status_code=418)
        assert events[AgentStateEvent].state == "http_error"

        with pytest.raises(HTTPStatusError) as exc:
            await Process.get(stream).status()
        assert exc.value.response.status_code == 418
        assert exc.value.response.json() == "hello is not a name"

    @pytest.mark.parametrize("program", ["idle", "idle_streaming"])
    async def test_unhandled_error(self, server, program):
        with pytest.raises(HTTPStatusError) as exc:
            await Agent.get("HelloWorld").program(program, "error")
        assert exc.value.response.status_code == 500
        assert exc.value.response.json() == "big bad server error"

    @pytest.mark.parametrize("program", ["idle", "idle_streaming"])
    async def test_streaming_unhandled_error(self, agent, program):
        stream = agent.stream_program(program, "error")
        events = {type(e): e async for e in stream}
        assert ErrorEvent in events
        assert events[ErrorEvent].reason == dict(detail="big bad server error", status_code=500)
        assert events[AgentStateEvent].state == "unhandled_error"

        with pytest.raises(HTTPStatusError) as exc:
            await Process.get(stream).status()
        assert exc.value.response.status_code == 500
        assert exc.value.response.json() == "big bad server error"

    async def test_lots_o_context(self, agent):
        resp = await agent.program("lots_o_context")
        assert resp.data == "12"

    async def test_lots_o_context_streaming(self, agent):
        events = [e async for e in agent.stream_program("lots_o_context")]
        assert events[2:-1] == [
            StringOutputEvent(content="1"),
            StringOutputEvent(content="2"),
            StartStreamContextEvent(context_id="c1"),
            StringOutputEvent(content="3", stream_context="c1"),
            StringOutputEvent(content="4", stream_context="c1"),
            EndStreamContextEvent(context_id="c1"),
            StartStreamContextEvent(context_id="c2"),
            StringOutputEvent(content="5", stream_context="c2"),
            StringOutputEvent(content="6", stream_context="c2"),
            StartStreamContextEvent(context_id="c3", stream_context="c2"),
            StringOutputEvent(content="7", stream_context="c2.c3"),
            StringOutputEvent(content="8", stream_context="c2.c3"),
            EndStreamContextEvent(stream_context="c2", context_id="c3"),
            EndStreamContextEvent(context_id="c2"),
            AgentStateEvent(state="terminated", available_actions=[]),
        ]

    async def test_creating_processes_without_program(self, agent):
        process: ProcessStatus = await agent.create_process()
        assert process.state == "initialized"
        assert "idle" in process.available_actions
        action = await process.action('idle', "Luke")
        assert action.data == "Hello, Luke!"

    async def test_delete_process(self, agent):
        process: ProcessStatus = await agent.create_process()
        deleted = await process.delete()
        assert deleted.process_id == process.process_id
        assert deleted.deleted == 1
        with pytest.raises(HTTPStatusError) as exc:
            await process.status()
        assert exc.value.response.status_code == 404


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


class StateMachine2(StateMachine):
    pass


class TestStateMachine:
    @pytest_asyncio.fixture(scope="class")
    async def server(self, run_app):
        async with run_app(StateMachine, StateMachine2) as ra:
            yield ra

    @pytest_asyncio.fixture(scope="function")
    async def client(self, server):
        with httpx.Client(base_url=server, timeout=httpx.Timeout(60)) as client:
            yield client

    def test_can_list_processes(self, client):
        url = "/agents/StateMachine/programs/idle"

        first = client.post(url, json=dict(desired_state="church", response="blurb")).json()["process_id"]
        second = client.post(url, json=dict(desired_state="foo", response="blurb")).json()["process_id"]
        third = client.post(url, json=dict(desired_state="foo", response="blurb")).json()["process_id"]

        processes = client.get("/agents/StateMachine/processes")
        assert processes.status_code == 200
        assert processes.json()["total"] == 3
        assert {p["process_id"] for p in processes.json()["processes"]} == {first, second, third}

        # update the first process: it should be at end of list now
        assert first == client.post(f"/agents/StateMachine/processes/{first}/actions/terminate").json()["process_id"]

        processes = client.get("/agents/StateMachine/processes")
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
        action = client.post(
            f"/agents/StateMachine/processes/{program.json()['process_id']}/actions/action_program",
        )
        assert action.status_code == 200

    def test_agents_are_separate(self, client):
        init = client.post(
            "/agents/StateMachine/programs/idle",
            json=dict(desired_state="church", response="blurb"),
        )
        assert init.status_code == 200
        assert init.json()["state"] == "church"

        not_found = client.post(f"/agents/StateMachine2/processes/{init.json()['process_id']}/actions/terminate")
        assert not_found.status_code == 404
