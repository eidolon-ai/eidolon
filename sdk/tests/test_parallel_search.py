import asyncio
import json

import httpx
import pytest
from jsonschema import ValidationError

from eidolon_ai_client.events import ToolCall
from eidolon_ai_sdk.apu.call_context import CallContext
from eidolon_ai_sdk.apu.logic_unit import LLMToolWrapper, LogicUnit
from eidolon_ai_sdk.builtins.logic_units import parallel_search
from eidolon_ai_sdk.system.reference_model import Reference

FQN = "eidolon_ai_sdk.builtins.logic_units.parallel_search.ParallelSearch"


def install_server(monkeypatch, *, sse=False, error=None, delay=False):
    requests = []
    request_ids = set()
    original = httpx.AsyncClient

    async def handle(request):
        requests.append(request)
        assert str(request.url) == "https://search.parallel.ai/mcp"
        assert request.headers["User-Agent"] == "eidolon-ai-sdk/0.1.184 (ParallelSearch)"
        assert "authorization" not in request.headers
        if request.method == "DELETE":
            return httpx.Response(204)
        message = json.loads(request.content)
        method = message["method"]
        if "id" in message:
            assert message["id"] not in request_ids
            request_ids.add(message["id"])
        if method == "initialize":
            return httpx.Response(
                200,
                headers={"Mcp-Session-Id": "test-session"},
                json={"jsonrpc": "2.0", "id": message["id"], "result": {"protocolVersion": "2025-03-26"}},
            )
        assert request.headers["Mcp-Session-Id"] == "test-session"
        assert request.headers["MCP-Protocol-Version"] == "2025-03-26"
        if method == "notifications/initialized":
            return httpx.Response(202)
        if method == "tools/list":
            if delay:
                await asyncio.sleep(10)
            name = "web_fetch" if message["params"].get("cursor") else "web_search"
            field = "urls" if name == "web_fetch" else "objective"
            result = {
                "tools": [
                    {
                        "name": name,
                        "description": name,
                        "inputSchema": {
                            "type": "object",
                            "properties": {field: {"type": "string"}, "session_id": {"type": "string"}},
                            "required": [field],
                        },
                    }
                ]
            }
            if name == "web_search":
                result["nextCursor"] = "page-two"
        else:
            args = message["params"]["arguments"]
            assert "session_id" in args and "model_name" not in args
            result = {"content": [{"type": "text", "text": message["params"]["name"]}], "isError": error == "tool"}
        body = {"jsonrpc": "2.0", "id": message["id"], "result": result}
        if error == "rpc" and method == "tools/call":
            body = {"jsonrpc": "2.0", "id": message["id"], "error": {"code": -32602, "message": "bad args"}}
        if sse:
            return httpx.Response(
                200,
                headers={"Content-Type": "text/event-stream"},
                content=(
                    'data: {"jsonrpc":"2.0","method":"notifications/progress"}\n\n'
                    + "data: "
                    + json.dumps(body)
                    + "\n\n"
                ),
            )
        return httpx.Response(200, json=body)

    def client(**kwargs):
        return original(transport=httpx.MockTransport(handle), **kwargs)

    monkeypatch.setattr(parallel_search, "AsyncClient", client)
    return requests


@pytest.mark.parametrize("sse", [False, True])
async def test_reference_dispatch_and_sessions(monkeypatch, sse):
    requests = install_server(monkeypatch, sse=sse)
    unit = Reference[LogicUnit](implementation=FQN).instantiate()
    context = CallContext(process_id="p1", thread_id="t1")
    tools = await LLMToolWrapper.from_logic_units(context, [unit])
    assert set(tools) == {"ParallelSearch_web_search", "ParallelSearch_web_fetch"}
    assert "session_id" not in tools["ParallelSearch_web_search"].llm_message.parameters["properties"]
    for name, args in [("web_search", {"objective": "Python"}), ("web_fetch", {"urls": "https://python.org"})]:
        wrapper = tools["ParallelSearch_" + name]
        events = [e async for e in wrapper.execute(ToolCall(tool_call_id=name, name=name, arguments=args))]
        assert events[0].content["content"][0]["text"] == name
    calls = [json.loads(r.content) for r in requests if r.method == "POST"]
    arguments = [c["params"]["arguments"] for c in calls if c["method"] == "tools/call"]
    assert arguments[0]["session_id"] == arguments[1]["session_id"]
    assert len([r for r in requests if r.method == "DELETE"]) == 3
    with pytest.raises(ValidationError):
        await anext(tools["ParallelSearch_web_search"].execute(ToolCall(tool_call_id="bad", name="bad", arguments={})))
    assert Reference[LogicUnit](implementation=FQN).model_dump() == {"implementation": FQN}


@pytest.mark.parametrize("error", ["rpc", "tool"])
async def test_errors_reach_caller(monkeypatch, error):
    requests = install_server(monkeypatch, error=error)
    tools = await LLMToolWrapper.from_logic_units(
        CallContext(process_id="p"), [Reference[LogicUnit](implementation=FQN).instantiate()]
    )
    with pytest.raises(RuntimeError, match="protocol error" if error == "rpc" else "tool error"):
        await anext(
            tools["ParallelSearch_web_search"].execute(
                ToolCall(tool_call_id="e", name="e", arguments={"objective": "x"})
            )
        )
    assert requests[-1].method == "DELETE"


async def test_timeout_and_cancellation(monkeypatch):
    install_server(monkeypatch, delay=True)
    unit = Reference[LogicUnit](implementation=FQN, timeout=0.05).instantiate()
    with pytest.raises(asyncio.TimeoutError):
        await unit.build_tools(CallContext(process_id="p"))
    task = asyncio.create_task(unit.build_tools(CallContext(process_id="p")))
    await asyncio.sleep(0.01)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
