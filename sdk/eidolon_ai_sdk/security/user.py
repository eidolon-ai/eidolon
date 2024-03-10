from __future__ import annotations

from contextvars import ContextVar
from typing import Optional

from pydantic import BaseModel

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
