import requests
from bs4 import BeautifulSoup

def scrape_quora():
    url = "https://www.quora.com/"
    response = requests.get(url)
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
    response = requests.get(url, headers=headers).json()

    questions = [post["data"]["title"] for post in response["data"]["children"] if post["data"]["title"].endswith("?")]
    
    return questions[:5]
