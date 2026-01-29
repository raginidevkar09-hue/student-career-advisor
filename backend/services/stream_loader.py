import pandas as pd
from pathlib import Path

BASE = Path("backend/data")

def load_stream_master_numeric():
    path = BASE / "stream_master_numeric.csv"
    return pd.read_csv(path)

def load_stream_master_details():
    path = BASE / "stream_master_details.csv"
    return pd.read_csv(path)
