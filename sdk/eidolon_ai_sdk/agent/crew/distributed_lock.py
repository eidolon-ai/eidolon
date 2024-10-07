import asyncio
from datetime import datetime, timedelta
from typing import ClassVar

from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.system.processes import MongoDoc


class LockException(Exception):
    pass


class DistributedLock(MongoDoc, extra="allow"):
    collection: ClassVar[str] = "distributed_lock"
    owner: str
    created: datetime = None
    updated: datetime = None
    expiration: datetime
    metadata: dict = {}

    @property
    def record_id(self):
        return self._id

    @classmethod
    async def acquire(cls, key: str, duration, timeout: int = -1):
        now = datetime.now()
        lock_expiration = now + timedelta(milliseconds=duration)
        timout_datetime = now + timedelta(milliseconds=timeout)
        while timeout < 0 or now <= timout_datetime:
            now = datetime.now()
            # todo, this is not the right way to do comparison, google this when I have internet
            query = {"_id": key, "expiration": {"lt": lock_expiration}}
            doc = {
                "_id": key,
                "owner": str(ObjectId()),
                "created": str(now.isoformat()),
                "updated": str(now.isoformat()),
                "expiration": str(lock_expiration)
            }
            try:
                await AgentOS.symbolic_memory.upsert_one(cls.collection, query=query, document=doc)
                return DistributedLock(**doc)
            except DuplicateKeyError:
                logger.debug("Lock record already exists:", key)

        raise LockException(f"Timeout waiting to acquire lock for record `{key}`")

    async def renew(self, duration):
        query = {"_id": self.record_id, "owner": self.owner}
        now = datetime.now()
        doc = {
            "_id": self.record_id,
            "updated": str(now.isoformat()),
            "expiration": str((now + timedelta(milliseconds=duration)).isoformat())
        }
        try:
            await AgentOS.symbolic_memory.upsert_one(self.collection, query=query, document=doc)
            acc = self.model_dump()
            acc.update(doc)
            return DistributedLock(**acc)
        except DuplicateKeyError:
            raise LockException(f"Lock could not be renewed for record `{self.record_id}`")

    async def release(self):
        await AgentOS.symbolic_memory.delete(self.collection, {"_id": self.record_id, "owner": self.owner})


async def _refresh_lock(lock: DistributedLock, duration: int, interval: int):
    try:
        while True:
            await asyncio.sleep(interval / 1000)
            await lock.renew(duration)
    except LockException:
        logger.exception("Error automatically refreshing lock")


async def managed_lock(key: str, duration: int = 15000, refresh_interval: int = 5000, timeout: int = -1):
    lock = await DistributedLock.acquire(key, duration, timeout)
    refresh_in_background = asyncio.create_task(_refresh_lock(lock, duration, refresh_interval))
    try:
        yield lock
    finally:
        refresh_in_background.cancel("Completed task, releasing lock")
        await lock.release()
