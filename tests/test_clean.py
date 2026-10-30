import pytest
import pandas as pd
import numpy as np
from epi_pipeline.clean import clean

def test_missing_week_reindexed():
    # 1. Setup: 1 district, 3 weeks, but we skip the middle week (Jan 13)
    df = pd.DataFrame({
        "district": ["Kitwe", "Kitwe"],
        "week": pd.to_datetime(["2025-01-06", "2025-01-20"]),
        "cases": [10, 15]
    })
    
    # 2. Run: Clean the data
    cleaned_df = clean(df)
    
    # 3. Assert: 
    # It should have expanded from 2 rows to 3 rows
    assert len(cleaned_df) == 3
    
    # The missing middle week should now exist and its cases should be NaN
    missing_week_row = cleaned_df[cleaned_df["week"] == "2025-01-13"]
    assert len(missing_week_row) == 1
    assert pd.isna(missing_week_row["cases"].iloc[0])