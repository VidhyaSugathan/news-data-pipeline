CREATE TABLE news_articles (
    id SERIAL PRIMARY KEY,
    title TEXT,
    author TEXT,
    source TEXT,
    description TEXT,
    published_at TIMESTAMP,
    sentiment VARCHAR(20)
);