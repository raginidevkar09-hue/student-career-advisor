import pandas as pd

def load_stream_master():
    return pd.read_csv("backend/data/stream_master.csv")
