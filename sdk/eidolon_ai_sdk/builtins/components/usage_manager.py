import re

from openai import BaseModel
from starlette.responses import JSONResponse

from eidolon_ai_sdk.security.user import User
from eidolon_ai_sdk.system.dynamic_middleware import Middleware
from eidolon_ai_sdk.system.reference_model import AnnotatedReference
from usage_client.client import UsageClient

action_pattern = re.compile(r"^/processes/([^/]+)/agent/([^/]+)/actions/([^/]+)$")


class UsageMiddleware(Middleware, BaseModel):
    path_regex: str = None
    usage_client: AnnotatedReference[UsageClient]

    async def dispatch(self, request, call_next):
        search_pattern = re.compile(self.path_regex) if self.path_regex else action_pattern
        if request.method == "POST" and search_pattern.search(request.url.path):
            client: UsageClient = self.usage_client.instantiate()
            subject = User.get_current().id
            summary = await client.get_summary(subject)
            if summary.used >= summary.allowed:
                return JSONResponse(status_code=429, content={
                    "detail": "Usage limit exceeded",
                    "used": summary.used,
                    "allowed": summary.allowed
                })
        return await call_next(request)
