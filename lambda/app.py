import requests
from sentiment import get_sentiment
from db import connection, cursor
import os
import json
from news_api import fetch_news
from s3_upload import upload_to_s3

data = fetch_news()
# insert_into_database(data)

upload_to_s3()
articles = data["articles"]


# print(articles["source"]["name"])
# print(source)
for article in articles:
    title = article["title"]
    author = article["author"] or "Unknown"
    description = article["description"] or "No description"
    publishedAt = article["publishedAt"]
    source = article["source"]["name"]
    sentiment = get_sentiment(title)

    cursor.execute(
        """
    INSERT INTO news_articles
    (title, author, source, description, published_at, sentiment)
    VALUES (%s, %s, %s, %s, %s, %s)
    """,
        (title, author, source, description, publishedAt, sentiment),
    )
connection.commit()
cursor.close()
connection.close()


print("News articles inserted")
