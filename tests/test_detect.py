import pandas as pd
from epi_pipeline.analyze import flag_outbreaks  # adjust import based on your module file name

def test_flag_outbreaks_spike():
    # 1. Create 8 baseline weeks of 10 cases + 1 spike week of 50 cases
    weeks = pd.date_range("2025-01-01", periods=9, freq="W")
    cases = [10, 10, 10, 10, 10, 10, 10, 10, 50]
    
    df = pd.DataFrame({
        "district": ["District_A"] * 9,
        "week": weeks,
        "cases": cases
    })

    # 2. Run outbreak detection
    result = flag_outbreaks(df, window=8, k=2.0)

    # 3. Assertions
    # Baseline mean for week 9 = 10, SD = 0 -> Threshold = 10.0
    assert result["threshold"].iloc[8] == 10.0
    
    # Week 9 cases (50) > threshold (10) -> Alert should be True
    assert result["outbreak"].iloc[8] == True
    
    # First 8 weeks cannot form a full window of 8 prior weeks, so alerts should be False/NaN
    assert result["outbreak"].iloc[7] == False