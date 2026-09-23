import pandas as pd


def load_raw(path='../data/raw/spacex_launches_raw.csv'):
    return pd.read_csv(path)


def basic_cleaning(df):
    df = df.copy()
    # create Year
    if 'launch_date_utc' in df.columns:
        df['Year'] = pd.to_datetime(df['launch_date_utc'], errors='coerce').dt.year
    # Extract core serial and landing info when available
    if 'rocket.first_stage.cores' in df.columns:
        # cores is a list-like string/object; normalize first core
        try:
            cores = df['rocket.first_stage.cores'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None)
            df['CoreSerial'] = cores.apply(lambda c: c.get('core_serial') if isinstance(c, dict) else None)
            df['LandingOutcome'] = cores.apply(lambda c: c.get('landing_success') if isinstance(c, dict) else None)
        except Exception:
            df['CoreSerial'] = None
            df['LandingOutcome'] = None
    return df
