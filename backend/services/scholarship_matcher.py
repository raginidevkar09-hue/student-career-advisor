def match_scholarships(streams, gender, income, scholarships_df):
    applicable = []

    for _, row in scholarships_df.iterrows():
        if row["gender"] != "Any" and row["gender"].lower() != gender.lower():
            continue

        if row["income_limit"] != "No limit" and income > int(row["income_limit"]):
            continue

        applicable.append({
            "scheme_name": row["scheme_name"],
            "benefits": row["benefits"],
            "notes": row["notes"]
        })

    return applicable
