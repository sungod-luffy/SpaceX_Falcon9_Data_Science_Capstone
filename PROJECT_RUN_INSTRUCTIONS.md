# Project Run Instructions

1. Create a Python virtual environment and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run data collection:

```bash
python src/data_collection.py
```

4. Run preprocessing and generate processed CSV (edit scripts as needed):

```bash
python -c "from src.preprocessing import load_raw, basic_cleaning; df=load_raw(); df=basic_cleaning(df); df.to_csv('data/processed/spacex_processed.csv', index=False)"
```

5. Launch dashboard:

```bash
python dashboard/app.py
```

6. Open notebooks in `notebooks/` for EDA and ML.
