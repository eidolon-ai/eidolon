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

class BaseTokenProcessor(ABC):
    @abstractmethod
    async def check_auth(self, request: Request):
        pass

    @abstractmethod
    async def check_permission(self, agent: str, permissions: Permission | Set[Permission], process: Optional[str] = None):
        pass

    @abstractmethod
    async def record_resource(self, agent: str, process: Optional[str] = None):
        pass


class NoopAuthProcessor(BaseTokenProcessor):
    async def check_auth(self, request: Request):
        pass

    async def check_permission(self, agent: str, permissions: Permission | Set[Permission], process: Optional[str] = None):
        pass

    @abstractmethod
    async def record_resource(self, agent: str, process: Optional[str] = None):
        pass


class SecurityManagerSpec(BaseModel):
    authorization_processor: AnnotatedReference[BaseTokenProcessor]
    safe_paths: Set[str] = {"/system/health", "/docs", "/favicon.ico", "/openapi.json"}


class SecurityManager(Specable[SecurityManagerSpec]):
    authorization_processor: BaseTokenProcessor

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.authorization_processor = self.spec.authorization_processor.instantiate()
