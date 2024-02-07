import asyncio
from pathlib import Path
from typing import Annotated

import typer

from eidolon_ai_sdk.util.replay import replay

app = typer.Typer()


@app.command()
def main(
    replay_location: Path,
    color: Annotated[str, typer.Option(help="The color for the displayed text")] = typer.colors.BRIGHT_GREEN,
):
    async def fn():
        typer.echo(typer.style(f"Replaying from {replay_location}", dim=True))
        async for chunk in replay(replay_location):
            typer.echo(typer.style(chunk, fg=color), nl=False)
        typer.echo("\n" + typer.style("Done", dim=True), nl=True)

    try:
        asyncio.run(fn())
    except asyncio.exceptions.CancelledError:
        typer.echo("\n" + typer.style("Canceled", dim=True), nl=True)


def run():
    app()


if __name__ == "__main__":
    run()
