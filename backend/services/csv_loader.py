import pandas as pd

LEVEL1_CSV_PATH = "data/level1_questions.csv"

def load_level1_questions():
    df = pd.read_csv(LEVEL1_CSV_PATH)
    return df
