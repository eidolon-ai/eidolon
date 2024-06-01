from typing import Annotated

import pytest
from anthropic import BaseModel
from fastapi import Body
from pydantic import Field

from eidolon_ai_client.client import Agent
from eidolon_ai_client.util.aiohttp import AgentError
from eidolon_ai_sdk.agent.agent import register_program
from eidolon_ai_sdk.agent.simple_agent import SimpleAgent
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.cpu.logic_unit import llm_function, LogicUnit
from eidolon_ai_sdk.system.resources.reference_resource import ReferenceResource
from eidolon_ai_sdk.system.resources.resources_base import Resource, Metadata
from eidolon_ai_sdk.util.class_utils import fqn
from eidolon_ai_sdk.util.replay import ReplayConfig, replay


class MeaningOfLife(LogicUnit):
    @llm_function()
    async def meaning_of_life_tool(self) -> str:
        """
        call this tool to get the meaning of life
        """
        return "42"


class NestedObject(BaseModel):
    int_field: int = None


class ComplexInput(BaseModel):
    array_of_objects: list[NestedObject] = Field(description="An array of objects")


class ComplexAgent:
    @register_program()
    async def do_not_call(self, body: Annotated[ComplexInput, Body(embed=True)]) -> str:
        return "You shouldn't call this function"


def r(name, impl=SimpleAgent.__name__, **kwargs):
    return Resource(
        apiVersion="eidolon/v1",
        kind="Agent",
        metadata=Metadata(name=name),
        spec=dict(implementation=impl, **kwargs),
    )


resources = [
    r("default"),
    r("test_no_vars", actions=[dict(user_prompt="What is the capital of France?")]),
    r("multiple_prompt_args", actions=[dict(user_prompt="{{ a1 }} {{ a2 }}")]),
    r(
        "json_input",
        actions=[
            dict(
                user_prompt="Repeat the following text: {{ one_int }}, {{ two_optional }}, {{ three_default }}",
                input_schema=dict(
                    one_int=dict(type="integer"),
                    two_optional=dict(type="string", default="default"),
                ),
            )
        ],
    ),
    r(
        "json_output",
        actions=[
            dict(
                output_schema=dict(
                    type="object", properties=dict(capital=dict(type="string"), population=dict(type="number"))
                )
            )
        ],
    ),
    r(
        "states",
        actions=[
            dict(name="first", allowed_states=["initialized"], output_state="s2"),
            dict(name="second", allowed_states=["s2"]),
        ],
    ),
    r("system_prompt", system_prompt="You are a helpful assistant, and your favorite country is France"),
    r("refs", agent_refs=["system_prompt"]),
    r("with_tools", cpu=dict(logic_units=[fqn(MeaningOfLife)])),
    r("complex_refs", agent_refs=["complex_agent"]),
    r("complex_agent", impl=fqn(ComplexAgent)),
]


@pytest.fixture(scope="module", autouse=True)
async def server(run_app):
    async with run_app(*resources) as ra:
        yield ra


async def test_default_agent():
    process = await Agent.get("default").create_process()
    resp = await process.action("converse", body="What is the capital of France?")
    assert "paris" in resp.data.lower()


async def test_no_vars():
    process = await Agent.get("test_no_vars").create_process()
    resp = await process.action("converse")
    assert "paris" in resp.data.lower()


async def test_multiple_prompt_args():
    process = await Agent.get("multiple_prompt_args").create_process()
    resp = await process.action("converse", body=dict(a1="What is the capital of", a2="France?"))
    assert "paris" in resp.data.lower()


async def test_generating_title():
    process = await Agent.get("json_output").create_process()
    resp = await process.action("generate_title", body="What is the capital of France?")
    assert "france" in resp.data.lower()
    resp = await process.action("converse", body="What is the capital of France?")
    assert "population" in resp.data
    assert isinstance(resp.data["population"], int) and resp.data["population"] > 0
    assert "paris" in resp.data["capital"].lower()


async def test_json_input():
    process = await Agent.get("json_input").create_process()
    resp = await process.action("converse", body=dict(one_int=1, three_default="three"))
    assert "1, default, three" in resp.data


async def test_json_output():
    process = await Agent.get("json_output").create_process()
    resp = await process.action("converse", body="What is the capital of France?")
    assert "population" in resp.data
    assert isinstance(resp.data["population"], int) and resp.data["population"] > 0
    assert "paris" in resp.data["capital"].lower()


async def test_states():
    process = await Agent.get("states").create_process()
    status = await process.status()
    assert status.state == "initialized"
    assert status.available_actions == ["first", "generate_title"]
    first = await process.action("first", body="What is the capital of France?")
    status = await first.status()
    assert status.state == "s2"
    assert status.available_actions == ["second"]
    assert "paris" in first.data.lower()
    second = await first.action("second", body="What about Spain?")
    status = await second.status()
    assert status.state == "idle"
    assert status.available_actions == ["generate_title"]
    assert "madrid" in second.data.lower()

    with pytest.raises(AgentError) as e:
        await second.action("first", body="What is the capital of France?")
    assert e.value.status_code == 409


async def test_states_bad_initial_program():
    process = await Agent.get("states").create_process()
    with pytest.raises(AgentError) as e:
        await process.action("second", body="What is the capital of France?")
    assert e.value.status_code == 409


async def test_refs():
    process = await Agent.get("refs").create_process()
    resp = await process.action(
        "converse", body="Start a conversation with system_prompt and what its favorite country is."
    )
    assert "france" in resp.data.lower()


async def test_with_tools():
    process = await Agent.get("with_tools").create_process()
    resp = await process.action("converse", body="What is the meaning of life?")
    assert "42" in resp.data.lower()


@pytest.fixture
def record(test_name):
    save_loc = f"resume_points_{test_name}"
    AgentOS.register_resource(
        ReferenceResource(
            apiVersion="eidolon/v1",
            metadata=Metadata(name=ReplayConfig.__name__),
            spec=dict(save_loc=save_loc),
        )
    )
    return save_loc


async def test_with_replay_points(file_memory_loc, record):
    process = await Agent.get("with_tools").create_process()
    await process.action("converse", body="What is the meaning of life?")
    stream = replay(file_memory_loc / record / "001_openai_completion")
    assert "42" in [s async for s in stream]

    with open(file_memory_loc / record / "001_openai_completion" / "data.yaml", "r") as f:
        assert "You are a helpful assistant" in f.read()


async def test_agent_with_complex_refs():
    process = await Agent.get("complex_refs").create_process()
    resp = await process.action("converse", body="What is the capital of France?")
    assert "paris" in resp.data.lower()

