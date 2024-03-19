from usage_client.client import UsageClient
from usage_client.models import UsageReset, UsageDelta


async def test_get(client: UsageClient):
    summary = await client.get_summary("test")
    assert summary.used == 0
    assert summary.allowed == 600


async def test_record(client: UsageClient):
    await client.record_transaction("test", UsageDelta(used_delta=100, allowed_delta=50))
    summary = await client.get_summary("test")
    assert summary.used == 100
    assert summary.allowed == 650


async def test_reset(client: UsageClient):
    await client.record_transaction("test", UsageDelta(used_delta=100, allowed_delta=50))
    await client.record_transaction("test", UsageReset())
    summary = await client.get_summary("test")
    assert summary.used == 0
    assert summary.allowed == 600


async def test_reset_non_defaults(client: UsageClient):
    await client.record_transaction("test", UsageReset(used=1, allowed=2))
    summary = await client.get_summary("test")
    assert summary.used == 1
    assert summary.allowed == 2


async def test_adding_incrementally_works(client: UsageClient):
    for i in range(100):
        await client.record_transaction("foo", UsageDelta(used_delta=1))
    summary = await client.get_summary("foo")
    assert summary.used == 100
    assert summary.allowed == 600
