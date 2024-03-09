from __future__ import annotations

from abc import ABC, abstractmethod
from contextvars import ContextVar
from typing import Optional, Set, Literal

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
    extra: dict = {}

    @staticmethod
    def get_current() -> User:
        return _user_var.get()

    @staticmethod
    def set_current(user: User):
        return _user_var.set(user)


class PermissionException(Exception):
    missing: Set[Permission]
    process: Optional[str]

    def __init__(self, missing: Permission | Set[Permission], process: Optional[str] = None):
        self.missing = {missing} if isinstance(missing, str) else missing
        self.process = process
        reason = "Missing Resource Permission: " if process else "Missing Permission: "
        super().__init__(reason + ", ".join(self.missing))


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
        return User(id="NOOP_DEFAULT_USER", name="noop default user")


class ProcessAuthorizer(ABC):
    @abstractmethod
    async def check_process_perms(self, permissions: Set[Permission], agent: str, process_id: str):
        """
        Checks if the authenticated user has the specified permission(s) to the provided agent process.
        :raises PermissionException: If the agent does not have the required permissions.
        """
        pass

    @abstractmethod
    async def record_process(self, agent: str, resource_id: str):
        """
        Called when a process is created. Should propagate any state needed for future resource checks.
        """
        pass


class FunctionalAuthorizer:
    @abstractmethod
    async def check_functional_perms(self, permissions: Set[Permission], target):
        pass


class NoopFunctionalAuthorizer(FunctionalAuthorizer):
    async def check_functional_perms(self, *args, **kwargs):
        pass


class SecurityManagerSpec(BaseModel):
    authentication_processor: AnnotatedReference[AuthenticationProcessor]
    functional_authorizer: AnnotatedReference[FunctionalAuthorizer]
    process_authorizer: AnnotatedReference[ProcessAuthorizer]

    safe_paths: Set[str] = {"/system/health", "/docs", "/favicon.ico", "/openapi.json"}


class SecurityManager(Specable[SecurityManagerSpec]):
    authentication_processor: AuthenticationProcessor
    functional_authorizer: FunctionalAuthorizer
    process_authorizer: ProcessAuthorizer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.authentication_processor = self.spec.authentication_processor.instantiate()
        self.functional_authorizer = self.spec.functional_authorizer.instantiate()
        self.process_authorizer = self.spec.process_authorizer.instantiate()

    async def check_permissions(
        self, permissions: Permission | Set[Permission], agent: str, process_id: Optional[str] = None
    ):
        permissions = {permissions} if isinstance(permissions, str) else permissions
        await self.functional_authorizer.check_functional_perms(permissions, f"agents/{agent}/processes")
        if process_id:
            await self.process_authorizer.check_process_perms(permissions, agent, process_id)


def permission_exception_handler(request: Request, exc: PermissionException):
    logger.warning(str(exc))
    if "read" in exc.missing and exc.process:
        return JSONResponse(status_code=404, content={"detail": "Process Not Found"})
    return JSONResponse(status_code=403, content={"detail": str(exc)})
