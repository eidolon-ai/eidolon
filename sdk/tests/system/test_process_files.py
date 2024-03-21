from typing import Annotated

import pytest
import pytest_asyncio
from fastapi import Body, HTTPException, Request
from opentelemetry.trace import get_current_span

from eidolon_ai_client.client import Agent, ProcessStatus
from eidolon_ai_client.events import (
    StringOutputEvent,
    StartStreamContextEvent,
)
from eidolon_ai_client.util.aiohttp import AgentError
from eidolon_ai_sdk.agent.agent import register_program
from eidolon_ai_sdk.system.resources.reference_resource import ReferenceResource
from eidolon_ai_sdk.system.resources.resources_base import Metadata
from eidolon_ai_sdk.util.stream_collector import stream_manager


async def run_program(agent, program, **kwargs) -> ProcessStatus:
    process = await Agent.get(agent).create_process()
    return await process.action(program, **kwargs)


class HelloWorld:
    created_processes = set()

    @classmethod
    async def create_process(cls, process_id):
        HelloWorld.created_processes.add(process_id)

    @classmethod
    async def delete_process(cls, process_id):
        HelloWorld.created_processes.remove(process_id)

    @register_program()
    async def recurse(self, request: Request, n: Annotated[int, Body()]):
        child = None
        if n > 0:
            process = await Agent.get("HelloWorld").create_process()
            rtn = await process.action("recurse", json=str(n - 1))
            child = rtn.data
        span = get_current_span()
        span_context = span.get_span_context()
        parent = None
        if hasattr(span, "parent") and span.parent:
            parent = dict(trace=format(span.parent.trace_id, "032x"), span=format(span.parent.span_id, "016x"))
        return dict(
            self=dict(trace=format(span_context.trace_id, "032x"), span=format(span_context.span_id, "016x")),
            child=child,
            parent=parent,
            traceparent=request.headers.get("traceparent"),
        )

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
    return stream_manager(stream, StartStreamContextEvent(context_id=context, title=context))


@pytest.fixture(autouse=True)
def manage_hello_world_state():
    HelloWorld.created_processes = set()
    yield
    HelloWorld.created_processes = set()


class TestProcessFiles:
    @pytest_asyncio.fixture(scope="class")
    async def server(self, run_app):
        open_tel = ReferenceResource(
            apiVersion="eidolon/v1", metadata=Metadata(name="OpenTelemetryManager"), spec="BatchOpenTelemetry"
        )

        async with run_app(HelloWorld, open_tel) as ra:
            yield ra

    @pytest.fixture(scope="function")
    def agent(self, server) -> Agent:
        return Agent.get("HelloWorld")

    async def test_can_upload(self, agent):
        bts = "Hello, World!".encode("utf-8")
        process_status = await agent.create_process()
        process = agent.process(process_status.process_id)
        file_id = await process.upload_file(bts)
        assert bts == await process.download_file(file_id)

    async def test_can_delete(self, agent):
        bts = "Hello, World!".encode("utf-8")
        process_status = await agent.create_process()
        process = agent.process(process_status.process_id)
        file_id = await process.upload_file(bts)
        await process.delete_file(file_id)

        # now try again and expect a 404
        with pytest.raises(AgentError):
            await process.delete_file(file_id)
