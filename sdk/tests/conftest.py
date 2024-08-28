import os
import pathlib
from contextlib import asynccontextmanager

import httpx
import pytest
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from vcr.request import Request as VcrRequest

from eidolon_ai_sdk.apu.llm.open_ai_llm_unit import OpenAIGPT
from eidolon_ai_sdk.memory.local_file_memory import LocalFileMemory
from eidolon_ai_sdk.memory.local_symbolic_memory import LocalSymbolicMemory
from eidolon_ai_sdk.memory.mongo_symbolic_memory import MongoSymbolicMemory
from eidolon_ai_sdk.memory.similarity_memory import SimilarityMemoryImpl
from eidolon_ai_sdk.system.kernel import AgentOSKernel
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.resources.agent_resource import AgentResource
from eidolon_ai_sdk.system.resources.machine_resource import MachineResource
from eidolon_ai_sdk.system.resources.resources_base import Resource, Metadata
from eidolon_ai_sdk.test_utils.server import serve_thread
from eidolon_ai_sdk.test_utils.vcr import vcr_patch
from eidolon_ai_sdk.util.class_utils import fqn
from eidolon_ai_sdk.util.posthog import PosthogConfig

PosthogConfig.enabled = False


# we want all tests using the client_builder to use vcr, so we don't send requests to openai
def pytest_collection_modifyitems(items):
    for item in filter(lambda i: "run_app" in i.fixturenames, items):
        item.fixturenames.append("patched_vcr")
        item.add_marker(pytest.mark.vcr)


@pytest.fixture()
def patched_vcr(test_name):
    with vcr_patch(test_name):
        yield


@pytest.fixture(autouse=True)
def vcr_config():
    def ignore_some_localhost(request: VcrRequest):
        if (request.host == "0.0.0.0" or request.host == "localhost") and request.port != 11434:  # 11434 is the ollama port
            return None
        elif request.host == "login.microsoftonline.com":
            return None
        return request

    return dict(
        filter_headers=[
            ("authorization", "XXXXXX"),
            ("amz-sdk-invocation-id", None),
            ("X-Amz-Date", None),
            ("x-api-key", None),
        ],
        filter_query_parameters=["cx", "key"],  # google custom search engine id
        filter_post_data_parameters=["client_secret"],
        before_record_request=ignore_some_localhost,
        record_mode="once",
        match_on=["method", "scheme", "host", "port", "path", "query", "body"],
    )


@pytest.fixture(scope="module")
def run_app(machine_manager):
    @asynccontextmanager
    async def fn(*agents):
        async with machine_manager() as machine:
            resources = [a if isinstance(a, Resource) else AgentResource(
                apiVersion="eidolon/v1",
                spec=Reference(implementation=fqn(a)),
                metadata=Metadata(name=a.__name__),
            ) for a in agents]
            with serve_thread([machine, *resources], machine_name=machine.metadata.name) as ra:
                yield ra

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
        AgentOSKernel.load_machine(instantiated)
        yield instantiated
        AgentOSKernel.reset()


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
def similarity_memory(tmp_path_factory, module_identifier):
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
    loc = str(test_dir / "resources" / "dog.png")
    with open(loc, "rb") as f:
        yield f


@pytest.fixture()
def cat(test_dir):
    loc = str(test_dir / "resources" / "cat.png")
    with open(loc, "rb") as f:
        yield f


@pytest.fixture()
def test_name(request):
    return request.node.name
