import asyncio
import os
from functools import wraps
from typing import Optional, Annotated

from rich.style import Style

from eidolon_ai_client.client import Agent, Process, Machine, ProcessStatus
from eidolon_ai_client.events import StringOutputEvent, ObjectOutputEvent, LLMToolCallRequestEvent, \
    AgentStateEvent
from eidolon_ai_client.util.aiohttp import AgentError

try:
    import typer
    from rich.console import Console
except ImportError:
    print("The CLI dependencies are not installed. Please install with 'pip install eidolon_ai_client[cli]'.")
    exit(1)

app = typer.Typer()
processes = typer.Typer()
app.add_typer(processes, name="processes")

server_loc = os.environ.get('EIDOLON_SERVER') or "http://localhost:8080"
console = Console()
agent_console = Console(style="green italic")
dim_console = Console(style=Style(dim=True))
err_console = Console(stderr=True, style="red")


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return asyncio.run(f(*args, **kwargs))
        except AgentError as e:
            err_console.print("Agent Error:", e)
            exit(1)

    return wrapper


@processes.command("create")
@coro
async def create(agent: Annotated[str, typer.Option()], quite: Optional[bool] = False):
    process = await Agent(machine=server_loc, agent=agent).create_process()
    if quite:
        console.print(process.process_id)
    else:
        console.print(process)


@app.command("actions")
@coro
async def run(
        action: Annotated[Optional[str], typer.Argument()] = None,
        process_id: Optional[str] = None,
        agent: Optional[str] = None,
        body: Optional[str] = None,
        stream: Optional[bool] = True,
):
    process_status: Optional[ProcessStatus] = None
    if not process_id:
        processes = await Machine(machine=server_loc).processes()
        process_status = processes.processes[0]
        process_id = process_status.process_id
        if not process_id:
            err_console.print("No processes found.")
            exit(1)
    if not agent:
        if not process_status:
            process_status = await Machine(machine=server_loc).process(process_id)
        agent = process_status.agent
    if not action:
        if not process_status:
            process_status = await Machine(machine=server_loc).process(process_id)
        if len(process_status.available_actions) == 0:
            err_console.print("No actions available.")
            exit(1)
        elif len(process_status.available_actions) > 1:
            err_console.print(f"Multiple actions available. Please specify an action: {process_status.available_actions}")
            exit(1)
        else:
            action = process_status.available_actions[0]

    process = Process(machine=server_loc, agent=agent, process_id=process_id)

    if stream:
        has_newline = True
        async for event in process.stream_action(action, body):
            if event.is_root_and_type(StringOutputEvent):
                agent_console.print(event.content, end="")
                has_newline = False
            elif event.is_root_and_type(ObjectOutputEvent):
                if not has_newline:
                    console.print("")
                agent_console.print(event.content)
                has_newline = True
            elif event.is_root_and_type(LLMToolCallRequestEvent):
                if not has_newline:
                    console.print("")
                dim_console.print(event.tool_call)
                has_newline = True
            elif event.is_root_and_type(AgentStateEvent):
                if not has_newline:
                    console.print("")
                args = ["Agent transitioned to state:", event.state]
                if event.available_actions:
                    args.append(f"Available actions: {event.available_actions}")
                dim_console.print(*args)
                has_newline = True

        if not has_newline:
            console.print("")
    else:
        resp = await process.action(action, body)
        console.print(resp)


if __name__ == "__main__":
    app()
