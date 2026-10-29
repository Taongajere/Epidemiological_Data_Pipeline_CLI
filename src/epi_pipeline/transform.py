import pandas as pd

def add_indicators(df, pop): 
    # 1. Merge population data onto cleaned case data
    df = df.merge(pop, on="district", how="left")
    df = df.sort_values(["district", "week"])

    # 2. Incidence per 100,000 population
    df["incidence_per_100k"] = (df["cases"] / df["population"]) * 100_000

    # Group by district for per-district calculations
    g = df.groupby("district")["cases"]

    # 3. 4-week rolling average of cases
    df["roll4"] = g.transform(lambda s: s.rolling(4, min_periods=2).mean())

    # 4. Week-over-Week (WoW) percentage change
    df["wow_change"] = g.pct_change(fill_method=None)

    # 5. Cumulative cases
    df["cumulative"] = g.cumsum()

    return df