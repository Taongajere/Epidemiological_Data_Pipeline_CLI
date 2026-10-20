import typer

app = typer.Typer(help="Epidemiological Data Pipeline CLI")

@app.command()
def hello():
    """Verify CLI installation."""
    typer.echo("epipipe CLI initialized and ready.")

if __name__ == "__main__":
    app()