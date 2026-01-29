def filter_by_finance(streams, financial_level):
    """
    Finance filter is INFO-based.
    It does NOT remove streams.
    """

    result = []

    for stream in streams:
        score = stream.get("final_score", 0)

        # Example logic (adjust messaging, not eligibility)
        if financial_level == "LOW":
            finance_note = "Consider scholarships & govt colleges"
        elif financial_level == "HIGH":
            finance_note = "Private colleges also feasible"
        else:
            finance_note = "Mixed options available"

        result.append({
            **stream,
            "finance_note": finance_note
        })

    return result
