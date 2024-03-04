import asyncio
import os

import dotenv
import time
from asyncio import sleep
from functools import wraps
from glob import glob
from pathlib import Path
from typing import Annotated

import typer
from typer.main import except_hook, _typer_developer_exception_attr_name
from typer.models import DeveloperExceptionConfig
from eidolon_ai_sdk.util.replay import replay

app = typer.Typer()

dotenv.load_dotenv()


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return asyncio.run(f(*args, **kwargs))
        except asyncio.exceptions.CancelledError:
            typer.echo("\n" + typer.style("Aborted.", fg=typer.colors.RED))

    return wrapper


@app.command()
@coro
async def main(
    replay_location: Path,
    color: Annotated[str, typer.Option(help="The color for the displayed text")] = typer.colors.BRIGHT_GREEN,
    watch: Annotated[bool, typer.Option(help="Watch the replay location for new files")] = False,
):
    if not watch:
        await _do_replay(replay_location, color)
    else:
        care_time = time.time()
        while True:
            replay_task = asyncio.create_task(_do_replay(replay_location, color))
            wait_for_update = asyncio.create_task(_wait_for_modification(care_time, replay_location))

            done, pending = await asyncio.wait([replay_task, wait_for_update], return_when=asyncio.FIRST_COMPLETED)
            # Replay task pending means we have a new file, so we should stop our outgoing task
            if replay_task in pending:
                replay_task.cancel(msg="Replay instructions updated")

            # still await the task since we want to propagate or handle errors
            try:
                await replay_task
                typer.echo(typer.style("Waiting for updates...", dim=True))
            except asyncio.exceptions.CancelledError:
                typer.echo("\n" + typer.style("Aborted: file modified", fg=typer.colors.RED))
            except Exception as exc:
                # Don't let exceptions break us out of the loop. Instead, let typer format and print them nicely
                setattr(
                    exc,
                    _typer_developer_exception_attr_name,
                    DeveloperExceptionConfig(
                        pretty_exceptions_enable=app.pretty_exceptions_enable,
                        pretty_exceptions_show_locals=app.pretty_exceptions_show_locals,
                        pretty_exceptions_short=app.pretty_exceptions_short,
                    ),
                )
                except_hook(type(exc), exc, exc.__traceback__)
                typer.echo(typer.style("Waiting for updates...", dim=True))
            care_time = await wait_for_update


async def _do_replay(replay_location, color):
    typer.echo(typer.style(f"Replaying from {replay_location}", dim=True))
    try:
        ended_with_newline = True
        async for chunk in replay(replay_location):
            ended_with_newline = chunk.endswith("\n")
            typer.echo(typer.style(chunk, fg=color), nl=False)
        if not ended_with_newline:
            typer.echo("\n", nl=False)
    except FileNotFoundError as fnf:
        typer.echo(typer.style(f"{fnf}", fg=typer.colors.RED))
        raise typer.Exit(1)


async def _wait_for_modification(care_time, path, delay=0.2):
    while True:
        modification_times = [os.path.getmtime(f) for f in (glob(str(path / "**")))]
        if len(modification_times) > 1:
            latest_file = max(modification_times)
        elif len(modification_times) == 1:
            latest_file = modification_times[0]
        else:
            latest_file = care_time
        if care_time < latest_file:
            return latest_file
        await sleep(delay)


if __name__ == "__main__":
    app()
