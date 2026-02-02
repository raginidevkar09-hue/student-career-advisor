from backend.services.stream_mapper import map_streams

def generate_final_recommendation(
    student_id: str,
    level1_traits: dict,
    level2_traits: dict,
    level3_traits: dict,
    level3_summary: dict,
    financial_level: str
) -> dict:

    combined_traits = {}

    for source in [level1_traits, level2_traits, level3_traits]:
        for trait, score in source.items():
            combined_traits[trait] = combined_traits.get(trait, 0) + score

    for trait in combined_traits:
        combined_traits[trait] = round(combined_traits[trait] / 3, 3)

    stream_scores = map_streams(combined_traits)

    top_stream = next(iter(stream_scores))

    return {
        "student_id": student_id,
        "recommended_stream": top_stream,
        "stream_scores": stream_scores,
        "financial_level": financial_level,
        "level3_summary": level3_summary
    }
