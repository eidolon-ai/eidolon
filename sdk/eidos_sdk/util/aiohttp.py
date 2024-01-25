import json

from httpx import Timeout, AsyncClient
from httpx_sse import EventSource
from pydantic_core import to_jsonable_python

from eidos_sdk.io.events import BaseStreamEvent
from eidos_sdk.system.request_context import RequestContext


async def get_content(url):
    async with AsyncClient(timeout=Timeout(5.0, read=600.0)) as client:
        response = await client.get(url=url, headers=RequestContext.headers)
        response.raise_for_status()
        return response.json()


async def post_content(url, body):
    headers = {
        **RequestContext.headers,
        "Accept": "text/event-stream, application/json",
    }
    async with AsyncClient(timeout=Timeout(5.0, read=600.0)) as client:
        response = await client.post(url=url, json=to_jsonable_python(body), headers=headers)
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
