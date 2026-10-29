# tests/test_transform.py
import pandas as pd
from epi_pipeline.transform import add_indicators

def test_incidence_per_100k():
    df = pd.DataFrame({
        "district": ["A"],
        "week": pd.to_datetime(["2025-01-06"]),
        "cases": [50]
    })
    pop = pd.DataFrame({"district": ["A"], "population": [100000]})
    
    out = add_indicators(df, pop)
    
    # 50 cases in a population of 100,000 must equal 50.0 per 100k
    assert out["incidence_per_100k"].iloc[0] == 50