from fastapi import HTTPException
from starlette.requests import Request

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.security.user import User
from eidolon_ai_sdk.system.dynamic_middleware import FlexibleManager
from usage_client.client import UsageClient


class UsageManager(FlexibleManager):
    request: Request

    def __init__(self, request: Request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    async def __aenter__(self):
        if self.request.method == "POST":  # todo, check for action in path as well
            client: UsageClient = AgentOS.get_instance(UsageClient)
            subject = User.get_current().id
            summary = await client.get_summary(subject)
            if summary.used >= summary.allowed:
                raise HTTPException(status_code=429, detail="Usage limit exceeded")
