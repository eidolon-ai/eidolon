from __future__ import annotations

import os
from typing import List
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel

from eidolon_browser_service.api import PageInfo, EvaluateInfo, NavigateRequest


class BrowserError(Exception):
    def __init__(self, message: str, status_code: int = None, response_body: str = None,
                 original_error: Exception = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body
        self.original_error = original_error


class PageNotFoundError(BrowserError):
    pass


class EvaluationError(BrowserError):
    pass


async def _handle_response_error(e: httpx.HTTPStatusError, context: str) -> None:
    if e.response.status_code == 404:
        raise PageNotFoundError(
            f"{context}: resource not found",
            status_code=e.response.status_code,
            response_body=e.response.text,
            original_error=e
        )
    raise BrowserError(
        f"{context}: {str(e)}",
        status_code=e.response.status_code,
        response_body=e.response.text,
        original_error=e
    )


class Page(PageInfo):
    location: str
    context_id: str

    async def evaluate(self, script: str) -> EvaluateInfo:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    urljoin(self.location, f"/contexts/{self.context_id}/pages/{self.page_id}/evaluate"),
                    json={"script": script}
                )
                response.raise_for_status()
                return EvaluateInfo.model_validate(response.json())
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 422:
                raise EvaluationError(
                    e.response.json().get('detail', e.response.text),
                    status_code=e.response.status_code,
                    response_body=e.response.text,
                    original_error=e
                )
            await _handle_response_error(e, "Evaluation failed")

    async def navigate(self, url: str) -> Page:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    urljoin(self.location, f"/contexts/{self.context_id}/pages/{self.page_id}/navigate"),
                    json=NavigateRequest(url=url).model_dump(),
                )
                response.raise_for_status()
                return Page(
                    location=self.location,
                    context_id=self.context_id,
                    page_id=self.page_id,
                    url=url,
                )
        except httpx.HTTPStatusError as e:
            await _handle_response_error(e, "Failed to navigate")

    async def get_content(self) -> str:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    urljoin(self.location, f"/contexts/{self.context_id}/pages/{self.page_id}/content")
                )
                response.raise_for_status()
                return response.text
        except httpx.HTTPStatusError as e:
            await _handle_response_error(e, "Failed to get content")


class Context(BaseModel):
    location: str
    context_id: str

    async def create_page(self) -> Page:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(urljoin(self.location, f"/contexts/{self.context_id}/pages"))
                response.raise_for_status()
                return Page(
                    location=self.location,
                    context_id=self.context_id,
                    **response.json()
                )
        except httpx.HTTPStatusError as e:
            await _handle_response_error(e, "Failed to create page")

    async def list_pages(self) -> List[Page]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    urljoin(self.location, f"/contexts/{self.context_id}/pages")
                )
                response.raise_for_status()
                return [
                    Page(
                        location=self.location,
                        context_id=self.context_id,
                        **PageInfo(**page).model_dump(),
                    )
                    for page in response.json()["pages"]
                ]
        except httpx.HTTPStatusError as e:
            await _handle_response_error(e, "Failed to list pages")

    async def delete(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    urljoin(self.location, f"/contexts/{self.context_id}")
                )
                response.raise_for_status()
        except httpx.HTTPStatusError as e:
            await _handle_response_error(e, "Failed to delete context")


class Browser(BaseModel):
    location: str = os.environ.get("BROWSER_SERVICE_URL", "http://localhost:7468")

    def context(self, context_id: str) -> Context:
        return Context(location=self.location, context_id=context_id)
