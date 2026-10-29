import pandas as pd

def flag_outbreaks(df: pd.DataFrame, window: int = 8, k: float = 2.0) -> pd.DataFrame:

    """
    Detect outbreak weeks by comparing current cases against a historical threshold.

    For each district, this function calculates a baseline mean and standard deviation 
    using the preceding 'window' weeks (excluding the current week to prevent baseline 
    leakage). A week is flagged as an outbreak alert if its case count strictly exceeds 
    [mean + (k * standard_deviation)].

    Args:
        df (pd.DataFrame): DataFrame containing 'district', 'week', and 'cases'.
        window (int, optional): Number of prior weeks used for baseline history. Defaults to 8.
        k (float, optional): Standard deviation multiplier for threshold sensitivity. Defaults to 2.0.

    Returns:
        pd.DataFrame: A copy of the input DataFrame with added 'threshold' and 'alert' columns.
    """

    df = df.sort_values(["district", "week"])
    g = df.groupby("district")["cases"]
    mean = g.transform(lambda s: s.shift(1).rolling(window, min_periods=window).mean())
    std = g.transform(lambda s: s.shift(1).rolling(window, min_periods=window).std())
    df['threshold'] = mean + k * std
    df['outbreak'] = df['cases'] > df['threshold']
    return df