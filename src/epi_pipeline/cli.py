import typer
import pandas as pd
from pathlib import Path
app = typer.Typer(help="Epidemiological Data Pipeline CLI")
from epi_pipeline.validate import validate

@app.command()
def hello():
    """Verify CLI installation."""
    typer.echo("epipipe CLI initialized and ready.")

@app.command()
def validatecmd(path: Path = typer.Argument(..., exists=True, readable=True)): 
    df = pd.read_csv(path)
    issues = validate(df)
    if issues:
        for issue in issues:
            typer.echo(f"Problem Found: {issue}")
        raise typer.Exit(code=1)
    typer.echo(f"OK: {len(df)} rows. No issues found. Data is valid.")

if __name__ == "__main__":
    app()