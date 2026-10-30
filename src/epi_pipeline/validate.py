import pandas as pd 
import typer
from typer.cli import app

REQUIRED = {"district", "week", "cases"}

##accepts data frame in form of file link

def validate(df):
    issues = []
    # missing data 
    missing = REQUIRED - set(df.columns)
    if missing: 
        return [f"Missing columns: {sorted(missing)}"]

    #check date columns
    dates = pd.to_datetime(df["week"], errors="coerce")
    if dates.isna().any():
        issues.append(f"{dates.isna().sum()} invalid dates in 'week' column")
    #check if cases are numeric
    cases = pd.to_numeric(df["cases"], errors="coerce")
    if cases.isna().any():
        issues.append(f"{cases.isna().sum()} invalid numbers in 'cases' column")

    # check for duplicates
    dup = df.duplicated(subset=["district", "week"]).sum()
    if dup > 0:
        issues.append(f"{dup} duplicate rows based on 'district' and 'week'")

    #check for negative numbers in the cases column
    if (cases < 0).any(): 
        issues.append(f"{(cases < 0).sum()} negative numbers in 'cases' column")

    # missing weeks: compare each district to the full range
    d = df.assign(week=dates, district=df["district"].str.strip().str.title())
    full = pd.date_range(d["week"].min(), d["week"].max(), freq="W-MON")
    for name, g in d.groupby("district"):
        gap = len(full) - g["week"].nunique()
        if gap > 0:
            issues.append(f"{name}: {gap} missing week(s)")
    return issues


