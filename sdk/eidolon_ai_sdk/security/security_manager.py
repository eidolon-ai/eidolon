from typing import Optional

from abc import ABC, abstractmethod
from fastapi import Request, Response, FastAPI
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference


class BaseTokenProcessor(ABC):
    @abstractmethod
    async def dispatch(self, request: Request) -> Optional[Response]:
        pass


class NoopAuthProcessor(BaseTokenProcessor):
    def add_login_route(self, app: FastAPI):
        pass

    async def dispatch(self, request: Request):
        return None


class SecurityManagerSpec(BaseModel):
    authorization_processor: AnnotatedReference[BaseTokenProcessor, NoopAuthProcessor]


class SecurityManager(Specable[SecurityManagerSpec]):
    authorization_processor: BaseHTTPMiddleware

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.authorization_processor = self.spec.authorization_processor.instantiate()
