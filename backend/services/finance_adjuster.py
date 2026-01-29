def adjust_by_finance(streams, financial_level):
    adjusted = []

    for stream in streams:
        score = stream.get("final_score", 0)

        # Example finance logic (INFO-based, not removal)
        if financial_level == "LOW":
            score *= 0.95
        elif financial_level == "HIGH":
            score *= 1.05

        adjusted.append({
            **stream,
            "final_score": round(score, 4)
        })

    return adjusted
