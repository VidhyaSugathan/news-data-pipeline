import requests
from config import NEWS_API_KEY
import json

URL = f"https://newsapi.org/v2/top-headlines?" f"country=us&apiKey={NEWS_API_KEY}"


def fetch_news():
    response = requests.get(URL)
    response.raise_for_status()
    data = response.json()

    # Save raw JSON to /tmp (only writable directory in Lambda)
    file_path = "/tmp/news.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return data
