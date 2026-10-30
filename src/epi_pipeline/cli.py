import typer
import pandas as pd
from pathlib import Path
import logging
import os


from epi_pipeline.validate import validate
from epi_pipeline.clean import clean
from epi_pipeline.transform import add_indicators
from epi_pipeline.report import generate_report, plot_district
from epi_pipeline.analyze import flag_outbreaks

app = typer.Typer(help="Epidemiological Data Pipeline CLI")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

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

@app.command()
def transform(
    cases_path: str = "data/interim/cleaned_data.csv",
    pop_path: str = "data/raw/population.csv",
    out_path: str = "data/processed/cases_with_indicators.csv"
):
    """
    Merge population data and calculate epidemiological indicators.
    """
    df_cases = pd.read_csv(cases_path)
    df_pop = pd.read_csv(pop_path)

    transformed_df = add_indicators(df_cases, df_pop)

    # Ensure target directory exists and save
    from pathlib import Path
    Path(out_path).parent.mkdir(parents=True, exist_ok=True) 
    transformed_df.to_csv(out_path, index=False)

    typer.echo(f"Transformed dataset saved to {out_path}")
    typer.echo(f"Columns: {list(transformed_df.columns)}")


@app.command()
def report(data_path: str = "data/processed/cases_with_indicators.csv"):
    df = pd.read_csv(data_path)
    df["week"] = pd.to_datetime(df["week"])
    
    # Executes chart plotting for all districts AND creates reports/report.md
    generate_report(df)
    typer.echo("Report and charts generated in reports/")

@app.command()
def run(
    path: str = "data/raw/cases.csv",
    population_path: str = "data/raw/population.csv",
    out_path: str = "reports", 
    window: int = 8,
    k: float = 2.0
): 
    """run the full complete pipeline: validate, clean, transform, detect, report"""
    os.makedirs(f'{out_path}/figures', exist_ok=True)
    raw = pd.read_csv(path)
    pop = pd.read_csv(population_path)

    for issue in validate(raw):
        typer.echo(f"Problem Found: {issue}")

    df = clean(raw)
    df = add_indicators(df, pop)
    df = flag_outbreaks(df, window, k)

    df.to_csv(f"{out_path}/report.csv", index= False)

    for d in df["district"].unique():
        plot_district(df, d, f'{out_path}/figures/{d}.png')

    # Replaces the manual plot loop and write_report with generate_report
    generate_report(df, report_path=f"{out_path}/report.md", charts_dir=f"{out_path}/figures")

    typer.echo(f'Done: Outputs in {out_path}/')


if __name__ == "__main__":
    app()