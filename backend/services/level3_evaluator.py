from backend.services.analytics import analyze_student_performance

SUBJECT_TO_TRAIT = {
    "Maths": "logical",
    "Physics": "logical",
    "Chemistry": "memory",
    "Biology": "memory",
    "English": "creative",
    "History": "creative"
}

def evaluate_level3(student_id: str):
    analysis = analyze_student_performance(student_id)

    if "subject_summary" not in analysis:
        return {}

    academic_traits = {}

    for row in analysis["subject_summary"]:
        subject = row["subject"]
        percentage = row["percentage"]

        trait = SUBJECT_TO_TRAIT.get(subject)
        if not trait:
            continue

        academic_traits.setdefault(trait, 0)
        academic_traits[trait] += percentage

    for trait in academic_traits:
        academic_traits[trait] = round(academic_traits[trait] / 100, 2)

    return academic_traits
