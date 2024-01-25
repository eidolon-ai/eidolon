import httpx
import json
from aiohttp import ClientSession
from httpx_sse import EventSource

from eidos_sdk.io.events import BaseStreamEvent
from eidos_sdk.system.request_context import RequestContext


class ContextualClientSession(ClientSession):
    def __init__(self, *args, **kwargs):
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"].update(RequestContext.headers)
        super().__init__(*args, **kwargs)


async def stream_content(url: str, body):
    headers = {
        **RequestContext.headers,
        "Accept": "text/event-stream, application/json",
    }
    request = {"url": url, "json": body, "method": "POST", "headers": headers}
    async with httpx.AsyncClient(timeout=httpx.Timeout(5.0, read=600.0)) as client:
        async with client.stream(**request) as response:
            async for sse_event in EventSource(response).aiter_sse():
                data = json.loads(sse_event.data)
                event = BaseStreamEvent.from_dict(data)
                yield event
