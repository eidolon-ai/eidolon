from contextlib import contextmanager
from typing import Annotated

import pytest
from fastapi import Body
from pydantic import BaseModel

from eidolon_ai_sdk.agent.agent import register_program, register_action, AgentState
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.apu.agents_logic_unit import (
    AgentsLogicUnit,
    AgentsLogicUnitSpec,
)
from eidolon_ai_sdk.apu.agent_call_history import AgentCallHistory
from eidolon_ai_sdk.apu.call_context import CallContext
from eidolon_ai_client.events import SuccessEvent


class FooModel(BaseModel):
    foo: str
    bar: dict


class Foo:
    @register_program()
    async def init(self, name: Annotated[str, Body(embed=True)]):
        """
        init docs
        """
        return AgentState(name="active", data="initialized")

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
async def server(run_app):
    async with run_app(Foo, Bar) as ra:
        yield ra


@pytest.fixture(scope="function")
def conversational_logic_unit(server):
    @contextmanager
    def fn(*agents):
        unit = AgentsLogicUnit(
            spec=AgentsLogicUnitSpec(
                tool_prefix="convo",
                agents=[a.__name__ for a in agents],
            ),
            processing_unit_locator=None,
        )
        yield unit

    return fn


@pytest.mark.asyncio
async def test_can_build_tools(conversational_logic_unit):
    with conversational_logic_unit(Foo) as clu:
        tools = await clu.build_tools(CallContext(process_id="pid"))
        assert len(tools) == 1


@pytest.mark.asyncio
async def test_builds_tools_from_other_messages(conversational_logic_unit):
    with conversational_logic_unit(Foo) as clu:
        await AgentCallHistory(
            parent_process_id="parent_pid",
            parent_thread_id=None,
            machine=AgentOS.current_machine_url(),
            agent="Foo",
            remote_process_id="pid",
            state="idle",
            available_actions=["progress_active", "progress_idle"],
        ).upsert()
        tools = await clu.build_tools(CallContext(process_id="parent_pid"))
        assert len(tools) == 3


async def test_no_body(conversational_logic_unit):
    with conversational_logic_unit(Bar) as clu:
        tools = await clu.build_tools(CallContext(process_id="not_pid"))
        assert len(tools) == 1


async def test_docs(conversational_logic_unit):
    with conversational_logic_unit(Foo) as clu:
        tools = await clu.build_tools(CallContext(process_id="parent_pid"))
        assert tools[0].description(None, None) == "init docs"


async def test_multiple_calls(conversational_logic_unit):
    with conversational_logic_unit(Foo) as clu:
        for _ in range(3):
            tools = await clu.build_tools(CallContext(process_id="parent_pid"))
            output = {type(e) async for e in tools[0].fn(clu, name="foo")}
            assert SuccessEvent in output
