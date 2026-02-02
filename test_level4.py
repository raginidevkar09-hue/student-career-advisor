from backend.services.final_recommender import generate_final_recommendation

level1 = {"logical": 0.8, "creative": 0.6}
level2 = {"interest_science": 0.7}
level3 = {"strong_subjects": ["Maths", "Physics"]}

print(generate_final_recommendation("S101", level1, level2, level3))
