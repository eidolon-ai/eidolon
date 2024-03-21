from typing import Annotated

import pytest
import pytest_asyncio
from fastapi import Body, HTTPException

from eidolon_ai_client.client import Agent, ProcessStatus
from eidolon_ai_client.util.aiohttp import AgentError
from eidolon_ai_sdk.agent.agent import register_program
from eidolon_ai_sdk.system.resources.reference_resource import ReferenceResource
from eidolon_ai_sdk.system.resources.resources_base import Metadata


async def run_program(agent, program, **kwargs) -> ProcessStatus:
    process = await Agent.get(agent).create_process()
    return await process.action(program, **kwargs)


class HelloWorld:
    created_processes = set()

    @register_program()
    async def idle(self, name: Annotated[str, Body()]):
        if name.lower() == "hello":
            raise HTTPException(418, "hello is not a name")
        if name.lower() == "error":
            raise Exception("big bad server error")
        return f"Hello, {name}!"


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
