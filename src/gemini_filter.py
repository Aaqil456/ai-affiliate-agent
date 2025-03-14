import os
import requests
import time

# Load API Key from Environment Variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def is_problem_statement(statement):
    """Checks if a statement is a real problem using Gemini AI API."""
    if not GEMINI_API_KEY:
        print("[ERROR] Missing GEMINI_API_KEY!")
        return False

    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": f"Is this a real problem someone is facing? Answer only with 'Yes' or 'No'.\n\n{statement}"}]}]
    }

    for attempt in range(5):  # Retry mechanism for handling rate limits
        try:
            response = requests.post(gemini_url, headers=headers, json=payload)

            if response.status_code == 200:
                data = response.json()
                answer = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip().lower()
                return "yes" in answer  # Return True if response contains "Yes"

            elif response.status_code == 429:
                print(f"[Rate Limit] Retrying in {2 ** attempt} seconds...")
                time.sleep(2 ** attempt)
            else:
                print(f"[Gemini API Error] {response.status_code}: {response.text}")
                return False
        except Exception as e:
            print(f"[Gemini API Exception] {e}")
            return False

    return False
