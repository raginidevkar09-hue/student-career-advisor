import pandas as pd
from backend.services.csv_loader import load_level2_questions


def evaluate_level2(user_answers: dict) -> dict:
    """
    user_answers example:
    {
        "Q1": 4,
        "Q2": 3,
        "Q3": 5
    }
    """

    questions_df = load_level2_questions()

    if questions_df.empty:
        raise ValueError("Level 2 questions file is empty")

    trait_scores = {}
    trait_weights = {}

    for _, row in questions_df.iterrows():
        qid = row["question_id"]
        trait = row["trait"]
        weight = row.get("weight", 1.0)

        if qid not in user_answers:
            continue

        score = user_answers[qid] * weight
        trait_scores[trait] = trait_scores.get(trait, 0) + score
        trait_weights[trait] = trait_weights.get(trait, 0) + weight

    normalized_traits = {}
    for trait in trait_scores:
        normalized_traits[trait] = round(
            trait_scores[trait] / trait_weights[trait], 3
        )

    return normalized_traits
