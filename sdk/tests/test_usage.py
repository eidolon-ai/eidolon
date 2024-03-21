from unittest.mock import MagicMock, AsyncMock

import pytest

from eidolon_ai_client.client import Agent
from eidolon_ai_client.util.aiohttp import AgentError
from eidolon_ai_sdk.agent.agent import register_program
from eidolon_ai_sdk.builtins.components.usage import UsageMiddleware
from eidolon_ai_sdk.system.dynamic_middleware import Middleware
from eidolon_ai_sdk.system.resources.reference_resource import ReferenceResource
from eidolon_ai_sdk.system.resources.resources_base import Metadata
from eidolon_ai_sdk.util.class_utils import fqn
from eidolon_ai_usage_client.client import UsageClient, UsageLimitExceeded
from eidolon_ai_usage_client.models import UsageSummary, UsageDelta


class CodeAgent:
    @register_program()
    async def do(self):
        return "done"


class MockUsageClient(UsageClient):
    mock = None

    def __new__(cls, *args, **kwargs):
        return cls.mock


@pytest.fixture(scope="module")
async def server(run_app):
    c = ReferenceResource(apiVersion="eidolon/v1", metadata=Metadata(name=UsageClient.__name__),
                          spec=fqn(MockUsageClient))
    u = ReferenceResource(apiVersion="eidolon/v1", metadata=Metadata(name=Middleware.__name__),
                          spec=UsageMiddleware.__name__)
    async with run_app(CodeAgent, c, u) as ra:
        yield ra


@pytest.fixture
def agent(server):
    return Agent.get("CodeAgent")


@pytest.fixture(autouse=True)
def usage_client():
    mock = MagicMock()
    MockUsageClient.mock = mock
    mock.get_summary = AsyncMock()
    mock.record_transaction = AsyncMock()
    mock.delete = AsyncMock()
    yield mock
    MockUsageClient.mock = None


async def test_usage_enforced(agent: Agent, usage_client: MockUsageClient):
    process = await agent.create_process()
    usage_client.get_summary.side_effect = UsageLimitExceeded(UsageSummary(subject='sid', used=1, allowed=1))
    with pytest.raises(AgentError) as e:
        await process.action("do")
    assert e.value.status_code == 429


async def test_usage_recorded(agent: Agent, usage_client: MockUsageClient):
    process = await agent.create_process()
    await process.action("do")
    user = usage_client.record_transaction.await_args[0][0]
    delta: UsageDelta = usage_client.record_transaction.await_args[0][1]
    assert user == 'NOOP_DEFAULT_USER'
    assert delta.used_delta >= 1
