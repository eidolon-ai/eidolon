import asyncio
from fastapi import APIRouter

from usage_client.models import UsageSummary, UsageDelta
from usage_server.logger_ import logger
from usage_server.usage import UsageService, UsageReset

service: UsageService = UsageService()

usage = APIRouter()


@usage.delete(path="/subjects/{subject_id}")
async def delete_subject(subject_id: str) -> dict:
    deleted = await service.delete(subject_id)
    return {"deleted": True, "transactions": deleted}


@usage.get(path="/subjects/{subject_id}")
async def get_usage_summary(subject_id: str) -> UsageSummary:
    return await service.get_usage(subject_id)


@usage.post(path="/subjects/{subject_id}/transactions")
async def record_usage_transaction(
    subject_id: str, transaction: UsageDelta | UsageReset
) -> None:
    await service.record_transaction(subject_id, transaction)
    asyncio.create_task(
        _with_error_logging(service.create_breakpoint_record(subject_id))
    )


async def _with_error_logging(
    coro, error_message: str = "Error while executing background task"
):
    try:
        return await coro
    except Exception:
        logger.exception(error_message)
        raise
