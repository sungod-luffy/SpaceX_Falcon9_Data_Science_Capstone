import sqlite3
import pandas as pd


def create_sqlite_from_csv(csv_path='data/processed/spacex_processed.csv', db_path='data/spacex_launches.db'):
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(db_path)
    df.to_sql('spacex_launches', conn, if_exists='replace', index=False)
    conn.close()
    return db_path


def run_query(db_path, query):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


if __name__ == '__main__':
    print('This module creates an SQLite DB from processed CSV and runs queries.')
