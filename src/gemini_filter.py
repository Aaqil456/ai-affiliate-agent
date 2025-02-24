import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def is_problem_statement(statement):
    prompt = f"Is this a real problem someone is facing? Answer 'Yes' or 'No':\n\n{statement}"
    
    # Use Gemini AI to generate the response
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    
    # Extract and return the response
    answer = response.text.strip().lower()
    return "yes" in answer
