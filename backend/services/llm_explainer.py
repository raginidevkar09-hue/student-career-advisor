import subprocess
import json


def explain_career_recommendation(student_id, streams, traits, level3_summary, financial_level):
    prompt = f"""
You are a career guidance expert.

Student ID: {student_id}

Traits (normalized 0-1):
{json.dumps(traits, indent=2)}

Top Recommended Streams with scores:
{json.dumps(streams, indent=2)}

Level 3 Summary:
{level3_summary}

Financial Level: {financial_level}

Tasks:
1. Explain why these streams are recommended
2. Highlight strengths and weak areas
3. Suggest a 6–12 month skill roadmap
4. Give motivating advice

Keep language simple and practical.
"""

    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        capture_output=True,
        text=True
    )

    return result.stdout.strip()
