import psycopg2

connection = psycopg2.connect(
    host="localhost",
    database="news_pipeline",
    user="postgres",
    password="post123",
    port="5432",
)
print("Database connected successfully!")
