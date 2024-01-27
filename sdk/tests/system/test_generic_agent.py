import json
from collections import defaultdict

import pytest_asyncio
from typing import Annotated, List

import pytest
from fastapi import Body

from eidos_sdk.agent.agent import register_program
from eidos_sdk.agent_os import AgentOS
from eidos_sdk.io.events import StartAgentCallEvent, ObjectOutputEvent, SuccessEvent, AgentStateEvent, StartLLMEvent, StringOutputEvent
from eidos_sdk.system.request_context import RequestContext
from eidos_sdk.system.resources.resources_base import Metadata, Resource
from eidos_sdk.util.aiohttp import stream_content


@pytest.fixture(scope="module")
def generic_agent_root(llm):
    return Resource(
        apiVersion="eidolon/v1",
        kind="Agent",
        metadata=Metadata(name="GenericAgent"),
        spec=dict(
            implementation="GenericAgent",
            cpu=dict(llm_unit=llm),
            system_prompt="You are a machine which follows instructions and returns a summary of your actions.",
            user_prompt="{{instruction}}",
            input_schema=dict(instruction=dict(type="string")),
            description="An agent which can follow instructions and return a summary of its actions.",
        ),
    )


@pytest.fixture
def generic_agent(generic_agent_root):
    return generic_agent_root.model_copy(deep=True)


class TestGenericAgent:
    @pytest_asyncio.fixture(scope="class")
    async def client(self, client_builder, generic_agent_root):
        async with client_builder(generic_agent_root) as client:
            yield client

    def test_can_start(self, client):
        docs = client.get("/docs")
        assert docs.status_code == 200

    def test_llm_calls(self, client):
        post = client.post(
            "/agents/GenericAgent/programs/question",
            json=dict(instruction="Hi! What is the capital of France?"),
        )
        post.raise_for_status()
        json = post.json()
        assert "paris" in json["data"].lower()

    def test_continued_conversation(self, client):
        post = client.post(
            "/agents/GenericAgent/programs/question",
            json=dict(instruction="Hi! my name is Luke"),
        )
        post.raise_for_status()
        process_id = post.json()["process_id"]
        follow_up = client.post(
            f"/agents/GenericAgent/processes/{process_id}/actions/respond",
            json=dict(statement="Can you sing me Happy Birthday?"),
        )
        follow_up.raise_for_status()
        assert "Luke" in post.json()["data"]


@pytest.fixture(scope="module")
def generic_agent_with_refs():
    return Resource(
        apiVersion="eidolon/v1",
        kind="Agent",
        metadata=Metadata(name="GenericAgent"),
        spec=dict(
            implementation="GenericAgent",
            system_prompt="You are a machine which follows instructions",
            user_prompt="{{instruction}}",
            agent_refs=["HelloWorld"],
            description="An agent which can follow instructions and return a summary of its actions.",
            input_schema=dict(instruction=dict(type="string")),
        ),
    )


class HelloWorld:
    calls = defaultdict(list)

    @register_program()
    async def greeter1(self, name: Annotated[str, Body(embed=True)]):
        return self._greet("greeter1", name=name)

    @register_program()
    async def greeter2(self, name: Annotated[str, Body(description="The name to greet")]):
        return self._greet("greeter2", name=name)

    @register_program()
    async def greeter3(self, name: Annotated[List[str], Body(embed=True)]):
        return self._greet("greeter3", name=name[0], called_with=name)

    @register_program()
    async def greeter4(self):
        self.calls["greeter4"].append(RequestContext.get("foo"))
        return "leave me alone"

    def _greet(self, greeter, **kwargs):
        self.calls[greeter].append(kwargs)
        return f"Hello, {kwargs['name']}!"


# Image model does not support tool usage, so we need to break this out into a separate test suite
class TestAgentsWithReferences:
    @pytest.fixture(scope="function")
    async def client(self, client_builder, generic_agent_with_refs):
        async with client_builder(generic_agent_with_refs, HelloWorld) as client:
            yield client

    def test_can_communicate(self, client):
        post = client.post(
            "/agents/GenericAgent/programs/question",
            json=dict(instruction="Hi! my name is Luke. Can ask greeter1 to greet me?"),
        )
        post.raise_for_status()
        assert HelloWorld.calls["greeter1"] == [{"name": "Luke"}]

    def test_string_only_body(self, client):
        post = client.post(
            "/agents/GenericAgent/programs/question",
            json=dict(instruction="Hi! my name is Luke. Can ask greeter2 to greet me?"),
        )
        post.raise_for_status()
        assert HelloWorld.calls["greeter2"] == [{"name": "Luke"}]

    def test_list_body(self, client, patch_async_vcr_send):
        post = client.post(
            "/agents/GenericAgent/programs/question",
            json=dict(instruction="Hi! my name is Luke. Can ask greeter3 to greet me?"),
        )
        post.raise_for_status()
        assert HelloWorld.calls["greeter3"] == [{"name": "Luke", "called_with": ["Luke"]}]

    # todo, this is a nd test, let's catch a cassette failure and debug
    def test_passes_context(self, client):
        RequestContext.set("foo", "bar")
        post = client.post(
            "/agents/GenericAgent/programs/question",
            headers=RequestContext.headers,
            json=dict(instruction="Hi! my name is Luke. Can ask greeter4 to greet me?"),
        )
        post.raise_for_status()
        assert HelloWorld.calls["greeter4"] == ["bar"]


async def test_generic_agent_supports_object_output(client_builder, generic_agent, dog):
    generic_agent.spec["output_schema"] = {
        "type": "object",
        "properties": {"capital": {"type": "string"}, "population": {"type": "number"}},
    }
    async with client_builder(generic_agent) as client:
        post = client.post(
            "/agents/GenericAgent/programs/question", json=dict(instruction="Tell me about france please")
        )
        post.raise_for_status()
        assert "paris" in post.json()["data"]["capital"].lower()


@pytest.mark.asyncio
async def test_generic_agent_supports_object_output_with_stream(run_app, generic_agent, dog):
    generic_agent.spec["output_schema"] = {
        "type": "object",
        "properties": {"capital": {"type": "string"}, "population": {"type": "number"}},
    }
    async with run_app(generic_agent) as ra:
        stream = stream_content(
            f"{ra}/agents/GenericAgent/programs/question", body=dict(instruction="Tell me about france please")
        )
        expected_events = [
            StartAgentCallEvent(
                agent_name="GenericAgent",
                machine=AgentOS.current_machine_url,
                call_name="question",
                process_id="test_generic_agent_supports_object_output_with_stream_0"
            ),
            StartLLMEvent(),
            ObjectOutputEvent(content={'capital': 'Paris', 'population': 67399000}),
            SuccessEvent(),
            AgentStateEvent(state="idle", available_actions=["respond"]),
            SuccessEvent()
        ]
        events = [event async for event in stream]
        assert events == expected_events


@pytest.mark.asyncio
async def test_generic_agent_supports_string_stream(run_app, generic_agent, dog):
    generic_agent.spec["output_schema"] = "str"
    async with run_app(generic_agent) as ra:
        stream = stream_content(
            f"{ra}/agents/GenericAgent/programs/question", body=dict(
                instruction="What is the capital of france and its population. Put the relevant parts in XML like blocks. "
                            "For instance <capital>...insert capital here...</capital> and <population>...insert population here...</population>")
        )
        events = (e for e in [event async for event in stream])
        assert next(events) == StartAgentCallEvent(
            agent_name="GenericAgent",
            machine=AgentOS.current_machine_url,
            call_name="question",
            process_id="test_generic_agent_supports_string_stream_0"
        )
        assert next(events) == StartLLMEvent()
        next_event = next(events)
        str = ""
        while isinstance(next_event, StringOutputEvent):
            str += next_event.content
            next_event = next(events)

        assert "<capital>Paris</capital>" in str
        assert "<population>" in str
        assert next_event == SuccessEvent()
        assert next(events) == AgentStateEvent(state="idle", available_actions=["respond"])
        assert next(events) == SuccessEvent()


async def test_generic_agent_supports_image(client_builder, generic_agent, dog):
    generic_agent.spec["files"] = "single"
    async with client_builder(generic_agent) as client:
        post = client.post(
            "/agents/GenericAgent/programs/question",
            data=dict(body=json.dumps(dict(instruction="What is in this image?"))),
            files=dict(file=dog),
        )
        post.raise_for_status()
        assert "brown" in post.json()["data"].lower()


async def test_generic_agent_supports_multiple_images(client_builder, generic_agent, cat, dog):
    generic_agent.spec["files"] = "multiple"
    async with client_builder(generic_agent) as client:
        post = client.post(
            "/agents/GenericAgent/programs/question",
            data=dict(body=json.dumps(dict(instruction="what do these images have in common?"))),
            files=[("file", dog), ("file", cat)],
        )
        post.raise_for_status()
        assert "animals" in post.json()["data"].lower()

        # followup question should still have access to the image
        process_id = post.json()["process_id"]
        follow_up = client.post(
            f"/agents/GenericAgent/processes/{process_id}/actions/respond",
            json=dict(statement="What is different between them?"),
        )
        follow_up.raise_for_status()
        assert "cat" in follow_up.json()["data"].lower()
