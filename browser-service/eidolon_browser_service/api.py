from typing import Optional, Any

from pydantic import BaseModel, HttpUrl


class PageInfo(BaseModel):
    page_id: str
    url: Optional[str]


class PlaywrightActionRequest(BaseModel):
    args: list = []
    kwargs: dict = {}


class PlaywrightActionResponse(BaseModel):
    result: Optional[Any]
