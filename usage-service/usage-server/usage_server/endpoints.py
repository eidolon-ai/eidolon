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


in_progress_breakpoints = set()


@usage.post(path="/subjects/{subject_id}/transactions")
async def record_usage_transaction(
    subject_id: str, transaction: UsageDelta | UsageReset
) -> None:
    await service.record_transaction(subject_id, transaction)
    if not subject_id not in in_progress_breakpoints:
        in_progress_breakpoints.add(subject_id)
        asyncio.create_task(_add_breakpoint(subject_id))


async def _add_breakpoint(subject_id):
    try:
        await service.create_breakpoint_record(subject_id)
        logger.info(f"Added breakpoint for subject {subject_id}")
    except Exception:
        logger.exception(f"Error while adding breakpoint for subject {subject_id}")
        raise
    finally:
        in_progress_breakpoints.remove(subject_id)
