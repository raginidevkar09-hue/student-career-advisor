import pandas as pd
from datetime import date
import os

FILE_PATH = "backend/data/student_marks.csv"

def save_marks(entry: dict):
    df_new = pd.DataFrame([entry])

    # Ensure directory exists
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

    if os.path.exists(FILE_PATH):
        df_old = pd.read_csv(FILE_PATH)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_csv(FILE_PATH, index=False)
