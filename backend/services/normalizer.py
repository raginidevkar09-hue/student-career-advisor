def normalize_scores(trait_scores):
    max_score = max(trait_scores.values())

    normalized = {}
    for trait, score in trait_scores.items():
        normalized[trait] = round((score / max_score) * 100, 2)

    return normalized
