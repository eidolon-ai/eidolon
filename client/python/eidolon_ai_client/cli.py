import asyncio
import os
import tempfile
from functools import wraps
from subprocess import call
from typing import Optional, Annotated

from eidolon_ai_client.client import Agent, Process, Machine, ProcessStatus
from eidolon_ai_client.events import StringOutputEvent, ObjectOutputEvent, LLMToolCallRequestEvent, \
    AgentStateEvent
from eidolon_ai_client.util.aiohttp import AgentError

try:
    import typer
    from rich.style import Style
    from rich.console import Console
    from rich.prompt import Prompt
    from rich.panel import Panel
    from simple_term_menu import TerminalMenu
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


async def create(agent: Optional[str] = None, verbose: Optional[bool] = False, interactive: Optional[bool] = False):
    if not agent:
        agents = await Machine(machine=server_loc).list_agents()
        if len(agents) == 0:
            err_console.print("No agents found.")
            exit(1)
        elif len(agents) > 1:
            terminal_menu = TerminalMenu(agents, title="Select an agent")
            choice = terminal_menu.show()
            if choice is None:
                err_console.print("No agent selected.")
                exit(1)
            agent = agents[choice]
        else:
            agent = agents[0]
    with console.status("Creating processes..."):
        process = await Agent(machine=server_loc, agent=agent).create_process()
    if verbose:
        console.print(process)
    else:
        console.print(process.process_id)
    if interactive:
        await run(agent=process.agent, process_id=process.process_id, stream=True, interactive=True)


processes.command("create")(coro(create))

@processes.command("delete")
@coro
async def delete(process_id: str):
    with console.status("Deleting processes..."):
        process = Process(machine=server_loc, process_id=process_id)
        await process.delete()
    console.print("Done")


async def run(
        action: Annotated[Optional[str], typer.Argument()] = None,
        process_id: Optional[str] = None,
        agent: Optional[str] = None,
        body: Optional[str] = None,
        stream: Optional[bool] = True,
        interactive: Optional[bool] = False
):
    process_status: Optional[ProcessStatus] = None
    if not process_id:
        with console.status("Fetching processes..."):
            processes_resp = await Machine(machine=server_loc).processes()
        stati: list[ProcessStatus] = processes_resp.processes
        if len(stati) == 0:
            err_console.print("No processes found.")
            exit(1)
        elif len(stati) > 1:
            terminal_menu = TerminalMenu([_status_display(status) for status in stati], title="Select a process")
            choice = terminal_menu.show()
            if choice is None:
                err_console.print("No process selected.")
                exit(1)
            process_status = stati[choice]
        else:
            process_status = stati[0]
        process_id = process_status.process_id
    if not agent:
        if not process_status:
            with console.status("Fetching agent reference..."):
                process_status = await Machine(machine=server_loc).process(process_id)
        agent = process_status.agent
    if not action:
        if not process_status:
            with console.status("Fetching available actions..."):
                process_status = await Machine(machine=server_loc).process(process_id)
        actions = process_status.available_actions
        if len(actions) == 0:
            err_console.print("No actions available.")
            exit(1)
        elif len(actions) > 1:
            terminal_menu = TerminalMenu(actions, title="Select an action")
            choice = terminal_menu.show()
            if choice is None:
                err_console.print("No action selected.")
                exit(1)
            action = actions[choice]
        else:
            action = process_status.available_actions[0]

    process: Process = Process(machine=server_loc, process_id=process_id)

    if interactive and not body:
        body = Prompt.ask("Body") or None
        if body in ["vim", "nano", "emacs"]:
            with tempfile.NamedTemporaryFile(suffix=".txt") as tf:
                call([body, tf.name])
                with open(tf.name) as file:
                    body = file.read()

    if stream:
        has_newline = True
        async for event in process.stream_action(agent, action, body):
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
        with console.status("Running AgentProgram..."):
            resp = await process.action(agent, action, body)
        console.print(resp)

    if interactive:
        await run(agent=agent, process_id=process_id, stream=True, interactive=True)


app.command("actions")(coro(run))


def _status_display(status: ProcessStatus):
    display = [status.process_id, f"agent: {status.agent}", f"state: {status.state}"]
    if status.title:
        display.append(f"title: {status.title}")
    return ", ".join(display)


if __name__ == "__main__":
    app()
