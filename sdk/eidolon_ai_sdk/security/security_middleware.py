from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.security.security_manager import SecurityManagerImpl
from eidolon_ai_sdk.security.user import User


class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        security: SecurityManagerImpl = AgentOS.security_manager
        if request.url.path not in security.spec.safe_paths:
            try:
                user = await security.check_auth(request)
                User.set_current(user)
            except HTTPException as e:
                logger.info(f"Auth Denied: {e.detail}")
                return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        return await call_next(request)
