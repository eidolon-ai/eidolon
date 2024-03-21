from __future__ import annotations

from abc import abstractmethod
from typing import List

from openai import BaseModel
from pydantic import PrivateAttr
from starlette.middleware.base import BaseHTTPMiddleware

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.system.reference_model import Reference


class DynamicMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        middleware = AgentOS.get_instance(Middleware)
        return await middleware.dispatch(request, call_next)


class Middleware:
    @abstractmethod
    async def dispatch(self, request, call_next):
        raise NotImplementedError()


class MultiMiddleware(Middleware, BaseModel):
    middlewares: List[Reference[Middleware]] = []
    _original_call_next: callable = PrivateAttr(default=None)

    async def dispatch(self, request, call_next):
        self._original_call_next = self._original_call_next or call_next
        if self.middlewares:
            latest = self.middlewares.pop()
            return await latest.dispatch(request, self.dispatch)
        else:
            return await self._original_call_next(request)
