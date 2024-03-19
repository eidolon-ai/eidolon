import dotenv
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from typing import Tuple, Optional

from usage_client.models import UsageDelta, UsageSummary, UsageReset as _UsageReset
from usage_server.logger_ import logger

dotenv.load_dotenv()


class UsageReset(_UsageReset):
    allowed: int = int(os.environ.get("DEFAULT_ALLOWED", 600))


class UsageService:
    db: AsyncIOMotorCollection
    default_allowed: int

    def __init__(
        self,
        mongo_connection_string=None,
        mongo_database_name=None,
        default_allowed=int(os.environ.get("DEFAULT_ALLOWED", 600)),
    ):
        mongo_connection_string = mongo_connection_string or os.environ.get(
            "MONGO_CONNECTION_STR"
        )
        mongo_database_name = mongo_database_name or os.environ.get(
            "USAGE_MONGO_DATABASE_NAME", "eidolon_usage"
        )
        client = AsyncIOMotorClient(mongo_connection_string)
        self.db = client[mongo_database_name]["usage"]
        self.default_allowed = default_allowed

    async def delete(self, subject: str):
        resp = await self.db.delete_many({"subject": subject})
        return resp.deleted_count

    async def record_transaction(
        self, subject_id: str, transaction: UsageDelta | UsageReset
    ):
        data = transaction.model_dump()
        data["subject"] = subject_id
        data["created"] = datetime.now().isoformat()
        await self.db.insert_one(data)

    async def get_usage(self, subject: str) -> UsageSummary:
        latest_record, summary = await self._get_usage(subject)
        if not latest_record:
            logger.info(f"Subject {subject} has no usage records.")
        return summary

    async def create_breakpoint_record(self, subject) -> UsageSummary:
        latest_record, summary = await self._get_usage(subject)
        if latest_record:
            await self.db.update_one(
                {"_id": latest_record["_id"]},
                {"$set": {"used": summary.used, "allowed": summary.allowed}},
            )
        else:
            logger.warning(f"Subject {subject} has no usage records.")
        return summary

    async def _get_usage(self, subject: str) -> Tuple[Optional[dict], UsageSummary]:
        latest_record = None
        breakpoint = None
        used, allowed = 0, 0
        async for data in self.db.find(dict(subject=subject)).sort("created", -1):
            if not latest_record:
                latest_record = data
            if "used" in data:
                breakpoint = data
                break
            try:
                transaction = UsageDelta.model_validate(data)
            except ValueError as e:
                t = data.get("type")
                raise (
                    ValueError(f"Unexpected transaction type: {t}")
                    if t != "delta"
                    else e
                )
            used += transaction.used_delta
            allowed += transaction.allowed_delta

        if breakpoint:
            used += breakpoint["used"]
            allowed += breakpoint["allowed"]
        else:
            allowed += self.default_allowed
        if used > allowed:
            logger.info(
                f"Subject {subject} has exceeded their used quota: {used} of {allowed} allowed"
            )
        return latest_record, UsageSummary(subject=subject, used=used, allowed=allowed)
