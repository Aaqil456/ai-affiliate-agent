import openai
from config import GEMINI_API_KEY

openai.api_key = GEMINI_API_KEY

def is_problem_statement(statement):
    prompt = f"Is this a real problem someone is facing? Answer 'Yes' or 'No':\n\n{statement}"
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=10
    )
    return "Yes" in response.choices[0].text
