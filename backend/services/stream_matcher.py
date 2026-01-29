TRAIT_COLUMN_MAP = {
    "logical": "logical_thinking_level",
    "memory": "memorization_level",
    "creative": "creativity_level",
    "physical": "physical_requirement"
}

def match_streams(numeric_df, normalized_traits):
    results = []

    for _, row in numeric_df.iterrows():
        score = 0

        for trait, column in TRAIT_COLUMN_MAP.items():
            if trait in normalized_traits and column in row:
                score += normalized_traits[trait] * row[column]

        results.append({
            "stream_id": row["stream_id"],
            "final_score": round(score, 4)
        })

    return sorted(results, key=lambda x: x["final_score"], reverse=True)
