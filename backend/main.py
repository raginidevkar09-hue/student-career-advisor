from fastapi import FastAPI
from datetime import date
from pydantic import BaseModel

# Question & scoring
from backend.services.csv_loader import load_level1_questions
from backend.services.scoring import calculate_trait_scores
from backend.services.normalizer import normalize_scores

# Progress & marks
from backend.services.progress_store import save_progress
from backend.services.marks_store import save_marks
from backend.services.analytics import analyze_student_performance

# Streams
from backend.services.stream_loader import (
    load_stream_master_numeric,
    load_stream_master_details
)
from backend.services.stream_matcher import match_streams
from backend.services.finance_filter import filter_by_finance
from backend.services.finance_adjuster import adjust_by_finance

# Confidence
from backend.services.confidence_calculator import calculate_confidence

from backend.services.level2_evaluator import evaluate_level2
from backend.services.final_recommender import generate_final_recommendation
from backend.services.progress_store import save_progress

app = FastAPI()


# ------------------ BASIC HEALTH ------------------
@app.get("/")
def root():
    return {"status": "Backend running"}


# ------------------ LEVEL 1 QUESTIONS ------------------
@app.get("/level1/questions")
def get_level1_questions():
    df = load_level1_questions()
    return df.to_dict(orient="records")


# ------------------ LEVEL 1 SUBMIT ------------------
@app.post("/level1/submit")
def submit_level1(payload: dict):
    """
    Expected payload:
    {
        "student_id": "S101",
        "answers": {
            "Q1": 3,
            "Q2": 4,
            "Q3": 2
        },
        "financial_level": "LOW"   # LOW | MID | HIGH
    }
    """

    student_id = payload["student_id"]
    answers = payload["answers"]
    financial_level = payload.get("financial_level", "MID")

    # 1. Load questions
    questions_df = load_level1_questions()
    questions = questions_df.to_dict(orient="records")

    # 2. Trait scoring
    trait_scores = calculate_trait_scores(questions, answers)
    normalized_scores = normalize_scores(trait_scores)

    # 3. Save trait progress
    save_progress(student_id, normalized_scores)

    # 4. Load stream data
    numeric_df = load_stream_master_numeric()
    details_df = load_stream_master_details()

    # 5. Match streams (NUMERIC scoring)
    matched_streams = match_streams(numeric_df, normalized_scores)

    # 6. Finance-aware adjustment (priority, not removal)
    adjusted_streams = adjust_by_finance(matched_streams, financial_level)

    # 7. Add finance notes
    final_streams = filter_by_finance(adjusted_streams, financial_level)

    # 8. Confidence score
    confidence = calculate_confidence(normalized_scores, final_streams)

    return {
        "raw_trait_scores": trait_scores,
        "normalized_trait_scores": normalized_scores,
        "stream_recommendations": final_streams,
        "confidence_score": confidence
    }


# ------------------ ACADEMIC PROGRESS ------------------
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


# ------------------ PERFORMANCE ANALYTICS ------------------
@app.get("/progress/analyze/{student_id}")
def analyze_progress(student_id: str):
    return analyze_student_performance(student_id)

class Level2Submission(BaseModel):
    student_id: str
    answers: dict

@app.post("/level2/submit")
def submit_level2(payload: Level2Submission):
    traits = evaluate_level2(payload.answers)

    # 🔑 THIS is the important line
    save_progress(payload.student_id, traits)

    return {
        "student_id": payload.student_id,
        "level": 2,
        "traits": traits,
        "status": "saved"
    }

@app.post("/final/recommendation")
def final_recommendation(payload: dict):
    """
    payload:
    {
        "student_id": "S101",
        "level1_traits": {...},
        "level2_traits": {...},
        "level3_traits": {...}
    }
    """

    return generate_final_recommendation(
    payload["student_id"],
    payload["level1_traits"],
    payload["level2_traits"],
    payload["level3_summary"],
    payload["financial_level"]
)

