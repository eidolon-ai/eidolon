import pytest

from usage_client.client import UsageClient, UsageLimitExceeded
from usage_client.models import UsageReset, UsageDelta


async def test_get(client: UsageClient):
    summary = await client.get_summary("test")
    assert summary.used == 0
    assert summary.allowed == 600


async def test_record(client: UsageClient):
    await client.record_transaction(
        "test", UsageDelta(used_delta=100, allowed_delta=50)
    )
    summary = await client.get_summary("test")
    assert summary.used == 100
    assert summary.allowed == 650


async def test_reset(client: UsageClient):
    await client.record_transaction(
        "test", UsageDelta(used_delta=100, allowed_delta=50)
    )
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

async def test_uniqueness_is_per_subject(client: UsageClient):
    await client.record_transaction("foo", UsageDelta(used_delta=1))
    await client.record_transaction("bar", UsageDelta(used_delta=2))
    foo = await client.get_summary("foo")
    assert foo.used == 1
    bar = await client.get_summary("bar")
    assert bar.used == 2


async def test_get_summary_raises_over_limit(client: UsageClient):
    await client.record_transaction("foo", UsageDelta(used_delta=601))
    with pytest.raises(UsageLimitExceeded) as e:
        await client.get_summary("foo")
    assert e.value.summary.used == 601
    assert e.value.summary.allowed == 600
    assert str(e.value) == "Usage limit exceeded: 601/600"
