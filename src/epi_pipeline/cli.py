import typer
import pandas as pd
from pathlib import Path
app = typer.Typer(help="Epidemiological Data Pipeline CLI")
from epi_pipeline.validate import validate
from epi_pipeline.clean import clean

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

@app.command()
def clean_cmd(input_path: Path = typer.Argument(..., exists=True, readable=True)):
    df = pd.read_csv(input_path)
    typer.echo(f"Cleaning {len(df)} rows of data...")

    cleaned_df = clean(df)

    typer.echo(f"Cleaned data has {len(cleaned_df)} rows. Saving to cleaned_data.csv")
    output_path = Path("data/interim/cleaned_data.csv")
    cleaned_df.to_csv(output_path, index=False)
    typer.echo(
        f"Cleaned data saved to {output_path}"
)


if __name__ == "__main__":
    app()