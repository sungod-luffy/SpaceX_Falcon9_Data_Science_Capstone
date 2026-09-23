import pandas as pd
import matplotlib.pyplot as plt
import os
from src.coords_lookup import lookup


def generate_static_map(csv_path='data/processed/spacex_processed.csv', out_png='figures/map/spacemap_static.png'):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(csv_path)
    df = pd.read_csv(csv_path)
    lats = []
    lons = []
    labels = []
    for site in df['Launch Site'].unique():
        coord = lookup(site)
        if coord:
            lats.append(coord[0])
            lons.append(coord[1])
            labels.append(site)
    if not lats:
        raise RuntimeError('No coordinates found for launch sites')

    plt.figure(figsize=(10,6))
    plt.scatter(lons, lats, s=100, c='red', alpha=0.8)
    for i, lab in enumerate(labels):
        plt.text(lons[i]+0.2, lats[i], lab, fontsize=9)
    plt.title('Launch Sites (static)')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True, linestyle=':', alpha=0.5)
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    plt.savefig(out_png, bbox_inches='tight', dpi=150)
    plt.close()


if __name__ == '__main__':
    generate_static_map()
    print('Saved', 'figures/map/spacemap_static.png')
