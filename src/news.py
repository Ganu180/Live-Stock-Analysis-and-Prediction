import requests
import pandas as pd

import streamlit as st

NEWS_API_KEY = st.secrets["NEWS_API_KEY"]

import os

try:
    NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
except Exception:
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Replace with your own NewsAPI key
API_KEY = "412a4d28d0264fb29bd86db6fc7cdadd"

BASE_URL = "https://newsapi.org/v2/everything"

import requests
import streamlit as st

# Read News API Key
NEWS_API_KEY = st.secrets["NEWS_API_KEY"]


def get_stock_news(company_name, page_size=10):
    """
    Fetch latest news for a company.
    """

    params = {
        "q": company_name,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": "412a4d28d0264fb29bd86db6fc7cdadd"
    }

    try:

        response = requests.get(BASE_URL, params=params)

        data = response.json()

        if data["status"] != "ok":
            return pd.DataFrame()

        articles = []

        for article in data["articles"]:

            articles.append({
                "Title": article["title"],
                "Source": article["source"]["name"],
                "Published": article["publishedAt"],
                "Author": article["author"],
                "Description": article["description"],
                "URL": article["url"]
            })

        return pd.DataFrame(articles)

    except Exception as e:

        print(e)

        return pd.DataFrame()