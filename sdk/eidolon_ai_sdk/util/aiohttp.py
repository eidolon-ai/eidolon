from typing import Any, Dict, Optional

import json

from httpx import Timeout, AsyncClient
from httpx_sse import EventSource
from pydantic_core import to_jsonable_python

from eidolon_ai_sdk.io.events import BaseStreamEvent
from eidolon_ai_sdk.system.request_context import RequestContext


# noinspection PyShadowingNames
async def get_content(url: str, json: Optional[Dict[str, Any]] = None, **kwargs):
    async with AsyncClient(timeout=Timeout(5.0, read=600.0)) as client:
        params = {"url": url, "headers": RequestContext.headers}
        if json:
            params["json"] = json
        response = await client.get(**params, **kwargs)
        response.raise_for_status()
        return response.json()


# noinspection PyShadowingNames
async def post_content(url, json: Optional[Any] = None, **kwargs):
    params = {"url": url, "headers": RequestContext.headers}
    if json:
        params["json"] = to_jsonable_python(json)
    async with AsyncClient(timeout=Timeout(5.0, read=600.0)) as client:
        response = await client.post(**params, **kwargs)
        response.raise_for_status()
        return response.json()


async def stream_content(url: str, body):
    body = to_jsonable_python(body)
    headers = {
        **RequestContext.headers,
        "Accept": "text/event-stream, application/json",
    }
    request = {"url": url, "json": body, "method": "POST", "headers": headers}
    async with AsyncClient(timeout=Timeout(5.0, read=600.0)) as client:
        async with client.stream(**request) as response:
            async for sse_event in EventSource(response).aiter_sse():
                data = json.loads(sse_event.data)
                event = BaseStreamEvent.from_dict(data)
                yield event
