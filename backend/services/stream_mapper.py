STREAM_RULES = {
    "Science": ["logical", "memory"],
    "Commerce": ["logical"],
    "Arts": ["creative"],
    "Sports": ["physical"]
}

def map_traits_to_streams(normalized_scores):
    stream_scores = {}

    for stream, traits in STREAM_RULES.items():
        total = 0
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
