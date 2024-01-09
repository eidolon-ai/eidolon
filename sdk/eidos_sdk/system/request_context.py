from __future__ import annotations

from contextvars import ContextVar
from typing import Any, Dict

from pydantic import BaseModel

_request_context = ContextVar('request_context')


class _Record(BaseModel):
    key: str
    value: str
    propagate: bool


def _get_context() -> Dict[str, _Record]:
    try:
        return _request_context.get()
    except LookupError:
        _request_context.set(dict())
        return _request_context.get()


class _RequestContextMeta(type):
    def __getitem__(self, key):
        return _get_context()[key].value

    def __repr__(self):
        return repr(_get_context())

    def __delitem__(self, key):
        del _get_context()[key]

    @staticmethod
    def set(key: str, value: str | Any, propagate=False):
        if propagate and not isinstance(value, str):
            raise ValueError('can only propagate string values')
        _get_context()[key] = _Record(key=key, value=value, propagate=propagate)

    def get(self, key, default=None):
        return self[key] if key in _get_context() else default

    @property
    def headers(self):
        return {v.key: v.value for v in _get_context().values() if v.propagate}


class RequestContext(metaclass=_RequestContextMeta):
    pass
