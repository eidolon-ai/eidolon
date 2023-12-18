from contextlib import contextmanager
from typing import Annotated

import pytest
from fastapi import Body
from pydantic import BaseModel

from eidos.agent.agent import register_program, register_action
from eidos.cpu.conversational_logic_unit import (
    ConversationalLogicUnit,
    ConversationalSpec,
    ConversationalResponse,
)
from eidos.cpu.llm_message import ToolResponseMessage


class FooModel(BaseModel):
    foo: str
    bar: dict


class Foo:
    @register_program()
    async def init(self, name: Annotated[str, Body()]):
        """
        init docs
        """
        pass

    @register_action("active")
    async def progress_active(self, name: Annotated[str, Body()]) -> str:
        pass

    @register_action("idle")
    async def progress_idle(self, name: FooModel) -> FooModel:
        pass


class Bar:
    @register_program()
    async def init(self):
        pass


@pytest.fixture(scope="module")
def open_api_json(client_builder):
    with client_builder(Foo, Bar) as client:
        yield client.get("/openapi.json").json()


@pytest.fixture
def conversational_logic_unit(open_api_json):
    @contextmanager
    def fn(*agents):
        unit = ConversationalLogicUnit(
            spec=ConversationalSpec(
                location="http://localhost:8080",
                tool_prefix="convo",
                agents=[a.__name__ for a in agents],
            ),
            processing_unit_locator=None,
        )
        unit.set_openapi_json(open_api_json)
        yield unit

    return fn


@pytest.mark.asyncio
async def test_can_build_tools(conversational_logic_unit):
    with conversational_logic_unit(Foo) as clu:
        tools = await clu.build_tools([])
        assert len(tools) == 1


@pytest.mark.asyncio
async def test_builds_tools_from_other_messages(conversational_logic_unit):
    with conversational_logic_unit(Foo) as clu:
        tools = await clu.build_tools(
            [
                ToolResponseMessage(
                    name="convo_Foo_program_init",
                    tool_call_id="1234",
                    result=ConversationalResponse(
                        program="Foo",
                        process_id="pid",
                        state="idle",
                        data="foo",
                        available_actions=["progress_active", "progress_idle"],
                    ).model_dump_json(),
                )
            ]
        )
        assert len(tools) == 3


@pytest.mark.asyncio
async def test_no_body(conversational_logic_unit):
    with conversational_logic_unit(Bar) as clu:
        tools = await clu.build_tools([])
        assert len(tools) == 1


@pytest.mark.asyncio
async def test_docs(conversational_logic_unit):
    with conversational_logic_unit(Foo) as clu:
        tools = await clu.build_tools([])
        assert tools[0].description(None, None) == "init docs"
