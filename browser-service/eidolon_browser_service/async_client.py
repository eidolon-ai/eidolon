from __future__ import annotations

import os
from typing import List
from urllib.parse import urljoin

import httpx
from httpx import Timeout
from pydantic import BaseModel

from eidolon_browser_service.api import PageInfo, PlaywrightActionResponse


class BrowserError(Exception):
    def __init__(self, message: str, status_code: int = None, response_body: str = None,
                 original_error: Exception = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body
        self.original_error = original_error


class PageNotFoundError(BrowserError):
    pass


async def _handle_response_error(e: httpx.HTTPStatusError, context: str) -> None:
    if e.response.status_code == 404:
        raise PageNotFoundError(
            f"{context}: resource not found",
            status_code=e.response.status_code,
            response_body=e.response.text,
            original_error=e
        )
    error_message = f"{context}: {str(e)}"
    try:
        error_message = e.response.json().get("detail")
    except Exception:
        pass
    raise BrowserError(
        error_message,
        status_code=e.response.status_code,
        response_body=e.response.text,
        original_error=e
    )


class Page(PageInfo):
    location: str
    context_id: str
    request_timout: int = 30
    connect_timout: int = 5

    async def actions(self, action: str, args: list = None, kwargs: dict = None) -> PlaywrightActionResponse:
        json = dict()
        if args:
            json["args"] = args
        if kwargs:
            json["kwargs"] = kwargs
        try:
            async with httpx.AsyncClient(timeout=Timeout(self.request_timout, connect=self.connect_timout)) as client:
                response = await client.post(
                    urljoin(self.location, f"/contexts/{self.context_id}/pages/{self.page_id}/actions/{action}"),
                    json=json
                )
                response.raise_for_status()
                return PlaywrightActionResponse.model_validate(response.json())
        except httpx.HTTPStatusError as e:
            await _handle_response_error(e, f"action \"{action}\" failed")

    async def get_content(self) -> str:
        try:
            async with httpx.AsyncClient(timeout=Timeout(self.request_timout, connect=self.connect_timout)) as client:
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
