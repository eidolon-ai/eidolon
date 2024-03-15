from __future__ import annotations

from typing import Set, Optional, Literal

from starlette.requests import Request
from starlette.responses import JSONResponse

from eidolon_ai_client.util.logger import logger


class PermissionException(Exception):
    missing: Set[Permission]
    process: Optional[str]

    def __init__(self, missing: Permission | Set[Permission], process: Optional[str] = None):
        self.missing = {missing} if isinstance(missing, str) else missing
        self.process = process
        reason = "Missing Resource Permission: " if process else "Missing Permission: "
        super().__init__(reason + ", ".join(self.missing))


Permission = Literal["create", "read", "update", "delete"]  # probably expands to include concept of know


def permission_exception_handler(request: Request, exc: PermissionException):
    logger.warning(str(exc))
    if "read" in exc.missing and exc.process:
        return JSONResponse(status_code=404, content={"detail": "Process Not Found"})
    return JSONResponse(status_code=403, content={"detail": str(exc)})
