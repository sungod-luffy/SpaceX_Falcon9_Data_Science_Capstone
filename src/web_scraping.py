import requests
from bs4 import BeautifulSoup
import pandas as pd


WIKI_URL = 'https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches'


def scrape_wikipedia_launches(save_path='../data/raw/spacex_wiki_launches.csv', retries=3):
    headers = {
        'User-Agent': 'SpaceX-Capstone-Agent/1.0 (mailto:you@example.com)',
        'From': 'you@example.com'
    }
    for attempt in range(1, retries+1):
        r = requests.get(WIKI_URL, headers=headers, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'lxml')
            table = soup.find('table', {'class': 'wikitable'})
            if table is None:
                raise RuntimeError('Could not find wikitable on page')
            rows = []
            for tr in table.find_all('tr'):
                cols = [td.get_text(strip=True) for td in tr.find_all(['th', 'td'])]
                if cols:
                    rows.append(cols)
            df = pd.DataFrame(rows)
            df.to_csv(save_path, index=False)
            return df
        else:
            import time
            wait = 2 ** attempt
            print(f'Attempt {attempt} returned {r.status_code}, waiting {wait}s before retry')
            time.sleep(wait)
    raise RuntimeError(f'Failed to scrape Wikipedia after {retries} attempts (last status: {r.status_code})')


if __name__ == '__main__':
    try:
        df = scrape_wikipedia_launches()
        print('Saved scraped wiki table to data/raw/spacex_wiki_launches.csv with', len(df), 'rows')
    except Exception as e:
        print('Scraping failed:', e)
