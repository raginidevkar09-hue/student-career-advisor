def match_streams(streams, normalized_scores):
    results = []

    for _, row in streams.iterrows():
        traits = row["suitable_traits"].lower().split("-")
        score = 0

        for trait in traits:
            trait = trait.strip()
            if trait in normalized_scores:
                score += normalized_scores[trait]

        results.append({
            "stream_id": row["stream_id"],
            "stream_name": row["stream_name"],
            "match_score": round(score, 2),
            "career_examples": row["career_examples"],
            "financial_notes": row["financial_support_notes"]
        })

    return sorted(results, key=lambda x: x["match_score"], reverse=True)
