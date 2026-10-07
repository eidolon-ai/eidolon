"""Opt-in, anonymous Parallel Search MCP tools over Streamable HTTP."""

import asyncio
import copy
import json
from contextlib import asynccontextmanager
from uuid import NAMESPACE_URL, uuid5

import httpx
from httpx import AsyncClient
from httpx_sse import EventSource
from pydantic import Field

from eidolon_ai_sdk.apu.call_context import CallContext
from eidolon_ai_sdk.system.fn_handler import FnHandler
from eidolon_ai_sdk.system.tool_builder import ToolBuilder
from eidolon_ai_sdk.util.partial import return_value

_ENDPOINT = "https://search.parallel.ai/mcp"
_USER_AGENT = "eidolon-ai-sdk/0.1.184 (ParallelSearch)"
_PROTOCOL = "2025-03-26"


class ParallelSearch(ToolBuilder):
    """Discover search and fetch tools without reading or sending API credentials."""

    timeout: float = Field(default=60, gt=0, description="Maximum seconds for discovery or a tool call.")

    async def build_tools(self, call_context: CallContext):
        tools = await asyncio.wait_for(self._discover(), timeout=self.timeout)
        session_id = str(uuid5(NAMESPACE_URL, json.dumps([call_context.process_id, call_context.thread_id])))
        handlers = []
        for tool in tools:
            if tool["name"] not in ("web_search", "web_fetch"):
                continue
            schema = copy.deepcopy(tool["inputSchema"])
            for key in ("session_id", "model_name"):
                schema.get("properties", {}).pop(key, None)
                if key in schema.get("required", []):
                    schema["required"].remove(key)

            handlers.append(self._handler(tool, schema, session_id))
        return handlers

    def _handler(self, tool, schema, session_id):
        async def execute(_self, **arguments):
            # Runtime context owns free-tier accounting, rather than model-generated metadata.
            arguments.pop("model_name", None)
            arguments["session_id"] = session_id
            result = await asyncio.wait_for(self._call(tool["name"], arguments), timeout=self.timeout)
            if result.get("isError"):
                raise RuntimeError(f"Parallel Search MCP tool error: {result.get('content')}")
            return result

        return FnHandler(
            name=tool["name"],
            description=return_value(tool.get("description", tool["name"])),
            input_model_fn=return_value(schema),
            output_model_fn=return_value(dict),
            fn=execute,
            extra=dict(title="Parallel Search", sub_title=tool["name"]),
        )

    async def _discover(self):
        async with self._connection() as client:
            tools = []
            params = {}
            while True:
                result = await _rpc(client, "tools/list", params)
                tools.extend(result["tools"])
                cursor = result.get("nextCursor")
                if not cursor:
                    return tools
                params = {"cursor": cursor}

    async def _call(self, name, arguments):
        async with self._connection() as client:
            return await _rpc(client, "tools/call", dict(name=name, arguments=arguments))

    @asynccontextmanager
    async def _connection(self):
        # A short-lived MCP session per operation avoids shared mutable session state across threads.
        async with AsyncClient(
            timeout=self.timeout,
            headers={"User-Agent": _USER_AGENT, "Accept": "application/json, text/event-stream"},
        ) as client:
            result = await _rpc(
                client,
                "initialize",
                dict(
                    protocolVersion=_PROTOCOL, capabilities={}, clientInfo=dict(name="eidolon-ai-sdk", version="0.1.184")
                ),
            )
            if result["protocolVersion"] != _PROTOCOL:
                raise RuntimeError("Parallel Search MCP negotiated an unsupported protocol version")
            client.headers["MCP-Protocol-Version"] = _PROTOCOL
            cancelled = False
            try:
                response = await client.post(_ENDPOINT, json=dict(jsonrpc="2.0", method="notifications/initialized"))
                response.raise_for_status()
                yield client
            except asyncio.CancelledError:
                cancelled = True
                raise
            finally:
                if not cancelled and "Mcp-Session-Id" in client.headers:
                    # Cleanup must not mask tool errors or cancellation. Sessions may also expire server-side.
                    try:
                        await client.delete(_ENDPOINT, timeout=min(self.timeout, 5))
                    except httpx.HTTPError:
                        pass


async def _rpc(client, method, params):
    request_id = str(uuid5(NAMESPACE_URL, method))
    async with client.stream(
        "POST", _ENDPOINT, json=dict(jsonrpc="2.0", id=request_id, method=method, params=params)
    ) as response:
        response.raise_for_status()
        if method == "initialize" and response.headers.get("Mcp-Session-Id"):
            client.headers["Mcp-Session-Id"] = response.headers["Mcp-Session-Id"]
        content_type = response.headers.get("content-type", "").split(";", 1)[0]
        if content_type == "text/event-stream":
            async for event in EventSource(response).aiter_sse():
                if not event.data:
                    continue
                message = json.loads(event.data)
                if message.get("id") == request_id:
                    return _result(message)
            raise RuntimeError("Parallel Search MCP stream ended without a response")
        if content_type != "application/json":
            raise RuntimeError(f"Unexpected Parallel Search MCP content type: {content_type}")
        message = json.loads(await response.aread())
        if message.get("id") != request_id:
            raise RuntimeError("Parallel Search MCP response ID mismatch")
        return _result(message)


def _result(message):
    if "error" in message:
        raise RuntimeError(f"Parallel Search MCP protocol error: {message['error']}")
    return message["result"]
