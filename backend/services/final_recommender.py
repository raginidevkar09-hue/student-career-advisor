from backend.services.stream_mapper import map_streams
from backend.services.llm_explainer import explain_career_recommendation


def generate_final_recommendation(
    student_id: str,
    level1_traits: dict,
    level2_traits: dict,
    level3_summary: dict,
    financial_level: str
) -> dict:

    # Combine only TRAIT dictionaries (Level 1 & 2)
    combined_traits = {}

    for source in [level1_traits, level2_traits]:
        for trait, score in source.items():
            combined_traits[trait] = combined_traits.get(trait, 0) + score

    # Average traits (Level 1 + Level 2 = 2 sources)
    for trait in combined_traits:
        combined_traits[trait] = round(combined_traits[trait] / 2, 3)

    # Map traits to streams
    stream_scores = map_streams(combined_traits)

    # Top stream
    top_stream = next(iter(stream_scores)) if stream_scores else None

    # LLM explanation
    llm_output = explain_career_recommendation(
    student_id,
    stream_scores,
    combined_traits,
    level3_summary,
    financial_level
)

    return {
        "student_id": student_id,
        "recommended_stream": top_stream,
        "stream_scores": stream_scores,
        "financial_level": financial_level,
        "level3_summary": level3_summary,
        "ai_guidance": llm_output
    }
