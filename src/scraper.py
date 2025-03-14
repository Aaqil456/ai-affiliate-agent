import requests
from bs4 import BeautifulSoup

def scrape_quora():
    url = "https://www.quora.com/"
    response = requests.get(url)
    
    # Ensure response is valid
    if response.status_code != 200:
        print(f"Error fetching Quora: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    questions = []
    for post in soup.find_all("span", class_="q-text"):
        question = post.get_text()
        if question.endswith("?"):
            questions.append(question)

    return questions[:5]  # Limit results

def scrape_reddit():
    headers = {"User-Agent": "Mozilla/5.0"}
    url = "https://www.reddit.com/r/AskReddit/new.json"

    try:
        response = requests.get(url, headers=headers)

        # Ensure response is valid
        if response.status_code != 200:
            print(f"Error fetching Reddit: {response.status_code}")
            return []

        # Handle empty response
        if not response.text.strip():
            print("Error: Empty response from Reddit API")
            return []

        response_json = response.json()
        questions = [post["data"]["title"] for post in response_json["data"]["children"] if post["data"]["title"].endswith("?")]

        return questions[:5]

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []
    except ValueError:
        print("Error: Unable to decode JSON from Reddit API")
        return []
