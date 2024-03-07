import pytest
import requests
from pytest_asyncio import fixture
from starlette.requests import Request

from eidolon_ai_client.client import Agent
from eidolon_ai_client.util.aiohttp import AgentError
from eidolon_ai_sdk.agent.agent import register_program
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.security.security_manager import AuthenticationProcessor, Permission, User
from eidolon_ai_sdk.system.resources.reference_resource import ReferenceResource
from eidolon_ai_sdk.system.resources.resources_base import Metadata
from eidolon_ai_sdk.util.class_utils import fqn


class HelloWorld:
    @register_program()
    async def hello_world(self) -> str:
        return "Hello, world!"


class TestAuthenticationProcessor(AuthenticationProcessor):
    user: User

    def __init__(self):
        self.user = User(id="default")

    def reset(self, test_name):
        self.user.id = test_name
        self.user.functional_permissions = [
            "eidolon/agents/HelloWorld/processes/create",
            "eidolon/agents/HelloWorld/processes/read",
            "eidolon/agents/HelloWorld/processes/update",
            "eidolon/agents/HelloWorld/processes/delete",
        ]

    def remove_permission(self, permission: Permission):
        self.user.functional_permissions.remove(f"eidolon/agents/HelloWorld/processes/{permission}")

    def remove_all_permissions(self):
        self.user.functional_permissions.clear()

    async def check_auth(self, request: Request) -> User:
        return self.user


@fixture(scope="module")
async def server(run_app):
    auth_processor = ReferenceResource(
        apiVersion="eidolon/v1", metadata=Metadata(name="AuthenticationProcessor"), spec=fqn(TestAuthenticationProcessor)
    )
    async with run_app(HelloWorld, auth_processor) as ra:
        yield ra


@fixture()
def auth(test_name, server) -> TestAuthenticationProcessor:
    processor: TestAuthenticationProcessor = AgentOS.security_manager.authentication_processor
    processor.reset(test_name)
    yield processor


@fixture()
def agent(server, auth) -> Agent:
    return Agent.get("HelloWorld")


def test_system_health_does_not_require_permissions(agent, auth):
    auth.remove_all_permissions()
    response = requests.get(agent.machine + "/system/health")
    assert response.status_code == 200


def test_open_api_does_not_require_permissions(auth, agent):
    auth.remove_all_permissions()
    response = requests.get(agent.machine + "/openapi.json")
    assert response.status_code == 200


async def test_system_list_processes_requires_read_permissions(auth, agent: Agent):
    await agent.create_process()
    auth.remove_permission("read")
    response = requests.get(agent.machine + "/system/processes")
    assert response.status_code == 200
    assert not response.json()  # response is naked list, which should change, but is fine for now


async def test_system_list_processes_requires_filters_resources_by_user(auth, agent: Agent):
    await agent.create_process()
    auth.user.id = "somebody_else"
    response = requests.get(agent.machine + "/system/processes")
    assert response.status_code == 200
    assert not response.json()  # response is naked list, which should change, but is fine for now


async def test_missing_read_is_identical_to_bad_agent(auth, agent: Agent):
    with pytest.raises(AgentError) as e2:
        await Agent.get("BadAgent").process("foo").status()
    assert e2.value.status_code == 404
    assert e2.value.response.json() == {"detail": "Not Found"}

    auth.remove_permission("read")
    with pytest.raises(AgentError) as e3:
        await agent.process("foo").status()
    assert e3.value.status_code == e2.value.status_code
    assert e3.value.response.json() == e2.value.response.json()


async def test_resource_read_missing_identical_to_bad_resource(auth, agent: Agent):
    created = await agent.create_process()
    found = await agent.process(created.process_id).status()
    assert found.process_id == created.process_id

    auth.user.id = "somebody_else"

    with pytest.raises(AgentError) as e1:
        await agent.process(created.process_id).status()
    assert e1.value.status_code == 404
    assert e1.value.response.json() == {"detail": "Process Not Found"}

    with pytest.raises(AgentError) as e2:
        await agent.process("foo").status()
    assert e2.value.status_code == e1.value.status_code
    assert e2.value.response.json() == e1.value.response.json()


async def test_create_process_no_agent_Read(auth, agent: Agent):
    auth.remove_permission("read")
    with pytest.raises(AgentError) as e1:
        await agent.create_process()
    assert e1.value.status_code == 404
    assert e1.value.response.json() == {"detail": "Not Found"}


async def test_update_process_no_read_response_matches_missing_response(auth, agent: Agent):
    auth.remove_permission("read")
    with pytest.raises(AgentError) as e1:
        await agent.process("foo").action("hello_world")
    assert e1.value.status_code == 404
    assert e1.value.response.json() == {"detail": "Not Found"}


async def test_update_process_no_update_shows_403(auth, agent: Agent):
    auth.remove_permission("update")
    with pytest.raises(AgentError) as e1:
        await agent.process("foo").action("hello_world")
    assert e1.value.status_code == 403
    assert e1.value.response.json() == {"detail": "Missing Permission: update"}


async def test_update_process_missing_resource_perms(auth, agent: Agent):
    with pytest.raises(AgentError) as e1:
        await agent.process("foo").action("hello_world")
    assert e1.value.status_code == 404
    assert e1.value.response.json() == {"detail": "Process Not Found"}


async def test_delete_process_no_delete_shows_403(auth, agent: Agent):
    auth.remove_permission("delete")
    with pytest.raises(AgentError) as e1:
        await agent.process("foo").delete()
    assert e1.value.status_code == 403
    assert e1.value.response.json() == {"detail": "Missing Permission: delete"}


async def test_delete_process_no_read_shows_404(auth, agent: Agent):
    auth.remove_permission("read")
    with pytest.raises(AgentError) as e1:
        await agent.process("foo").delete()
    assert e1.value.status_code == 404
    assert e1.value.response.json() == {"detail": "Not Found"}


async def test_get_process_events_no_read_shows_404(auth, agent: Agent):
    auth.remove_permission("read")
    with pytest.raises(AgentError) as e1:
        await agent.process("foo").events()
    assert e1.value.status_code == 404
    assert e1.value.response.json() == {"detail": "Not Found"}


async def test_agent_list_processes_requires_read_permissions(auth, agent: Agent):
    auth.remove_permission("read")
    with pytest.raises(AgentError) as e1:
        await agent.processes()
    assert e1.value.status_code == 404
    assert e1.value.response.json() == {"detail": "Not Found"}


async def test_list_processes_filters_by_resource_perms(auth, agent: Agent):
    await agent.create_process()
    process_response = await agent.processes()
    assert process_response.total == 1
    assert process_response.processes

    auth.user.id = "somebody_else"
    process_response_2 = await agent.processes()
    assert process_response_2.total == 0
    assert not process_response_2.processes
