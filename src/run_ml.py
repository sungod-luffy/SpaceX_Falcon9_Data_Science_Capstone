import pandas as pd
from src.modeling import train_models
import os
import json


def run_ml(processed_csv='data/processed/spacex_processed.csv', out_dir='figures/ml'):
    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(processed_csv)
    # Prepare X and y using simple features: Payload Mass and one-hot of Booster Version Category
    if 'Payload Mass (kg)' not in df.columns or 'class' not in df.columns:
        raise RuntimeError('Required columns missing for ML')
    X = df[['Payload Mass (kg)']].fillna(0)
    if 'Booster Version Category' in df.columns:
        dummies = pd.get_dummies(df['Booster Version Category'], prefix='bv')
        X = pd.concat([X, dummies], axis=1)
    y = df['class']

    results = train_models(X, y)
    with open(f'{out_dir}/ml_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print('Saved ML results to', out_dir)


if __name__ == '__main__':
    run_ml()
