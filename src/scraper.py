import requests
import os
from bs4 import BeautifulSoup

# Load Reddit API credentials from environment variables
CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("REDDIT_PASSWORD")
USER_AGENT = os.getenv("REDDIT_USER_AGENT")

def get_reddit_token():
    """Authenticate and get an OAuth token from Reddit."""
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    data = {
        "grant_type": "password",
        "username": USERNAME,
        "password": PASSWORD
    }
    headers = {"User-Agent": USER_AGENT}

    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers)

    if response.status_code != 200:
        print(f"Error getting Reddit token: {response.status_code} - {response.text}")
        return None

    return response.json().get("access_token")

def scrape_quora():
    """Scrape Quora questions."""
    url = "https://www.quora.com/"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching Quora: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    questions = [post.get_text() for post in soup.find_all("span", class_="q-text") if post.get_text().endswith("?")]

    return questions[:5]

def scrape_reddit():
    """Fetch latest AskReddit questions using OAuth authentication."""
    token = get_reddit_token()
    if not token:
        print("Error: Unable to authenticate with Reddit.")
        return []

    headers = {
        "Authorization": f"bearer {token}",
        "User-Agent": USER_AGENT
    }

    url = "https://oauth.reddit.com/r/AskReddit/new"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching Reddit: {response.status_code} - {response.text}")
        return []

    try:
        response_json = response.json()
        questions = [post["data"]["title"] for post in response_json["data"]["children"] if post["data"]["title"].endswith("?")]
        return questions[:5]
    except ValueError:
        print("Error: Unable to decode JSON from Reddit API")
        return []
