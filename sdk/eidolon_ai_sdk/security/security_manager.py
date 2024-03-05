from typing import Optional, Set, Literal

from abc import ABC, abstractmethod
from fastapi import Request, Response, FastAPI
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference

Permission = Literal["create", "read", "update", "delete"]  # probably exapnds to include concept of know

class PermissionException(Exception):
    missing: Set[Permission]
    def __init__(self, missing: Permission | Set[Permission]):
        self.missing = [missing] if isinstance(missing, str) else missing
        super().__init__(f"Missing permissions: {', '.join(self.missing)}")


class AuthorizationProcessor(ABC):
    @abstractmethod
    async def check_auth(self, request: Request):
        """
        Check the request for expected authentication and stores information in context as needed for authorization.
        :raises HTTPException: if the request is not authenticated
        """
        pass

    @abstractmethod
    async def check_permission(self, permissions: Permission | Set[Permission], agent: str, process: Optional[str] = None):
        """
        Checks if the authenticated user has the specified permission(s) to the provided agent process.

        Checks functional permissions only if processes is omitted.
        Checks functional AND resource permissions when process is included.

        :raises PermissionException: If the agent does not have the required permissions.
        """
        pass

    @abstractmethod
    async def record_resource(self, agent: str, process: Optional[str] = None):
        """
        Called when a process is created. Should propagate any state needed for future resource checks.
        """
        pass


class NoopAuthProcessor(AuthorizationProcessor):
    async def check_auth(self, request: Request):
        pass

    async def check_permission(self, permissions: Permission | Set[Permission], agent: str,
                               process: Optional[str] = None):
        pass

    @abstractmethod
    async def record_resource(self, agent: str, process: Optional[str] = None):
        pass


class SecurityManagerSpec(BaseModel):
    authorization_processor: AnnotatedReference[AuthorizationProcessor]
    safe_paths: Set[str] = {"/system/health", "/docs", "/favicon.ico", "/openapi.json"}


class SecurityManager(Specable[SecurityManagerSpec]):
    authorization_processor: AuthorizationProcessor

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.authorization_processor = self.spec.authorization_processor.instantiate()
