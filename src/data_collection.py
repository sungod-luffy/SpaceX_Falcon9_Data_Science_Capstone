import requests
import pandas as pd

SPACEX_API_V3 = 'https://api.spacexdata.com/v3/launches'
SPACEX_API_V4 = 'https://api.spacexdata.com/v4/launches'


def fetch_spacex_launches():
    headers = {'User-Agent': 'SpaceX-Capstone-Agent/1.0'}
    # try v3 first
    for url in (SPACEX_API_V3, SPACEX_API_V4):
        try:
            r = requests.get(url, headers=headers, timeout=15)
            r.raise_for_status()
            data = r.json()
            # save raw JSON
            with open('../data/raw/spacex_launches_raw.json', 'w', encoding='utf-8') as f:
                import json
                json.dump(data, f, ensure_ascii=False, indent=2)
            df = pd.json_normalize(data)
            # save CSV too
            df.to_csv('../data/raw/spacex_launches_raw.csv', index=False)
            print(f'Fetched launches from {url} — rows:', len(df))
            return df
        except Exception as e:
            print('Fetch from', url, 'failed:', e)
            continue
    raise RuntimeError('Failed to fetch SpaceX launches from both v3 and v4 APIs')


if __name__ == '__main__':
    df = fetch_spacex_launches()
    print('Saved raw data to data/raw/spacex_launches_raw.json and .csv')
