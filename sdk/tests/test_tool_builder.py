from typing import List

import pytest
from pydantic import BaseModel

from eidolon_ai_client import client
from eidolon_ai_sdk.system.resources.resources_base import Resource, Metadata
from eidolon_ai_sdk.system.tool_builder import ToolUnit
from eidolon_ai_sdk.util.class_utils import fqn


def r(tool: ToolUnit, agent_name: str = None):
    return Resource(
        apiVersion="eidolon/v1",
        kind="Agent",
        metadata=Metadata(name=agent_name or type(tool).__name__),
        spec=dict(
            implementation="SimpleAgent",
            apu=dict(logic_units=[dict(implementation=fqn(type(tool)), **tool.model_dump())])
        ),
    )


class BasicTool(ToolUnit):
    foo: str


@BasicTool.tool()
def get_magic_word(spec: BasicTool):
    return spec.foo


class DynamicTool(ToolUnit):
    tools: List[str]


@DynamicTool.dynamic_contract
def fn(spec: DynamicTool):
    for tool in spec.tools:
        @DynamicTool.tool(name=tool)
        async def tool_call():
            return tool


class CustomDescription(ToolUnit):
    pass


@CustomDescription.tool(name="foo", description="will return foo, bar, baz")
def cd_fn():
    return "foo", "bar", "baz"


class SimpleSigTool(ToolUnit):
    pass


@SimpleSigTool.tool()
def add(a: int, b: int):
    """Add two numbers together. giggity."""
    return a + b


class PydanticSigTool(ToolUnit):
    pass


class PhilosopherDescription(BaseModel):
    philosopher_name: str
    school_of_thought: str


@PydanticSigTool.tool()
def meaning_of_life(philosopher: PhilosopherDescription):
    if philosopher.philosopher_name == "Douglas Adams" and philosopher.school_of_thought == "Hitchhiker's Guide to the Galaxy":
        return "Isn't it obvious: 42!"
    else:
        return "Unknown for the provided philosopher, school of thought"


@pytest.fixture(scope="module", autouse=True)
async def server(run_app):
    async with run_app(
        r(BasicTool(foo="bar")),
        r(DynamicTool(tools=["foo", "bar"])),
        r(CustomDescription()),
        r(SimpleSigTool()),
        r(PydanticSigTool()),
    ) as ra:
        yield ra


async def test_build_tools():
    process = await client.Agent.get(BasicTool.__name__).create_process()
    resp = await process.action("converse", body="What is the magic word?")
    assert "bar" in resp.data


async def test_dynamic_tools():
    process = await client.Agent.get(DynamicTool.__name__).create_process()
    resp = await process.action("converse", body="What tools do you have?")
    assert "foo" in resp.data
    assert "bar" in resp.data


async def test_custom_description():
    process = await client.Agent.get(CustomDescription.__name__).create_process()
    resp = await process.action("converse", body="describe the foo tool as it is shown to you")
    assert "baz" in resp.data


async def test_simple_signature():
    process = await client.Agent.get(SimpleSigTool.__name__).create_process()
    resp = await process.action("converse", body="What is 2 + 3? Use your tools give me the answer, and also the description of the tool you are given, including anything odd about it.")
    assert "5" in resp.data
    assert "giggity" in resp.data.lower()


async def test_complex_signature():
    process = await client.Agent.get(PydanticSigTool.__name__).create_process()
    resp = await process.action("converse", body="What is the meaning of life according to \"Douglas Adams\" within \"Hitchhiker's Guide to the Galaxy\"? Use the tool provided and return the exact response given to you")
    assert "42" in resp.data
    assert "obvious" in resp.data
