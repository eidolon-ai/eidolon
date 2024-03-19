from typing import Set

import pytest
import requests
from pytest_asyncio import fixture
from starlette.requests import Request

from eidolon_ai_client.client import Agent, Machine
from eidolon_ai_client.util.aiohttp import AgentError
from eidolon_ai_sdk.agent.agent import register_program
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.security.functional_authorizer import FunctionalAuthorizer
from eidolon_ai_sdk.security.permissions import PermissionException, Permission
from eidolon_ai_sdk.security.authentication_processor import AuthenticationProcessor
from eidolon_ai_sdk.security.user import User
from eidolon_ai_sdk.system.resources.reference_resource import ReferenceResource
from eidolon_ai_sdk.system.resources.resources_base import Metadata
from eidolon_ai_sdk.util.class_utils import fqn


class HelloWorld:
    @register_program()
    async def hello_world(self) -> str:
        return "Hello, world!"


class TestAuthenticationProcessor(AuthenticationProcessor):
    user: User

    def reset(self, test_name):
        self.user = User(id=test_name)

    async def check_auth(self, request: Request) -> User:
        return self.user


class TestFunctionalAuthorizer(FunctionalAuthorizer):
    perms: Set[str]

    def reset(self):
        self.perms = {
            "agents/HelloWorld/processes/create",
            "agents/HelloWorld/processes/read",
            "agents/HelloWorld/processes/update",
            "agents/HelloWorld/processes/delete",
        }

    def remove_permission(self, permission: Permission):
        self.perms.remove(f"agents/HelloWorld/processes/{permission}")

    def remove_all_permissions(self):
        self.perms.clear()

    async def check_functional_perms(self, permissions: Set[Permission], target):
        missing: Set[Permission] = {p for p in permissions if f"{target}/{p}" not in self.perms}
        if missing:
            raise PermissionException(missing)


@fixture(scope="module")
async def server(run_app):
    auth_processor = ReferenceResource(
        apiVersion="eidolon/v1", metadata=Metadata(name="AuthenticationProcessor"), spec=fqn(TestAuthenticationProcessor)
    )
    functional_authorizer = ReferenceResource(
        apiVersion="eidolon/v1", metadata=Metadata(name="FunctionalAuthorizer"), spec=fqn(TestFunctionalAuthorizer)
    )

    async with run_app(HelloWorld, auth_processor, functional_authorizer) as ra:
        yield ra


@fixture()
def authentication(test_name, server) -> TestAuthenticationProcessor:
    processor: TestAuthenticationProcessor = AgentOS.security_manager.authentication_processor
    processor.reset(test_name)
    yield processor


@fixture()
def authorization(server) -> TestFunctionalAuthorizer:
    processor: TestFunctionalAuthorizer = AgentOS.security_manager.functional_authorizer
    processor.reset()
    yield processor


@fixture()
def agent(server, authentication, authorization) -> Agent:
    return Agent.get("HelloWorld")


def test_system_health_does_not_require_permissions(agent, authorization):
    authorization.remove_all_permissions()
    response = requests.get(agent.machine + "/system/health")
    assert response.status_code == 200


def test_open_api_does_not_require_permissions(authorization, agent):
    authorization.remove_all_permissions()
    response = requests.get(agent.machine + "/openapi.json")
    assert response.status_code == 200


async def test_system_list_processes_requires_read_permissions(authorization, agent: Agent):
    await agent.create_process()
    authorization.remove_permission("read")
    response = await Machine().processes()
    assert response.total == 0


async def test_system_list_processes_requires_filters_resources_by_user(authentication, agent: Agent):
    await agent.create_process()
    authentication.user.id = "somebody_else"
    response = await Machine().processes()
    assert response.total == 0


async def test_get_process_missing_agent(authorization, agent: Agent):
    with pytest.raises(AgentError) as e2:
        await Agent.get("BadAgent").process("foo").status()
    assert e2.value.status_code == 404
    assert e2.value.response.json() == {"detail": "Process Not Found"}


async def test_get_process_missing_functional_perms(authorization, agent: Agent):
    pid = await agent.create_process()
    authorization.remove_permission("read")
    with pytest.raises(AgentError) as e3:
        await agent.process(pid.process_id).status()
    assert e3.value.status_code == 403
    assert e3.value.response.json() == {"detail": "Missing Permission: read"}


async def test_resource_read_missing(authentication, agent: Agent):
    created = await agent.create_process()
    found = await agent.process(created.process_id).status()
    assert found.process_id == created.process_id

    authentication.user.id = "somebody_else"

    with pytest.raises(AgentError) as e1:
        await agent.process(created.process_id).status()
    assert e1.value.status_code == 404
    assert e1.value.response.json() == {"detail": "Process Not Found"}

    with pytest.raises(AgentError) as e2:
        await agent.process("foo").status()
    assert e2.value.status_code == e1.value.status_code
    assert e2.value.response.json() == e1.value.response.json()


async def test_create_process_no_agent_Read(authorization, agent: Agent):
    authorization.remove_permission("read")
    with pytest.raises(AgentError) as e1:
        await agent.create_process()
    assert e1.value.status_code == 403
    assert e1.value.response.json() == {"detail": "Missing Permission: read"}


async def test_update_process_no_read_functional_403(authorization, agent: Agent):
    authorization.remove_permission("read")
    with pytest.raises(AgentError) as e1:
        await agent.process("foo").action("hello_world")
    assert e1.value.status_code == 403
    assert e1.value.response.json() == {"detail": "Missing Permission: read"}


async def test_update_process_no_update_shows_403(authorization, agent: Agent):
    authorization.remove_permission("update")
    with pytest.raises(AgentError) as e1:
        await agent.process("foo").action("hello_world")
    assert e1.value.status_code == 403
    assert e1.value.response.json() == {"detail": "Missing Permission: update"}


async def test_update_process_missing_resource_perms(authorization, agent: Agent):
    with pytest.raises(AgentError) as e1:
        await agent.process("foo").action("hello_world")
    assert e1.value.status_code == 404
    assert e1.value.response.json() == {"detail": "Process Not Found"}


async def test_delete_process_no_delete_shows_403(authorization, agent: Agent):
    pid = await agent.create_process()
    authorization.remove_permission("delete")
    with pytest.raises(AgentError) as e1:
        await agent.process(pid.process_id).delete()
    assert e1.value.status_code == 403
    assert e1.value.response.json() == {"detail": "Missing Permission: delete"}


async def test_delete_process_no_read_shows_403(authorization, agent: Agent):
    pid = await agent.create_process()
    authorization.remove_permission("read")
    with pytest.raises(AgentError) as e1:
        await agent.process(pid.process_id).delete()
    assert e1.value.status_code == 403
    assert e1.value.response.json() == {"detail": "Missing Permission: read"}


async def test_get_process_events_no_read_shows_403(authorization, agent: Agent):
    pid = await agent.create_process()
    authorization.remove_permission("read")
    with pytest.raises(AgentError) as e1:
        await agent.process(pid.process_id).events()
    assert e1.value.status_code == 403
    assert e1.value.response.json() == {"detail": "Missing Permission: read"}


async def test_list_processes_filters_by_resource_perms(authentication, agent: Agent):
    await agent.create_process()
    process_response = await agent.processes()
    assert process_response.total == 1
    assert process_response.processes

    authentication.user.id = "somebody_else"
    process_response_2 = await agent.processes()
    assert process_response_2.total == 0
    assert not process_response_2.processes
