import asyncio
from typing import Annotated

import typer

from eidolon_cli import terminal


def main(endpoint: Annotated[str, typer.Option(help="The endpoint to use.")] = "http://localhost:8080"):
    asyncio.run(terminal.run(endpoint))


if __name__ == "__main__":
    typer.run(main)
