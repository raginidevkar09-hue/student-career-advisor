import pandas as pd

FILE_PATH = "backend/data/student_marks.csv"

def analyze_student_performance(student_id: str):
    df = pd.read_csv(FILE_PATH)

    student_df = df[df["student_id"] == student_id]

    if student_df.empty:
        return {"message": "No data available"}

    student_df["percentage"] = (student_df["marks"] / student_df["max_marks"]) * 100

    summary = (
        student_df
        .groupby("subject")["percentage"]
        .mean()
        .reset_index()
    )

    weak_subjects = summary[summary["percentage"] < 40]["subject"].tolist()
    strong_subjects = summary[summary["percentage"] >= 70]["subject"].tolist()

    return {
        "weak_subjects": weak_subjects,
        "strong_subjects": strong_subjects,
        "subject_summary": summary.to_dict(orient="records")
    }
