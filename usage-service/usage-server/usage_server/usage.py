from __future__ import annotations

import dotenv
import os
from datetime import datetime
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pydantic import BaseModel
from pymongo import DESCENDING
from pymongo.errors import DuplicateKeyError
from typing import Optional

from usage_client.models import UsageDelta, UsageSummary, UsageReset
from usage_server.logger_ import logger

dotenv.load_dotenv()


class _UsageDoc(BaseModel):
    subject: str
    i: int
    used: int
    allowed: int
    created: str
    transaction: UsageDelta | UsageReset
    insertion_retries: int

    def to_summary(self) -> UsageSummary:
        return UsageSummary(subject=self.subject, used=self.used, allowed=self.allowed)


class UsageService:
    _singleton = None
    collection: AsyncIOMotorCollection
    default_allowed: int
    max_insertion_attempts: int

    def __init__(
        self,
        mongo_connection_string=None,
        mongo_database_name=None,
        default_allowed=int(os.environ.get("DEFAULT_ALLOWED", 600)),
        max_insertion_attempts=int(os.environ.get("MAX_INSERTION_ATTEMPTS", 20)),
    ):
        mongo_connection_string = mongo_connection_string or os.environ.get(
            "MONGO_CONNECTION_STR"
        )
        mongo_database_name = mongo_database_name or os.environ.get(
            "USAGE_MONGO_DATABASE_NAME", "eidolon_usage"
        )
        self.collection = AsyncIOMotorClient(mongo_connection_string)[
            mongo_database_name
        ]["usage"]
        self.default_allowed = default_allowed
        self.max_insertion_attempts = max_insertion_attempts

    async def ensure_unique_index(self):
        index_info = await self.collection.index_information()
        for index in index_info.values():
            if index["key"] == [("i", DESCENDING)] and index["unique"]:
                return
        await self.collection.create_index("i", unique=True)

    async def delete(self, subject: str):
        resp = await self.collection.delete_many({"subject": subject})
        return resp.deleted_count

    async def record_transaction(
        self, subject_id: str, transaction: UsageDelta | UsageReset
    ) -> UsageSummary:
        for attempt in range(self.max_insertion_attempts):
            try:
                latest = await self._get_latest(subject_id)
                doc = latest or _UsageDoc(
                    subject=subject_id,
                    i=-1,
                    used=0,
                    allowed=self.default_allowed,
                    created="",
                    transaction=transaction,
                    insertion_retries=0,
                )
                doc.i += 1
                doc.created = datetime.now().isoformat()
                doc.insertion_retries = attempt
                doc.transaction = transaction
                if isinstance(transaction, UsageDelta):
                    doc.used += transaction.used_delta
                    doc.allowed += transaction.allowed_delta
                elif isinstance(transaction, UsageReset):
                    doc.used = transaction.used
                    doc.allowed = transaction.allowed
                else:
                    raise ValueError(f"Invalid transaction type: {transaction}")
                await self.collection.insert_one(doc.dict())
                return doc.to_summary()
            except DuplicateKeyError:
                logger.info(f"Duplicated key error on attempt {attempt}. Retrying...")
            raise HTTPException(
                status_code=503, detail="Failed to insert usage record."
            )

        data = transaction.model_dump()
        data["subject"] = subject_id
        data["created"] = datetime.now().isoformat()
        await self.collection.insert_one(data)

    async def get_usage(self, subject: str) -> UsageSummary:
        latest_record = await self._get_latest(subject)
        if not latest_record:
            logger.info(f"Subject {subject} has no usage records.")
            return UsageSummary(subject=subject, used=0, allowed=self.default_allowed)
        else:
            return latest_record.to_summary()

    async def _get_latest(self, subject) -> Optional[_UsageDoc]:
        found = await self.collection.find_one(
            filter={"subject": subject}, sort=[("i", DESCENDING)]
        )
        return _UsageDoc(**found) if found else None

    @staticmethod
    async def singleton() -> UsageService:
        if not UsageService._singleton:
            UsageService._singleton = UsageService()
            await UsageService._singleton.ensure_unique_index()
        return UsageService._singleton
