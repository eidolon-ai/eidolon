from __future__ import annotations

import copy
from contextvars import ContextVar
from typing import Any, Dict
from urllib.request import Request

from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

from eidolon_ai_client.util.logger import logger

_request_context = ContextVar("request_context")


class _Record(BaseModel):
    key: str
    value: Any
    propagate: bool


def _get_context() -> Dict[str, _Record]:
    try:
        return _request_context.get()
    except LookupError:
        _request_context.set(dict())
        return _request_context.get()


class _RequestContextMeta(type):
    def __contains__(self, item):
        return item in _get_context()

    def __setitem__(self, key, value):
        return self.set(key, value, propagate=False)

    def __getitem__(self, key):
        return _get_context()[key].value

    def __repr__(self):
        return repr(_get_context())

    @staticmethod
    def set(key: str, value: str | Any, propagate=False):
        logger.debug(f"setting context {key}={value}, propagate={propagate}")
        if propagate and not isinstance(value, str):
            raise ValueError("can only propagate string values")
        if "," in key:
            raise ValueError("key cannot contain commas")
        _get_context()[key] = _Record(key=key, value=value, propagate=propagate)

    def get(self, key, default=...):
        context = _get_context()
        if default is ... and key not in context:
            raise KeyError(key)
        return copy.deepcopy(self[key]) if key in context else default

    @property
    def headers(self):
        to_propagate = {v.key: v.value for v in _get_context().values() if v.propagate}
        if to_propagate:
            to_propagate["X-Eidolon-Context"] = ",".join(f"{k}" for k in to_propagate.keys())
        return to_propagate


class RequestContext(metaclass=_RequestContextMeta):
    pass


class ContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        context_headers = request.headers.get("X-Eidolon-Context", "") or []
        if context_headers:
            context_headers = context_headers.split(",")
        for header in context_headers:
            try:
                RequestContext.set(header, request.headers[header], propagate=True)
            except KeyError:
                logger.warning(f"Expected context header {header} not found")

        return await call_next(request)
