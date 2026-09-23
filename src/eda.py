import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def ensure_dir(d):
    os.makedirs(d, exist_ok=True)


def run_eda(processed_csv='data/processed/spacex_processed.csv', out_dir='figures/eda'):
    ensure_dir(out_dir)
    df = pd.read_csv(processed_csv)

    # Flight Number vs Payload Mass
    if 'Flight Number' in df.columns and 'Payload Mass (kg)' in df.columns:
        plt.figure(figsize=(8,5))
        sns.scatterplot(data=df, x='Flight Number', y='Payload Mass (kg)', hue='class')
        plt.title('Flight Number vs Payload Mass')
        plt.xlabel('Flight Number')
        plt.ylabel('Payload Mass (kg)')
        plt.savefig(f'{out_dir}/flight_payload.png', bbox_inches='tight', dpi=150)
        plt.close()

    # Payload Mass vs Landing Success
    if 'Payload Mass (kg)' in df.columns and 'class' in df.columns:
        plt.figure(figsize=(8,5))
        sns.boxplot(x='class', y='Payload Mass (kg)', data=df)
        plt.title('Payload Mass by Landing Success (class)')
        plt.xlabel('Class (0=Fail,1=Success)')
        plt.ylabel('Payload Mass (kg)')
        plt.savefig(f'{out_dir}/payload_vs_success.png', bbox_inches='tight', dpi=150)
        plt.close()

    # Launch Success by Launch Site
    if 'Launch Site' in df.columns and 'class' in df.columns:
        site_counts = df.groupby('Launch Site')['class'].mean().sort_values(ascending=False)
        plt.figure(figsize=(8,5))
        site_counts.plot(kind='bar')
        plt.title('Launch Success Rate by Launch Site')
        plt.ylabel('Success Rate')
        plt.xlabel('Launch Site')
        plt.savefig(f'{out_dir}/success_by_site.png', bbox_inches='tight', dpi=150)
        plt.close()

    # Payload Distribution
    if 'Payload Mass (kg)' in df.columns:
        plt.figure(figsize=(8,5))
        sns.histplot(df['Payload Mass (kg)'].dropna(), bins=20)
        plt.title('Payload Mass Distribution')
        plt.xlabel('Payload Mass (kg)')
        plt.savefig(f'{out_dir}/payload_distribution.png', bbox_inches='tight', dpi=150)
        plt.close()

    print('EDA figures saved to', out_dir)


if __name__ == '__main__':
    run_eda()
