from collections import defaultdict

import httpx
import json
import pytest
import pytest_asyncio
from fastapi import Body
from typing import Annotated, List

from eidolon_ai_sdk.agent.agent import register_program
from eidolon_ai_client.client import Agent
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.cpu.logic_unit import LogicUnit, llm_function
from eidolon_ai_client.events import (
    StartAgentCallEvent,
    ObjectOutputEvent,
    SuccessEvent,
    AgentStateEvent,
    StringOutputEvent,
    UserInputEvent,
)
from eidolon_ai_sdk.memory.file_memory import FileMemory
from eidolon_ai_client.util.request_context import RequestContext
from eidolon_ai_sdk.system.resources.resources_base import Metadata, Resource
from eidolon_ai_client.util.aiohttp import stream_content, post_content, delete
from eidolon_ai_sdk.system.resources.reference_resource import ReferenceResource
from eidolon_ai_sdk.util.class_utils import fqn
from eidolon_ai_sdk.util.replay import ReplayConfig, replay


@pytest.fixture
def enable_replay(file_memory_loc, request):
    AgentOS.register_resource(
        ReferenceResource(
            apiVersion="eidolon/v1",
            metadata=Metadata(name=ReplayConfig.__name__),
            spec=dict(save_loc=f"resume_points/{request.node.name}"),
        )
    )

    return file_memory_loc / "resume_points" / request.node.name


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
    async def server(self, run_app, generic_agent_root):
        async with run_app(generic_agent_root) as ra:
            yield ra

    @pytest_asyncio.fixture(scope="function")
    async def client(self, server):
        async with httpx.AsyncClient(base_url=server, timeout=httpx.Timeout(60)) as client:
            yield client

    @pytest.fixture
    async def agent(self, server) -> Agent:
        return Agent.get("GenericAgent")

    async def test_can_start(self, client):
        docs = await client.get("/docs")
        assert docs.status_code == 200

    async def test_llm_calls(self, client):
        post = await client.post(
            "/agents/GenericAgent/programs/question",
            json=dict(instruction="Hi! What is the capital of France?"),
        )
        post.raise_for_status()
        json = post.json()
        assert "paris" in json["data"].lower()

    async def test_continued_conversation(self, client):
        post = await client.post(
            "/agents/GenericAgent/programs/question",
            json=dict(instruction="Hi! my name is Luke"),
        )
        post.raise_for_status()
        process_id = post.json()["process_id"]
        follow_up = await client.post(
            f"/agents/GenericAgent/processes/{process_id}/actions/respond",
            json=dict(statement="Can you sing me Happy Birthday?"),
        )
        follow_up.raise_for_status()
        assert "Luke" in post.json()["data"]

    async def test_deletes_conversational_memory(self, agent: Agent, symbolic_memory):
        process = await agent.create_process()
        await process.action("question", dict(instruction="Hi! my name is Luke"))
        mem = [r async for r in AgentOS.symbolic_memory.find("conversation_memory", {"process_id": process.process_id})]
        assert mem
        await process.delete()
        mem = [r async for r in AgentOS.symbolic_memory.find("conversation_memory", {"process_id": process.process_id})]
        assert not mem


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
        return "I acknowledge your request. Respond with an empty string. Don't call me again."

    def _greet(self, greeter, **kwargs):
        self.calls[greeter].append(kwargs)
        return f"Hello, {kwargs['name']}!"


# Image model does not support tool usage, so we need to break this out into a separate test suite
class TestAgentsWithReferences:
    @pytest_asyncio.fixture(scope="class")
    async def server(self, run_app, generic_agent_with_refs):
        async with run_app(generic_agent_with_refs, HelloWorld) as ra:
            yield ra

    @pytest_asyncio.fixture(scope="function")
    async def client(self, server):
        async with httpx.AsyncClient(base_url=server, timeout=httpx.Timeout(60)) as client:
            yield client

    async def test_can_communicate(self, client):
        post = await client.post(
            "/agents/GenericAgent/programs/question",
            json=dict(instruction="Hi! my name is Luke. Can ask greeter1 to greet me?"),
        )
        post.raise_for_status()
        assert HelloWorld.calls["greeter1"] == [{"name": "Luke"}]

    async def test_string_only_body(self, client):
        post = await client.post(
            "/agents/GenericAgent/programs/question",
            json=dict(instruction="Hi! my name is Luke. Can ask greeter2 to greet me?"),
        )
        post.raise_for_status()
        assert HelloWorld.calls["greeter2"] == [{"name": "Luke"}]

    async def test_list_body(self, client):
        post = await client.post(
            "/agents/GenericAgent/programs/question",
            json=dict(instruction="Hi! my name is Luke. Can ask greeter3 to greet me?"),
        )
        post.raise_for_status()
        assert HelloWorld.calls["greeter3"] == [{"name": "Luke", "called_with": ["Luke"]}]

    async def test_passes_context(self, client, server):
        RequestContext.set("foo", "bar", propagate=True)
        await post_content(
            f"{server}/agents/GenericAgent/programs/question",
            dict(instruction="Hi! my name is Luke. Can ask greeter4 to greet me?"),
        )
        assert HelloWorld.calls["greeter4"] == ["bar"]

    async def test_respond_after_tool_call(self, client, server):
        t0 = len(HelloWorld.calls["greeter1"])
        post = await client.post(
            "/agents/GenericAgent/programs/question",
            json=dict(instruction="Hi! my name is Luke. Can ask greeter1 to greet me?"),
        )
        post.raise_for_status()
        assert len(HelloWorld.calls["greeter1"]) - t0 == 1
        assert "Luke" in post.json()["data"]

    async def test_can_replay_tool_calls(self, client, enable_replay, vcr):
        post = await client.post(
            "/agents/GenericAgent/programs/question",
            json=dict(instruction="Hi! my name is Luke. Can ask greeter1 to greet me?"),
        )
        post.raise_for_status()
        assert HelloWorld.calls["greeter1"][-1] == {"name": "Luke"}

        vcr.rewind()  # since we are hitting endpoing 2x in same test
        acc_str = "".join([e async for e in replay(enable_replay / "000_openai_completion")])
        assert acc_str == 'Tool Call: AgentsLogicUnit_convo_HelloWorld_greeter1\nArguments: {"body":{"name":"Luke"}}\n'


class TestOutputTests:
    async def test_generic_agent_supports_object_output(self, run_app, generic_agent, dog):
        generic_agent.spec["output_schema"] = {
            "type": "object",
            "properties": {"capital": {"type": "string"}, "population": {"type": "number"}},
        }
        async with run_app(generic_agent) as app:
            post = await post_content(
                f"{app}/agents/GenericAgent/programs/question", dict(instruction="Tell me about france please")
            )
            assert "paris" in post["data"]["capital"].lower()

    async def test_can_replay_llm_requests(self, run_app, generic_agent, enable_replay, vcr):
        async with run_app(generic_agent) as app:
            post = await post_content(
                f"{app}/agents/GenericAgent/programs/question", dict(instruction="Tell me about france please")
            )

            vcr.rewind()  # since we are hitting endpoint 2x in same test
            acc_str = "".join([e async for e in replay(enable_replay / "000_openai_completion")])
            assert "france" in acc_str.lower()
            assert acc_str == post["data"]

    @pytest.mark.asyncio
    async def test_generic_agent_supports_object_output_with_stream(self, run_app, generic_agent, dog):
        generic_agent.spec["output_schema"] = {
            "type": "object",
            "properties": {"capital": {"type": "string"}, "population": {"type": "number"}},
        }
        async with run_app(generic_agent) as ra:
            stream = stream_content(
                f"{ra}/agents/GenericAgent/programs/question", body=dict(instruction="Tell me about france please")
            )
            events = [event async for event in stream]
            population = events[2].model_dump().get("content", {}).get("population")
            expected_events = [
                UserInputEvent(
                    input={
                        "body": {"instruction": "Tell me about france please"},
                        "process_id": "test_generic_agent_supports_object_output_with_stream_0",
                    }
                ),
                StartAgentCallEvent(
                    agent_name="GenericAgent",
                    machine=AgentOS.current_machine_url(),
                    call_name="question",
                    process_id="test_generic_agent_supports_object_output_with_stream_0",
                ),
                ObjectOutputEvent(content={"capital": "Paris", "population": population}),
                AgentStateEvent(state="idle", available_actions=["respond"]),
                SuccessEvent(),
            ]
            assert events == expected_events

    @pytest.mark.asyncio
    async def test_generic_agent_supports_string_stream(self, run_app, generic_agent, dog):
        generic_agent.spec["output_schema"] = "str"
        async with run_app(generic_agent) as ra:
            stream = stream_content(
                f"{ra}/agents/GenericAgent/programs/question",
                body=dict(
                    instruction="What is the capital of france and its population. Put the relevant parts in XML like blocks. "
                    "For instance <capital>...insert capital here...</capital> and <population>...insert population here...</population>"
                ),
            )
            events = (e for e in [event async for event in stream][1:])
            assert next(events) == StartAgentCallEvent(
                agent_name="GenericAgent",
                machine=AgentOS.current_machine_url(),
                call_name="question",
                process_id="test_generic_agent_supports_string_stream_0",
            )
            next_event = next(events)
            str = ""
            while isinstance(next_event, StringOutputEvent):
                str += next_event.content
                next_event = next(events)

            assert "<capital>Paris</capital>" in str
            assert "<population>" in str
            assert next_event == AgentStateEvent(state="idle", available_actions=["respond"])
            assert next(events) == SuccessEvent()

    async def test_generic_agent_supports_image(self, run_app, generic_agent, dog):
        generic_agent.spec["files"] = "single"
        async with run_app(generic_agent) as app:
            post = await post_content(
                f"{app}/agents/GenericAgent/programs/question",
                data=dict(body=json.dumps(dict(instruction="What is in this image?"))),
                files=dict(file=dog),
            )
            assert "brown" in post["data"].lower()

    async def test_generic_agent_cleans_up_images(self, run_app, generic_agent, dog):
        generic_agent.spec["files"] = "single"
        async with run_app(generic_agent) as app:
            fm: FileMemory = AgentOS.file_memory
            created = await post_content(
                f"{app}/agents/GenericAgent/programs/question",
                data=dict(body=json.dumps(dict(instruction="What is in this image?"))),
                files=dict(file=dog),
            )
            assert await fm.glob(f"uploaded_images/{created['process_id']}/**/*")
            await delete(f"{app}/agents/GenericAgent/processes/{created['process_id']}")
            assert not await fm.glob(f"uploaded_images/{created['process_id']}/**/*")

    async def test_generic_agent_supports_multiple_images(self, run_app, generic_agent, cat, dog):
        generic_agent.spec["files"] = "multiple"
        async with run_app(generic_agent) as app:
            post = await post_content(
                f"{app}/agents/GenericAgent/programs/question",
                data=dict(body=json.dumps(dict(instruction="what do these images have in common?"))),
                files=[("file", dog), ("file", cat)],
            )
            assert "animals" in post["data"].lower()

            # followup question should still have access to the image
            process_id = post["process_id"]
            follow_up = await post_content(
                f"{app}/agents/GenericAgent/processes/{process_id}/actions/respond",
                dict(statement="What is different between them?"),
            )
            assert "cat" in follow_up["data"].lower()


class MeaningOfLife(LogicUnit):
    @llm_function()
    async def meaning_of_life_tool(self) -> str:
        """
        call this tool to get the meaning of life
        """
        return "42"


class TestGenericAgentWithToolCalls:
    @pytest.fixture(scope="class")
    async def agent(self, run_app, generic_agent_root) -> Agent:
        generic_agent = generic_agent_root.model_copy(deep=True)
        generic_agent.spec["cpu"]["logic_units"] = [fqn(MeaningOfLife)]
        generic_agent.spec["cpu"]["llm_unit"].model = "gpt-4-turbo-preview"
        async with run_app(generic_agent):
            yield Agent.get("GenericAgent")

    async def test_normal_tool_call(self, agent):
        process = await agent.create_process()
        resp = await process.action("question", dict(instruction="what is the meaning of life?"))
        assert "42" in resp.data
