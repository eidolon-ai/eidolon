import re

from starlette.requests import Request
from starlette.responses import JSONResponse

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.security.user import User
from eidolon_ai_sdk.system.dynamic_middleware import FlexibleManager
from usage_client.client import UsageClient


class UsageManager(FlexibleManager):
    action_pattern = re.compile(r"^/processes/([^/]+)/agent/([^/]+)/actions/([^/]+)$")
    request: Request

    def __init__(self, request: Request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    async def __aenter__(self):
        if self.request.method == "POST" and self.action_pattern.search(self.request.url.path):
            client: UsageClient = AgentOS.get_instance(UsageClient)
            subject = User.get_current().id
            summary = await client.get_summary(subject)
            return JSONResponse(status_code=429, content={
                "detail": "Usage limit exceeded",
                "used": summary.used,
                "allowed": summary.allowed
            }) if summary.used >= summary.allowed else None
