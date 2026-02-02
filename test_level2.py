from services.level2_evaluator import evaluate_level2
from services.progress_store import save_progress

student_id = "TEST_001"

answers = {
    "Q1": 4,
    "Q2": 3,
    "Q3": 5
}

traits = evaluate_level2(answers)
print("Level 2 traits:", traits)

save_progress(student_id, traits)
print("Saved to student_progress.csv")
