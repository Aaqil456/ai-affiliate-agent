import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def generate_comment(problem, product_name, product_link):
    prompt = f"""
    Write a casual and engaging response for the following problem:
    "{problem}"

    Mention the product "{product_name}" subtly and include the link: {product_link}.
    Avoid making it sound like an ad. Make it feel like personal advice or a friendly recommendation.
    """

    # Generate response using Gemini AI
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    # Extract and return the generated text
    return response.text.strip()
