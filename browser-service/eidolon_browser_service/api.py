from typing import Optional

from pydantic import BaseModel


class PageInfo(BaseModel):
    page_id: str
    url: Optional[str]


class EvaluateRequest(BaseModel):
    script: str


class EvaluateInfo(BaseModel):
    result: Optional[str]


class NavigateRequest(BaseModel):
    url: str
