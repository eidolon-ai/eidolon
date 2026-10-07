"""Exercise the configured tools through Eidolon's loader and tool dispatch, without an LLM."""

import asyncio
from pathlib import Path
from uuid import uuid4

import yaml

from eidolon_ai_client.events import ToolCall
from eidolon_ai_sdk.apu.call_context import CallContext
from eidolon_ai_sdk.apu.logic_unit import LLMToolWrapper, LogicUnit
from eidolon_ai_sdk.system.reference_model import Reference


async def main():
    resource = yaml.safe_load((Path(__file__).parent / "resources" / "agent.yaml").read_text())
    unit = Reference[LogicUnit].model_validate(resource["spec"]["apu"]["logic_units"][0]).instantiate()
    tools = await LLMToolWrapper.from_logic_units(CallContext(process_id=str(uuid4())), [unit])
    calls = [
        (
            "web_search",
            {
                "objective": "Find official Python asyncio task documentation",
                "search_queries": ["Python asyncio tasks documentation"],
            },
        ),
        (
            "web_fetch",
            {
                "urls": ["https://docs.python.org/3/library/asyncio-task.html"],
                "objective": "How do you cancel an asyncio task?",
            },
        ),
    ]
    for name, arguments in calls:
        tool_name = "ParallelSearch_" + name
        async for event in tools[tool_name].execute(ToolCall(tool_call_id=name, name=tool_name, arguments=arguments)):
            print(event.model_dump_json())


if __name__ == "__main__":
    asyncio.run(main())
