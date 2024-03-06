from abc import ABC, abstractmethod
from typing import Optional, Set, Literal

from fastapi import Request
from pydantic import BaseModel

from eidolon_ai_client.util.request_context import User
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference

Permission = Literal["create", "read", "update", "delete"]  # probably expands to include concept of know


class PermissionException(Exception):
    process: Optional[str]
    missing: Set[Permission]

    def __init__(self, missing: Permission | Set[Permission], process: Optional[str] = None):
        self.missing = [missing] if isinstance(missing, str) else missing
        self.process = process
        reason = f"Missing permission(s) {', '.join(self.missing)}" + (f" for process {process}" if process else "")
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
            functional_permissions={"eidolon/agents/*/processes": {"create", "read", "update", "delete"}}
        )

class AuthorizationProcessor(ABC):
    @abstractmethod
    async def check_permission(self, permissions: Permission | Set[Permission], agent: str, process_id: Optional[str] = None):
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
