import streamlit as st
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="News Sentiment Dashboard", layout="wide")


@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
    )


@st.cache_data(ttl=300)
def load_data():
    conn = get_connection()
    query = "SELECT * FROM news_articles ORDER BY published_at DESC LIMIT 500;"
    df = pd.read_sql(query, conn)
    return df


st.title("📰 News Sentiment Dashboard")

try:
    df = load_data()
except Exception as e:
    st.error(f"Could not connect to database: {e}")
    st.stop()

if df.empty:
    st.warning("No data found yet.")
    st.stop()

df["published_at"] = pd.to_datetime(df["published_at"])

# --- KPIs ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Articles", len(df))
col2.metric("Most Common Sentiment", df["sentiment"].mode()[0])
col3.metric("Sources", df["source"].nunique())

# --- Sentiment breakdown ---
st.subheader("Sentiment Breakdown")
sentiment_counts = df["sentiment"].value_counts()
st.bar_chart(sentiment_counts)

# --- Sentiment trend over time ---
st.subheader("Sentiment Trend Over Time")
trend = (
    df.groupby([df["published_at"].dt.date, "sentiment"]).size().unstack(fill_value=0)
)
st.bar_chart(trend)

# --- Sentiment by source ---
st.subheader("Sentiment by Source")
by_source = df.groupby(["source", "sentiment"]).size().unstack(fill_value=0)
st.bar_chart(by_source)

# --- Table ---
st.subheader("Latest Articles")
st.dataframe(
    df[["title", "author", "source", "sentiment", "published_at"]],
    use_container_width=True,
)
