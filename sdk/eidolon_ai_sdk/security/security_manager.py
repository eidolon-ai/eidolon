from __future__ import annotations

import fnmatch
from abc import ABC, abstractmethod
from contextvars import ContextVar
from typing import Optional, Set, Literal, List

from fastapi import Request
from pydantic import BaseModel
from starlette.responses import JSONResponse

from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference

Permission = Literal["create", "read", "update", "delete"]  # probably expands to include concept of know


_user_var = ContextVar("current_user")


class User(BaseModel):
    id: str
    name: Optional[str] = None
    functional_permissions: List[str] = []

    def check_functional_permissions(self, permissions: Permission | Set[Permission], agent):
        permissions = {permissions} if isinstance(permissions, str) else permissions
        missing = permissions.copy()
        for permission in permissions:
            for pattern in self.functional_permissions:
                if fnmatch.fnmatch(f"eidolon/agents/{agent}/processes/{permission}", pattern):
                    missing.remove(permission)
                    break
        if missing:
            raise PermissionException(missing)

    def agent_process_permissions(self, agent: str) -> set[str]:
        permissions = set()
        for pattern in self.functional_permissions.keys():
            if fnmatch.fnmatch(f"eidolon/agents/{agent}/processes", pattern):
                permissions = permissions.union(self.functional_permissions[pattern])
        return permissions

    @staticmethod
    def get_current() -> User:
        return _user_var.get()

    @staticmethod
    def set_current(user: User):
        return _user_var.set(user)


class PermissionException(Exception):
    process: Optional[str]
    missing: Set[Permission]

    def __init__(self, missing: Permission | Set[Permission], process: Optional[str] = None):
        self.missing = [missing] if isinstance(missing, str) else missing
        self.process = process
        if process:
            reason = f"Missing Resource Permission: {', '.join(self.missing)}"
        else:
            reason = f"Missing Permission: {', '.join(self.missing)}"
        super().__init__(reason)


class AuthenticationProcessor(ABC):
    @abstractmethod
    async def check_auth(self, request: Request) -> User:
        """
        Check the request for expected authentication and stores information in context as needed for authorization.

        :return User: the authenticated user
        :raises HTTPException: if the request is not authenticated
        """
        pass


class NoopAuthProcessor(AuthenticationProcessor):
    async def check_auth(self, request: Request) -> User:
        return User(
            id="NOOP_DEFAULT_USER",
            name="noop default user",
            functional_permissions=["eidolon/agents/*/processes/*"],
        )


class AuthorizationProcessor(ABC):
    @abstractmethod
    async def check_permissions(
        self, permissions: Permission | Set[Permission], agent: str, process_id: Optional[str] = None
    ):
        """
        Checks if the authenticated user has the specified permission(s) to the provided agent process.

        Checks functional permissions only if processes is omitted.
        Checks functional AND resource permissions when process is included.

        :raises PermissionException: If the agent does not have the required permissions.
        """
        pass

    @abstractmethod
    async def record_resource(self, agent: str, process: str):
        """
        Called when a process is created. Should propagate any state needed for future resource checks.
        """
        pass


class SecurityManagerSpec(BaseModel):
    authentication_processor: AnnotatedReference[AuthenticationProcessor]
    authorization_processor: AnnotatedReference[AuthorizationProcessor]

    safe_paths: Set[str] = {"/system/health", "/docs", "/favicon.ico", "/openapi.json"}


class SecurityManager(Specable[SecurityManagerSpec]):
    authentication_processor: AuthenticationProcessor
    authorization_processor: AuthorizationProcessor

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.authentication_processor = self.spec.authentication_processor.instantiate()
        self.authorization_processor = self.spec.authorization_processor.instantiate()


def permission_exception_handler(request: Request, exc: PermissionException):
    user = User.get_current()
    logger.warning(f"Missing Permissions (user '{user.name}' | id '{user.id}'): {exc}")
    if "read" in exc.missing:
        if exc.process:
            return JSONResponse(status_code=404, content={"detail": "Process Not Found"})
        else:
            return JSONResponse(status_code=404, content={"detail": "Not Found"})
    return JSONResponse(status_code=403, content={"detail": str(exc)})
