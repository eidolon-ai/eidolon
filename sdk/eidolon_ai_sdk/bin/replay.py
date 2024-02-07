import typer

app = typer.Typer()


@app.command()
def main(name: str):
    typer.echo(f"Hello {name}")


def run():
    app()
