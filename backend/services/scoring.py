def calculate_trait_scores(questions, answers):
    """
    questions: list of dicts from CSV
    answers: dict {question_id: answer_score}
    """

    trait_scores = {}

    for q in questions:
        qid = q["question_id"]
        trait = q["trait"]
        weight = q["weight"]

        if qid not in answers:
            continue

        score = answers[qid] * weight

        if trait not in trait_scores:
            trait_scores[trait] = 0

        trait_scores[trait] += score

    return trait_scores
