import os
from typing import Literal

from pydantic import BaseModel


class UsageDelta(BaseModel):
    type: Literal["delta"] = "delta"
    used_delta: int = 0
    allowed_delta: int = 0
    extra: dict = {}


class UsageReset(BaseModel):
    type: Literal["reset"] = "reset"
    used: int = 0
    allowed: int = int(os.environ.get("DEFAULT_ALLOWED", 600))
    extra: dict = {}


class UsageSummary(BaseModel):
    subject: str
    used: int
    allowed: int
