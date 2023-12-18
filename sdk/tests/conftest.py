import os
import pathlib
from contextlib import asynccontextmanager, contextmanager
from typing import Iterable
from unittest.mock import patch

import pytest
from bson import ObjectId
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from vcr.request import Request as VcrRequest
from vcr.stubs import httpx_stubs

from eidos.cpu.llm.open_ai_llm_unit import OpenAiGPTSpec, OpenAIGPT
from eidos.memory.agent_memory import VectorMemory
from eidos.memory.local_file_memory import LocalFileMemory, LocalFileMemoryConfig
from eidos.memory.mongo_symbolic_memory import MongoSymbolicMemory
from eidos.memory.noop_memory import NoopVectorStore
from eidos.bin.agent_http_server import start_os
from eidos.system.reference_model import Reference
from eidos.system.resources import AgentResource
from eidos.system.resources_base import Resource, Metadata
from eidos.util.class_utils import fqn
import eidos.system.processes as processes


# we want all tests using the client_builder to use vcr so we don't send requests to openai
def pytest_collection_modifyitems(items):
    for item in filter(lambda i: "client_builder" in i.fixturenames, items):
        item.add_marker(pytest.mark.vcr)
        item.fixturenames.append("patched_vcr_object_handling")
        item.fixturenames.append("deterministic_process_ids")


@pytest.fixture(autouse=True)
def vcr_config():
    return dict(
        filter_headers=[("authorization", "XXXXXX")],
        ignore_localhost=True,
        ignore_hosts=["testserver"],
        record_mode="new_episodes",
        match_on=["method", "scheme", "host", "port", "path", "query", "body"],
    )


@pytest.fixture(scope="module")
def app_builder(machine_manager):
    def fn(resources: Iterable[Resource]):
        @asynccontextmanager
        async def manage_lifecycle(_app: FastAPI):
            async with machine_manager() as _machine:
                async with start_os(_app, [_machine, *resources] if _machine else resources):
                    yield

        return FastAPI(lifespan=manage_lifecycle)

    return fn


@pytest.fixture(scope="module")
def client_builder(app_builder):
    @contextmanager
    def fn(*agents):
        resources = [
            a
            if isinstance(a, Resource)
            else AgentResource(
                apiVersion="eidolon/v1",
                implementation=fqn(a),
                metadata=Metadata(name=a.__name__),
            )
            for a in agents
        ]
        app = app_builder(resources)

        def make_request(method):
            async def fn(url, args=None):
                async with AsyncClient(app=app, base_url="http://0.0.0.0:8080") as client:
                    return (await client.request(method, url, json=args)).json()

            return fn

        with TestClient(app) as client, patch(
            "eidos.cpu.conversational_logic_unit._agent_request"
        ) as _agent_request, patch("eidos.cpu.conversational_logic_unit._get_openapi_schema") as _get_openapi_schema:
            _agent_request.side_effect = make_request("POST")
            _get_openapi_schema.side_effect = make_request("GET")
            yield client

    return fn


@pytest.fixture(scope="module")
def machine_manager(file_memory, symbolic_memory, similarity_memory):
    @asynccontextmanager
    async def fn():
        async with symbolic_memory() as sm:
            yield Resource(
                apiVersion="eidolon/v1",
                kind="Machine",
                spec=dict(
                    symbolic_memory=sm,
                    file_memory=file_memory,
                    similarity_memory=similarity_memory,
                ),
            )

    return fn


@pytest.fixture(scope="module")
def symbolic_memory(module_identifier):
    @asynccontextmanager
    async def fn():
        # Setup unique database for test suite
        identifier = module_identifier[:20]
        database_name = f"test_db_{identifier}_{ObjectId()}"  # Unique name for test database
        ref = Reference(
            implementation=fqn(MongoSymbolicMemory),
            spec=dict(mongo_database_name=database_name),
        )
        memory = ref.instantiate()
        memory.start()
        yield ref
        memory.stop()
        # Teardown: drop the test database
        connection_string = os.getenv("MONGO_CONNECTION_STRING")
        client = AsyncIOMotorClient(connection_string)
        await client.drop_database(database_name)
        client.close()

    return fn


@pytest.fixture(scope="module")
def file_memory(tmp_path_factory, module_identifier):
    storage_loc = tmp_path_factory.mktemp(f"file_memory_{module_identifier}")
    spec = LocalFileMemoryConfig(root_dir=str(storage_loc))
    return Reference[LocalFileMemory](spec=spec)


@pytest.fixture(scope="module")
def similarity_memory():
    return Reference[VectorMemory](
        spec=dict(
            vector_store=dict(implementation=fqn(NoopVectorStore)),
        )
    )


@pytest.fixture(scope="module", autouse=True)
def module_identifier(request):
    return request.node.name.replace(".", "_")


@pytest.fixture(scope="session")
def test_dir():
    return pathlib.Path(__file__).parent


@pytest.fixture(scope="module")
def llm(test_dir, module_identifier):
    return Reference(
        implementation=fqn(OpenAIGPT),
        spec=OpenAiGPTSpec(
            model="gpt-4-vision-preview",
            force_json=False,
            max_tokens=4096,
        ),
    )


@pytest.fixture()
def dog(test_dir):
    loc = str(test_dir / "images" / "dog.png")
    with open(loc, "rb") as f:
        yield f


@pytest.fixture()
def cat(test_dir):
    loc = str(test_dir / "images" / "cat.png")
    with open(loc, "rb") as f:
        yield f


@pytest.fixture
def patched_vcr_object_handling():
    """
    vcr has a bug around how it handles multi-part requests, and it is wired in for everything,
    even the fake test client requests, so we need to pipe the body through ourselves
    """

    def my_custom_function(httpx_request, **kwargs):
        uri = str(httpx_request.url)
        headers = dict(httpx_request.headers)
        return VcrRequest(httpx_request.method, uri, httpx_request, headers)

    with patch.object(httpx_stubs, "_make_vcr_request", new=my_custom_function):
        yield


def deterministic_id_generator(test_name):
    count = 0
    while True:
        yield f"{test_name}_{count}"
        count += 1


@pytest.fixture()
def deterministic_process_ids(request):
    """
    Tool call responses contain the process id, which means it does name make cache hits for vcr.
    This method patches object id for processes so that it returns a deterministic id based on the test name.
    """

    test_name = request.node.name
    id_generator = deterministic_id_generator(test_name)
    def patched_ObjectId(*args, **kwargs):
        return next(id_generator)

    with patch.object(processes.bson, "ObjectId", new=patched_ObjectId):
        yield
