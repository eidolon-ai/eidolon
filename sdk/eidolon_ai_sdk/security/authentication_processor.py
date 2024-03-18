from __future__ import annotations

from abc import ABC, abstractmethod

from starlette.requests import Request

from eidolon_ai_sdk.security.user import User


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
        return User(id="NOOP_DEFAULT_USER", name="noop default user", extra={"permissions": ["agents/*/processes/*"]})
