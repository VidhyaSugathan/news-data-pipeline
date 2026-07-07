import requests
from sentiment import get_sentiment

API_KEY = "bea85fcf2a4c4e32a5671b5dc5094594"

url = f"https://newsapi.org/v2/top-headlines?" f"country=us&apiKey={API_KEY}"

response = requests.get(url)

data = response.json()
# print(type(data))
# print(data.keys())
articles = data["articles"]
# print(articles[0])
# # print(response.status_code)
# # print(response.json())

# print(articles["source"]["name"])
# print(source)
for article in articles:
    title = article["title"]
    author = article["author"] or "Unknown"
    description = article["description"] or "No description"
    publishedAt = article["publishedAt"]
    source = article["source"]["name"]
    sentiment = get_sentiment("title")

    print("Title       :", title)
    print("Author      :", author)
    print("Description :", description)
    print("Published At:", publishedAt)
    print("Source      :", source)
    print("Sentiment    :", sentiment)
    print("-" * 60)
