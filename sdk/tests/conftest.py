import os
import pathlib
import threading
from contextlib import asynccontextmanager
from typing import Iterable
from unittest.mock import patch

import httpx
import pytest
import uvicorn
from bson import ObjectId
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from sse_starlette.sse import AppStatus
from vcr.request import Request as VcrRequest
from vcr.stubs import httpx_stubs

import eidolon_ai_sdk.system.process_file_system as process_file_system
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.bin.agent_http_server import start_os, start_app
from eidolon_ai_sdk.cpu.llm.open_ai_llm_unit import OpenAIGPT
from eidolon_ai_sdk.memory.local_file_memory import LocalFileMemory
from eidolon_ai_sdk.memory.local_symbolic_memory import LocalSymbolicMemory
from eidolon_ai_sdk.memory.mongo_symbolic_memory import MongoSymbolicMemory
from eidolon_ai_sdk.memory.similarity_memory import SimilarityMemoryImpl
from eidolon_ai_sdk.system import agent_controller
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.resources.agent_resource import AgentResource
from eidolon_ai_sdk.system.resources.machine_resource import MachineResource
from eidolon_ai_sdk.system.resources.resources_base import Resource, Metadata
from eidolon_ai_sdk.util.class_utils import fqn
from eidolon_ai_sdk.util.posthog import PosthogConfig

PosthogConfig.enabled = False


# we want all tests using the client_builder to use vcr, so we don't send requests to openai
def pytest_collection_modifyitems(items):
    for item in filter(lambda i: "run_app" in i.fixturenames, items):
        item.add_marker(pytest.mark.vcr)
        item.fixturenames.append("patched_vcr_object_handling")
        item.fixturenames.append("deterministic_process_ids")


@pytest.fixture(scope="module")
def app_builder(machine_manager):
    def fn(resources: Iterable[Resource]):
        @asynccontextmanager
        async def manage_lifecycle(_app: FastAPI):
            async with machine_manager() as _machine:
                async with start_os(
                    app=_app,
                    resource_generator=[_machine, *resources] if _machine else resources,
                    machine_name=_machine.metadata.name,
                ):
                    yield
                    print("done")

        return start_app(lifespan=manage_lifecycle)

    return fn


@pytest.fixture(scope="module")
def port():
    # fixing the port. Do we need to be so cool to have a random port?
    return 9080
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.bind(("", 0))
    #     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #     return s.getsockname()[1]


@pytest.fixture(autouse=True)
def vcr_config():
    return dict(
        filter_headers=[("authorization", "XXXXXX"), ("amz-sdk-invocation-id", None), ("X-Amz-Date", None)],
        ignore_localhost=True,
        ignore_hosts=["0.0.0.0", "localhost"],
        record_mode="once",
        match_on=["method", "scheme", "host", "port", "path", "query", "body"],
    )


@pytest.fixture(scope="module")
def run_app(app_builder, port):
    @asynccontextmanager
    async def fn(*agents):
        server_wrapper = []

        def run_server():
            AppStatus.should_exit = False
            AppStatus.should_exit_event = None

            try:
                resources = [
                    a
                    if isinstance(a, Resource)
                    else AgentResource(
                        apiVersion="eidolon/v1",
                        spec=Reference(implementation=fqn(a)),
                        metadata=Metadata(name=a.__name__),
                    )
                    for a in agents
                ]
                app = app_builder(resources)
                # todo, the next line launches uvicorn app as a subprocess so it does not block
                config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info", loop="asyncio")
                server = uvicorn.Server(config)
                server_wrapper.append(server)
                server.run()
                server_wrapper.clear()
                server_wrapper.append("stopped")
            except BaseException as e:
                server_wrapper.clear()
                server_wrapper.append("aborted")
                raise e

        server_thread = threading.Thread(target=run_server)
        server_thread.start()

        try:
            # Wait for the server to start
            while len(server_wrapper) == 0 or not (
                server_wrapper[0] in {"aborted", "stopped"} or server_wrapper[0].started
            ):
                pass
            if server_wrapper[0] in {"aborted", "stopped"}:
                raise Exception("Server failed to start")

            print(f"Server started on port {port}")
            os.environ["EIDOLON_LOCAL_MACHINE"] = f"http://localhost:{port}"
            yield f"http://localhost:{port}"
        finally:
            # server_wrapper[0].force_exit = True
            if isinstance(server_wrapper[0], uvicorn.Server):
                server_wrapper[0].should_exit = True
            server_thread.join()

    return fn


@pytest.fixture(scope="module")
def client_builder(run_app):
    @asynccontextmanager
    async def fn(*agents):
        async with run_app(*agents) as ra:
            with httpx.Client(base_url=ra, timeout=httpx.Timeout(60)) as client:
                yield client

    return fn


@pytest.fixture(scope="module")
def machine_manager(file_memory, symbolic_memory, similarity_memory):
    @asynccontextmanager
    async def fn():
        async with symbolic_memory() as sym, similarity_memory() as sim:
            yield MachineResource(
                apiVersion="eidolon/v1",
                metadata=Metadata(name="test_machine"),
                kind="Machine",
                spec=dict(
                    symbolic_memory=sym,
                    file_memory=file_memory,
                    similarity_memory=sim,
                ),
            )

    return fn


@pytest.fixture
async def machine(machine_manager):
    async with machine_manager() as m:
        instantiated = m.spec.instantiate()
        AgentOS.load_machine(instantiated)
        yield instantiated
        AgentOS.reset()


@pytest.fixture(scope="module")
def local_symbolic_memory(module_identifier):
    @asynccontextmanager
    async def fn():
        ref = Reference(implementation=fqn(LocalSymbolicMemory))
        memory = ref.instantiate()
        await memory.start()
        yield ref
        await memory.stop()
        # Teardown: drop the test database

    return fn


@pytest.fixture(scope="module")
def mongo_symbolic_memory(module_identifier):
    @asynccontextmanager
    async def fn():
        # Setup unique database for test suite
        identifier = module_identifier[:20]
        database_name = f"test_db_{identifier}_{ObjectId()}"  # Unique name for test database
        ref = Reference(
            implementation=fqn(MongoSymbolicMemory),
            mongo_database_name=database_name,
        )
        memory = ref.instantiate()
        await memory.start()
        yield ref
        await memory.stop()
        # Teardown: drop the test database
        connection_string = os.getenv("MONGO_CONNECTION_STRING")
        client = AsyncIOMotorClient(connection_string)
        await client.drop_database(database_name)
        client.close()

    return fn


def pytest_addoption(parser):
    parser.addoption("--symbolic_memory", action="store", default="mongo", help="Symbolic memory implementation to use")


@pytest.fixture(scope="module")
def symbolic_memory(mongo_symbolic_memory, local_symbolic_memory, pytestconfig):
    if pytestconfig.getoption("symbolic_memory").lower() == "local":
        print("Using local symbolic memory")
        return local_symbolic_memory
    else:
        print("Using mongo symbolic memory")
        return mongo_symbolic_memory


@pytest.fixture(scope="module")
def file_memory_loc(tmp_path_factory, module_identifier):
    return tmp_path_factory.mktemp(f"file_memory_{module_identifier}")


@pytest.fixture(scope="module")
def file_memory(file_memory_loc):
    return Reference[LocalFileMemory](root_dir=str(file_memory_loc))


@pytest.fixture(scope="module")
def similarity_memory(tmp_path_factory):
    @asynccontextmanager
    async def cm():
        tmp_dir = tmp_path_factory.mktemp(f"vector_store_{module_identifier}_{ObjectId()}")
        ref = Reference(
            implementation=fqn(SimilarityMemoryImpl),
            vector_store=dict(url=f"file://{tmp_dir}"),
        )
        memory: SimilarityMemoryImpl = ref.instantiate()
        await memory.start()
        yield ref
        await memory.stop()

    return cm


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
        model="gpt-4-vision-preview",
        force_json=False,
        max_tokens=4096,
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
    vcr has a bug around how it handles multipart requests, and it is wired in for everything,
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
def test_name(request):
    return request.node.name


@pytest.fixture()
def deterministic_process_ids(test_name):
    """
    Tool call responses contain the process id, which means it does name make cache hits for vcr.
    This method patches object id for processes so that it returns a deterministic id based on the test name.
    """

    pid_generator = deterministic_id_generator(test_name)
    fid_generator = deterministic_id_generator(test_name + "_file")

    def patched_pid(*args, **kwargs):
        return next(pid_generator)

    def patched_fid(*args, **kwargs):
        return next(fid_generator)

    with patch.object(agent_controller, "ObjectId", new=patched_pid), patch.object(
        process_file_system, "ObjectId", new=patched_fid
    ):
        yield


@pytest.fixture()
def deterministic_file_ids(test_name):
    """
    Tool call responses contain the process id, which means it does name make cache hits for vcr.
    This method patches object id for processes so that it returns a deterministic id based on the test name.
    """

    id_generator = deterministic_id_generator(test_name)

    def patched_ObjectId(*args, **kwargs):
        return next(id_generator)

    with patch.object(process_file_system.bson, "ObjectId", new=patched_ObjectId):
        yield
