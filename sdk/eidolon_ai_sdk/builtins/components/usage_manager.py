import re

from openai import BaseModel
from starlette.responses import JSONResponse

from eidolon_ai_sdk.security.user import User
from eidolon_ai_sdk.system.dynamic_middleware import Middleware
from eidolon_ai_sdk.system.reference_model import AnnotatedReference
from usage_client.client import UsageClient, UsageLimitExceeded

action_pattern = re.compile(r"^/processes/([^/]+)/agent/([^/]+)/actions/([^/]+)$")


class UsageMiddleware(Middleware, BaseModel):
    path_regex: str = None
    usage_client: AnnotatedReference[UsageClient]

    async def dispatch(self, request, call_next):
        search_pattern = re.compile(self.path_regex) if self.path_regex else action_pattern
        if request.method == "POST" and search_pattern.search(request.url.path):
            client: UsageClient = self.usage_client.instantiate()
            subject = User.get_current().id
            try:
                await client.get_summary(subject)
            except UsageLimitExceeded as e:
                return JSONResponse(status_code=429, content={
                    "detail": "Usage limit exceeded",
                    "used": e.summary.used,
                    "allowed": e.summary.allowed
                })
            except Exception as e:
                return JSONResponse(status_code=502, content={
                    "detail": "Error checking usage",
                    "error": str(e)
                })
        return await call_next(request)
