import openai
from config import GEMINI_API_KEY

openai.api_key = GEMINI_API_KEY

def generate_comment(problem, product_name, product_link):
    prompt = f"""
    Write a casual and engaging response for the following problem:
    "{problem}"

    Mention the product "{product_name}" subtly and include the link: {product_link}.
    Avoid making it sound like an ad. Make it feel like personal advice.
    """

    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=100
    )

    return response.choices[0].text.strip()
