import os

from httpx import AsyncClient

from eidolon_ai_usage_client.models import UsageSummary, UsageReset, UsageDelta


class UsageClient:
    kwargs: dict

    def __init__(self, location: str = os.environ.get('EIDOLON_USAGE_SERVER', "http://localhost:8527"), **kwargs):
        self.kwargs = dict(base_url=location, **kwargs)

    @property
    def client(self) -> AsyncClient:
        return AsyncClient(**self.kwargs)

    async def get_summary(self, subject: str) -> UsageSummary:
        async with self.client as client:
            response = await client.get(f"/subjects/{subject}")
            response.raise_for_status()
            summary = UsageSummary(**response.json())
            if summary.used >= summary.allowed:
                raise UsageLimitExceeded(summary)
            return summary

    async def record_transaction(
        self, subject: str, transaction: UsageDelta | UsageReset
    ):
        transaction_dict = transaction.model_dump(exclude_defaults=True)
        transaction_dict["type"] = transaction.type
        async with self.client as client:
            response = await client.post(
                f"/subjects/{subject}/transactions", json=transaction_dict
            )
            response.raise_for_status()

    async def delete(self, subject: str) -> dict:
        async with self.client as client:
            response = await client.delete(f"/subjects/{subject}")
            response.raise_for_status()
            return response.json()


class UsageLimitExceeded(Exception):
    summary: UsageSummary

    def __init__(self, summary: UsageSummary):
        self.summary = summary
        super().__init__(f"Usage limit exceeded: {summary.used}/{summary.allowed}")
