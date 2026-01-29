import csv
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = BASE_DIR / "data" / "student_progress.csv"

def save_progress(student_id, normalized_scores):
    file_exists = FILE_PATH.exists()

    with open(FILE_PATH, mode="a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["student_id", "date", "trait", "score"])

        today = date.today().isoformat()

        for trait, score in normalized_scores.items():
            writer.writerow([student_id, today, trait, score])
