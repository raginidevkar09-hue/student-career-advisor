# backend/services/stream_mapper.py

STREAM_RULES = {
    "Science": ["logical", "memory"],
    "Commerce": ["logical"],
    "Arts": ["creative"],
    "Sports": ["physical"]
}


def map_streams(normalized_scores: dict) -> dict:
    """
    Maps normalized trait scores to career streams.

    Input example:
    {
        "logical": 0.82,
        "memory": 0.71,
        "creative": 0.64,
        "physical": 0.55
    }

    Output example:
    {
        "Science": 0.77,
        "Commerce": 0.82,
        "Arts": 0.64,
        "Sports": 0.55
    }
    """

    stream_scores = {}

    for stream, traits in STREAM_RULES.items():
        total = 0.0
        count = 0

        for trait in traits:
            if trait in normalized_scores:
                total += normalized_scores[trait]
                count += 1

        if count > 0:
            stream_scores[stream] = round(total / count, 2)

    # Sort streams by score (highest first)
    ranked_streams = dict(
        sorted(stream_scores.items(), key=lambda x: x[1], reverse=True)
    )

    return ranked_streams
