def calculate_confidence(normalized_traits, stream_recommendations):
    """
    Confidence is based on:
    1. Strength of dominant trait
    2. Gap between top 2 career streams
    """

    if len(stream_recommendations) < 2:
        return 50.0  # neutral confidence

    top_score = stream_recommendations[0].get("final_score") \
                or stream_recommendations[0].get("match_score", 0)

    second_score = stream_recommendations[1].get("final_score") \
                   or stream_recommendations[1].get("match_score", 0)

    gap_score = max(top_score - second_score, 0) * 100
    trait_strength = max(normalized_traits.values()) * 100

    confidence = (gap_score * 0.6) + (trait_strength * 0.4)

    return round(min(confidence, 100), 2)