import asyncio
import sys
from functools import wraps
from pathlib import Path

import typer

from eidolon_ai_sdk.util.replay import replay

app = typer.Typer()


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@app.command()
@coro
async def main(replay_location: Path):
    async for chunk in replay(replay_location):
        sys.stdout.write(chunk)
    sys.stdout.write("\n")


def run():
    app()
