import os
import requests
import time

# Load API Key from Environment Variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_comment(problem, product_name, product_link):
    """Generates a human-like response using Gemini AI API."""
    if not GEMINI_API_KEY:
        print("[ERROR] Missing GEMINI_API_KEY!")
        return "Comment generation failed"

    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    prompt = (
        f"Write an engaging and relatable response to this problem: \"{problem}\". "
        f"The response should feel genuine and conversational. Casually mention the product \"{product_name}\" "
        f"and include the link subtly: {product_link}. Avoid direct promotion; instead, make it feel natural and helpful."
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    for attempt in range(5):  # Retry up to 5 times in case of errors
        try:
            response = requests.post(gemini_url, headers=headers, json=payload)

            if response.status_code == 200:
                data = response.json()
                comment = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
                return comment if comment else "Comment generation failed"

            elif response.status_code == 429:  # Rate limit exceeded
                wait_time = 2 ** attempt
                print(f"[Rate Limit] Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"[Gemini API Error] {response.status_code}: {response.text}")
                return "Comment generation failed"
        except Exception as e:
            print(f"[Gemini API Exception] {e}")
            return "Comment generation failed"

    return "Comment generation failed"
