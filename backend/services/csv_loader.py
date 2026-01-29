import pandas as pd
from pathlib import Path

def load_level1_questions():
    path = Path("backend/data/level1_questions.csv")
    return pd.read_csv(path)
