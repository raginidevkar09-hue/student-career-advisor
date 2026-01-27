from fastapi import FastAPI
from backend.services.csv_loader import load_level1_questions
from backend.services.scoring import calculate_trait_scores
from backend.services.normalizer import normalize_scores
from backend.services.progress_store import save_progress
from backend.services.stream_loader import load_stream_master
from backend.services.stream_matcher import match_streams
from backend.services.finance_filter import filter_by_finance
from backend.services.marks_store import save_marks
from datetime import date
from backend.services.marks_store import save_marks
from backend.services.analytics import analyze_student_performance

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Backend running"}

@app.get("/level1/questions")
def get_level1_questions():
    df = load_level1_questions()
    return df.to_dict(orient="records")

@app.post("/level1/submit")
def submit_answers(payload: dict):
    """
    Expected payload:
    {
        "student_id": "S101",
        "answers": {"Q1":2,"Q2":3},
        "financial_level": "low"   # optional later
    }
    """

    student_id = payload["student_id"]
    answers = payload["answers"]
    financial_level = payload.get("financial_level", "any")

    # Step 1: Load questions
    df = load_level1_questions()
    questions = df.to_dict(orient="records")

    # Step 2: Trait scoring
    trait_scores = calculate_trait_scores(questions, answers)
    normalized_scores = normalize_scores(trait_scores)

    # Step 3: Save daily progress
    save_progress(student_id, normalized_scores)

    # Step 4: Stream matching
    streams_df = load_stream_master()
    recommendations = match_streams(streams_df, normalized_scores)

    # Step 5: Financial filtering (INFO based, not removal)
    final_recommendations = filter_by_finance(recommendations, financial_level)

    return {
        "raw_scores": trait_scores,
        "normalized_scores": normalized_scores,
        "stream_recommendations": final_recommendations
    }

@app.post("/progress/add")
def add_progress(payload: dict):
    """
    payload:
    {
      "student_id": "S101",
      "standard": 6,
      "subject": "Maths",
      "marks": 18,
      "max_marks": 25,
      "exam_type": "Unit Test"
    }
    """

    entry = {
        "student_id": payload["student_id"],
        "date": str(date.today()),
        "standard": payload["standard"],
        "subject": payload["subject"],
        "marks": payload["marks"],
        "max_marks": payload["max_marks"],
        "exam_type": payload["exam_type"]
    }

    save_marks(entry)

    return {"status": "Progress saved"}

@app.get("/progress/analyze/{student_id}")
def analyze_progress(student_id: str):
    return analyze_student_performance(student_id)