import pandas as pd

def clean(df):
    df = df.copy()

    # clean the district names and week column
    df['district'] = df['district'].str.title().str.strip()
    df['week'] = pd.to_datetime(df['week'], errors='coerce')
    df = (
    df.groupby(["district", "week"], as_index=False)
    .agg(cases=("cases", lambda s: s.sum(min_count=1)))
)
    df.loc[df['cases'] < 0, 'cases'] = pd.NA

    full_weeks = pd.date_range(
        start=df['week'].min(),
        end=df['week'].max(),
        freq='W-MON')
    districts = df['district'].unique()

    # make a product
    master_index = pd.MultiIndex.from_product(
        [districts, full_weeks],
        names=['district', 'week']
        )
    df = df.set_index(['district', 'week']).reindex(master_index).reset_index()

    return df