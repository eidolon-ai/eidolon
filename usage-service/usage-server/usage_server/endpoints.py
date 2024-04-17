from fastapi import APIRouter

from eidolon_ai_usage_client.models import UsageSummary, UsageDelta, UsageReset
from usage_server.usage import UsageService

usage = APIRouter()


@usage.get(path="/health")
async def health():
    return {"status": "ok"}


@usage.delete(path="/subjects/{subject_id}")
async def delete_subject(subject_id: str) -> dict:
    s = await UsageService.singleton()
    deleted = await s.delete(subject_id)
    return {"deleted": True, "transactions": deleted}


@usage.get(path="/subjects/{subject_id}")
async def get_usage_summary(subject_id: str) -> UsageSummary:
    s = await UsageService.singleton()
    return await s.get_usage(subject_id)


Transaction = UsageDelta | UsageReset


@usage.post(path="/subjects/{subject_id}/transactions")
async def record_usage_transaction(
    subject_id: str, transaction: Transaction
) -> UsageSummary:
    s = await UsageService.singleton()
    return await s.record_transaction(subject_id, transaction)
