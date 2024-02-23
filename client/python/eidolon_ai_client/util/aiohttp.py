from typing import Any, Dict, Optional

import json

from httpx import Timeout, AsyncClient, HTTPStatusError, codes
from httpx_sse import EventSource
from pydantic_core import to_jsonable_python

from eidolon_ai_client.events import BaseStreamEvent
from eidolon_ai_client.util.logger import logger
from eidolon_ai_client.util.request_context import RequestContext


# noinspection PyShadowingNames
async def get_content(url: str, json: Optional[Dict[str, Any]] = None, **kwargs):
    async with AsyncClient(timeout=Timeout(5.0, read=600.0)) as client:
        params = {"url": url, "headers": RequestContext.headers}
        if json:
            params["json"] = json
        response = await client.get(**params, **kwargs)
        await AgentError.check(response)
        return response.json()


# noinspection PyShadowingNames
async def post_content(url, json: Optional[Any] = None, **kwargs):
    params = {"url": url, "headers": RequestContext.headers}
    if json:
        params["json"] = to_jsonable_python(json)
    async with AsyncClient(timeout=Timeout(5.0, read=600.0)) as client:
        response = await client.post(**params, **kwargs)
        await AgentError.check(response)
        return response.json()


# noinspection PyShadowingNames
async def delete(url, **kwargs):
    params = {"url": url, "headers": RequestContext.headers}
    async with AsyncClient(timeout=Timeout(5.0, read=600.0)) as client:
        response = await client.delete(**params, **kwargs)
        await AgentError.check(response)
        return response.json()


async def stream_content(url: str, body, **kwargs):
    body = to_jsonable_python(body)
    headers = {
        **RequestContext.headers,
        "Accept": "text/event-stream",
    }
    request = {"url": url, "json": body, "method": "POST", "headers": headers, **kwargs}
    async with AsyncClient(timeout=Timeout(5.0, read=600.0)) as client:
        async with client.stream(**request) as response:
            await AgentError.check(response)
            async for sse_event in EventSource(response).aiter_sse():
                if sse_event.data:
                    data = json.loads(sse_event.data)
                    event = BaseStreamEvent.from_dict(data)
                    yield event
                else:
                    logger.warning("Empty event from server")


class AgentError(Exception):
    message: str
    status_code: int
    response: Any

    def __init__(self, status_code: int, message: str, response=None):
        super().__init__(f"{status_code} ({codes.get_reason_phrase(status_code)}): {message}")
        self.message = message
        self.status_code = status_code
        self.response = response

    @classmethod
    async def check(cls, response, message_override=None):
        try:
            response.raise_for_status()
        except HTTPStatusError as e:
            message = message_override or "".join([b async for b in e.response.aiter_text()])
            raise cls(e.response.status_code, message, response)
