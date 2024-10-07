import asyncio

import pytest

from eidolon_ai_sdk.agent.crew.distributed_lock import DistributedLock, LockException


async def test_can_acquire(machine):
    await DistributedLock.acquire("test_lock", 1000)


async def test_keys_are_unique(machine):
    await DistributedLock.acquire("test_lock", 1000)
    await DistributedLock.acquire("test_lock2", 1000)


async def test_acquire_holds(machine):
    await DistributedLock.acquire("test_lock", 1000)
    with pytest.raises(LockException):
        await DistributedLock.acquire("test_lock", 1000, timeout=0)


async def test_acquire_releases_naturally(machine):
    await DistributedLock.acquire("test_lock", 5)
    await asyncio.sleep(.1)
    await DistributedLock.acquire("test_lock", 1000, timeout=0)


async def test_acquire_can_wait(machine):
    await DistributedLock.acquire("test_lock", 100)
    await DistributedLock.acquire("test_lock", 1000, timeout=1000)


async def test_acquire_only_waits_so_long(machine):
    await DistributedLock.acquire("test_lock", 2000)
    with pytest.raises(LockException):
        await DistributedLock.acquire("test_lock", 1000, timeout=100)


async def test_renew(machine):
    lock = await DistributedLock.acquire("test_lock", 0)
    await lock.renew(1000)
    with pytest.raises(LockException):
        await DistributedLock.acquire("test_lock", 1000, timeout=0)


async def test_release(machine):
    lock = await DistributedLock.acquire("test_lock", 1000)
    await lock.release()
    await DistributedLock.acquire("test_lock", 1000, timeout=0)
