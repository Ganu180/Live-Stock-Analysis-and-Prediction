"""
==========================================================
Live Stock Analysis & Prediction
News Module
Version : 2.0
==========================================================
"""

import os
from datetime import datetime, timedelta

import pandas as pd
import requests
import streamlit as st

# ==========================================================
# CONFIGURATION
# ==========================================================

NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", "")

BASE_URL = "https://newsapi.org/v2"

REQUEST_TIMEOUT = 15

DATA_FOLDER = "data"

CACHE_FILE = os.path.join(
    DATA_FOLDER,
    "news_cache.csv"
)

os.makedirs(
    DATA_FOLDER,
    exist_ok=True
)

# ==========================================================
# NEWS CATEGORIES
# ==========================================================

NEWS_CATEGORIES = [

    "business",

    "technology",

    "finance",

    "economy",

    "markets"

]

# ==========================================================
# REQUEST HEADERS
# ==========================================================

HEADERS = {

    "User-Agent":

    "LiveStockAnalysis/2.0"

}

# ==========================================================
# API KEY VALIDATION
# ==========================================================

def api_key_available():

    return bool(
        NEWS_API_KEY.strip()
    )

# ==========================================================
# DATE HELPERS
# ==========================================================

def today():

    return datetime.utcnow().strftime(
        "%Y-%m-%d"
    )


def seven_days_ago():

    return (

        datetime.utcnow()

        - timedelta(days=7)

    ).strftime("%Y-%m-%d")

# ==========================================================
# CREATE CACHE
# ==========================================================

def initialize_news_cache():

    if os.path.exists(CACHE_FILE):
        return

    df = pd.DataFrame(

        columns=[

            "Title",

            "Source",

            "Published",

            "URL",

            "Description"

        ]

    )

    df.to_csv(
        CACHE_FILE,
        index=False
    )

# ==========================================================
# LOAD CACHE
# ==========================================================

def load_cache():

    initialize_news_cache()

    try:

        return pd.read_csv(
            CACHE_FILE
        )

    except Exception:

        return pd.DataFrame(
            columns=[
                "Title",
                "Source",
                "Published",
                "URL",
                "Description"
            ]
        )

# ==========================================================
# SAVE CACHE
# ==========================================================

def save_cache(df):

    df.to_csv(
        CACHE_FILE,
        index=False
    )

# ==========================================================
# API REQUEST
# ==========================================================

def make_request(
    endpoint,
    params
):
    """
    Generic NewsAPI request.
    """

    if not api_key_available():

        raise RuntimeError(
            "NEWS_API_KEY not configured."
        )

    params["apiKey"] = NEWS_API_KEY

    url = f"{BASE_URL}/{endpoint}"

    try:

        response = requests.get(

            url,

            params=params,

            headers=HEADERS,

            timeout=REQUEST_TIMEOUT

        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:

        print("News request timed out.")

    except requests.exceptions.HTTPError as e:

        print(f"HTTP Error: {e}")

    except requests.exceptions.RequestException as e:

        print(f"Network Error: {e}")

    return None 
# ==========================================================
# CONVERT RESPONSE TO DATAFRAME
# ==========================================================

def news_to_dataframe(articles):
    """
    Convert NewsAPI articles to DataFrame.
    """

    if not articles:
        return pd.DataFrame()

    rows = []

    for article in articles:

        rows.append({

            "Title": article.get("title", ""),

            "Source": article.get(
                "source",
                {}
            ).get("name", ""),

            "Published": article.get(
                "publishedAt",
                ""
            ),

            "URL": article.get("url", ""),

            "Description": article.get(
                "description",
                ""
            )

        })

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    df.drop_duplicates(
        subset=["Title"],
        inplace=True
    )

    df.sort_values(
        "Published",
        ascending=False,
        inplace=True
    )

    df.reset_index(
        drop=True,
        inplace=True
    )

    return df


# ==========================================================
# STOCK NEWS
# ==========================================================

def get_stock_news(
    ticker,
    limit=10
):
    """
    Fetch latest news for a stock.
    """

    ticker = ticker.strip().upper()

    response = make_request(

        "everything",

        {

            "q": ticker,

            "language": "en",

            "sortBy": "publishedAt",

            "pageSize": limit,

            "from": seven_days_ago(),

            "to": today()

        }

    )

    if response is None:
        return pd.DataFrame()

    articles = response.get(
        "articles",
        []
    )

    df = news_to_dataframe(
        articles
    )

    if not df.empty:
        save_cache(df)

    return df


# ==========================================================
# MARKET NEWS
# ==========================================================

def get_market_news(
    limit=10
):
    """
    Latest stock market news.
    """

    response = make_request(

        "top-headlines",

        {

            "category": "business",

            "language": "en",

            "pageSize": limit

        }

    )

    if response is None:
        return pd.DataFrame()

    return news_to_dataframe(

        response.get(
            "articles",
            []
        )

    )


# ==========================================================
# BUSINESS NEWS
# ==========================================================

def get_business_news(
    limit=10
):
    """
    Business & finance headlines.
    """

    response = make_request(

        "everything",

        {

            "q": "stock market OR finance OR economy",

            "language": "en",

            "sortBy": "publishedAt",

            "pageSize": limit

        }

    )

    if response is None:
        return pd.DataFrame()

    return news_to_dataframe(

        response.get(
            "articles",
            []
        )

    )


# ==========================================================
# COMPANY NEWS
# ==========================================================

def get_company_news(
    company,
    limit=10
):
    """
    Company-specific news.
    """

    response = make_request(

        "everything",

        {

            "q": company,

            "language": "en",

            "sortBy": "publishedAt",

            "pageSize": limit

        }

    )

    if response is None:
        return pd.DataFrame()

    return news_to_dataframe(

        response.get(
            "articles",
            []
        )

    )
# ==========================================================
# SEARCH NEWS
# ==========================================================

def search_news(
    keyword,
    limit=20
):
    """
    Search news using any keyword.
    """

    keyword = keyword.strip()

    if keyword == "":
        return pd.DataFrame()

    response = make_request(

        "everything",

        {

            "q": keyword,

            "language": "en",

            "sortBy": "publishedAt",

            "pageSize": limit

        }

    )

    if response is None:
        return pd.DataFrame()

    return news_to_dataframe(

        response.get(
            "articles",
            []
        )

    )


# ==========================================================
# NEWS BY CATEGORY
# ==========================================================

def get_news_by_category(
    category="business",
    limit=20
):
    """
    Get news by category.
    """

    if category.lower() not in NEWS_CATEGORIES:

        category = "business"

    response = make_request(

        "top-headlines",

        {

            "category": category.lower(),

            "language": "en",

            "pageSize": limit

        }

    )

    if response is None:
        return pd.DataFrame()

    return news_to_dataframe(

        response.get(
            "articles",
            []
        )

    )


# ==========================================================
# FILTER BY KEYWORD
# ==========================================================

def filter_news(
    df,
    keyword
):

    if df.empty:
        return df

    keyword = keyword.lower()

    mask = (

        df["Title"].fillna("").str.lower().str.contains(keyword)

        |

        df["Description"].fillna("").str.lower().str.contains(keyword)

    )

    return df[mask].reset_index(drop=True)


# ==========================================================
# FILTER BY DATE
# ==========================================================

def filter_news_by_date(
    df,
    date_string
):

    if df.empty:
        return df

    return df[
        df["Published"].astype(str).str.startswith(date_string)
    ].reset_index(drop=True)


# ==========================================================
# LOAD CACHED NEWS
# ==========================================================

def get_cached_news():

    return load_cache()


# ==========================================================
# NEWS SUMMARY
# ==========================================================

def news_summary(df):

    if df.empty:

        return {

            "Articles": 0,

            "Sources": 0

        }

    return {

        "Articles": len(df),

        "Sources": df["Source"].nunique()

    }


# ==========================================================
# SIMPLE SENTIMENT
# ==========================================================

POSITIVE_WORDS = [

    "gain",
    "growth",
    "profit",
    "bull",
    "surge",
    "beat",
    "record",
    "strong",
    "buy"

]

NEGATIVE_WORDS = [

    "loss",
    "fall",
    "drop",
    "bear",
    "decline",
    "crash",
    "weak",
    "sell",
    "miss"

]


def estimate_sentiment(text):

    if not isinstance(text, str):
        return "Neutral"

    text = text.lower()

    positive = sum(
        word in text
        for word in POSITIVE_WORDS
    )

    negative = sum(
        word in text
        for word in NEGATIVE_WORDS
    )

    if positive > negative:
        return "Positive"

    if negative > positive:
        return "Negative"

    return "Neutral"


# ==========================================================
# ADD SENTIMENT COLUMN
# ==========================================================

def add_sentiment(df):

    if df.empty:
        return df

    df = df.copy()

    df["Sentiment"] = df["Title"].apply(
        estimate_sentiment
    )

    return df
# ==========================================================
# EXPORT NEWS
# ==========================================================

def export_news(
    df,
    filename="news_export.csv"
):
    """
    Export news DataFrame to CSV.
    """

    if df.empty:
        return False

    try:

        df.to_csv(
            filename,
            index=False
        )

        return True

    except Exception as e:

        print(e)

        return False


# ==========================================================
# REFRESH CACHE
# ==========================================================

def refresh_cache():

    """
    Clears cached news.
    """

    empty = pd.DataFrame(

        columns=[

            "Title",

            "Source",

            "Published",

            "URL",

            "Description"

        ]

    )

    save_cache(empty)

    return True


# ==========================================================
# TOP HEADLINES
# ==========================================================

def get_top_headlines(limit=10):

    response = make_request(

        "top-headlines",

        {

            "country": "us",

            "category": "business",

            "pageSize": limit

        }

    )

    if response is None:
        return pd.DataFrame()

    return news_to_dataframe(

        response.get(
            "articles",
            []
        )

    )


# ==========================================================
# TRENDING STOCK NEWS
# ==========================================================

def get_trending_news(limit=15):

    keywords = (

        "stock market OR "

        "share market OR "

        "NASDAQ OR "

        "NYSE OR "

        "Nifty OR "

        "Sensex"

    )

    response = make_request(

        "everything",

        {

            "q": keywords,

            "language": "en",

            "sortBy": "publishedAt",

            "pageSize": limit

        }

    )

    if response is None:
        return pd.DataFrame()

    return news_to_dataframe(

        response.get(
            "articles",
            []
        )

    )


# ==========================================================
# UNIQUE SOURCES
# ==========================================================

def unique_sources(df):

    if df.empty:
        return []

    return sorted(

        df["Source"]

        .dropna()

        .unique()

        .tolist()

    )


# ==========================================================
# FILTER BY SOURCE
# ==========================================================

def filter_by_source(
    df,
    source
):

    if df.empty:
        return df

    return df[

        df["Source"]

        .str.lower()

        == source.lower()

    ].reset_index(drop=True)


# ==========================================================
# REMOVE DUPLICATES
# ==========================================================

def remove_duplicate_news(df):

    if df.empty:
        return df

    return (

        df

        .drop_duplicates(

            subset=["Title"]

        )

        .reset_index(drop=True)

    )


# ==========================================================
# CACHE NEWS
# ==========================================================

def cache_news(df):

    if df.empty:
        return

    cached = load_cache()

    merged = pd.concat(

        [

            cached,

            df

        ],

        ignore_index=True

    )

    merged = remove_duplicate_news(
        merged
    )

    save_cache(merged)
# ==========================================================
# NEWS STATISTICS
# ==========================================================

def news_statistics(df=None):
    """
    Returns statistics for the supplied DataFrame.
    If df is None, cached news is used.
    """

    if df is None:
        df = load_cache()

    if df.empty:

        return {

            "Articles": 0,

            "Sources": 0,

            "Positive": 0,

            "Negative": 0,

            "Neutral": 0

        }

    if "Sentiment" not in df.columns:

        df = add_sentiment(df)

    return {

        "Articles": len(df),

        "Sources": df["Source"].nunique(),

        "Positive": (df["Sentiment"] == "Positive").sum(),

        "Negative": (df["Sentiment"] == "Negative").sum(),

        "Neutral": (df["Sentiment"] == "Neutral").sum()

    }


# ==========================================================
# NEWS REPORT
# ==========================================================

def news_report():

    df = load_cache()

    if "Sentiment" not in df.columns:

        df = add_sentiment(df)

    return {

        "News": df,

        "Statistics": news_statistics(df),

        "Sources": unique_sources(df)

    }


# ==========================================================
# RESET CACHE
# ==========================================================

def reset_news_cache():

    initialize_news_cache()

    empty = pd.DataFrame(

        columns=[

            "Title",

            "Source",

            "Published",

            "URL",

            "Description"

        ]

    )

    save_cache(empty)

    return True


# ==========================================================
# CACHE SIZE
# ==========================================================

def cache_size():

    return len(load_cache())


# ==========================================================
# HAS NEWS
# ==========================================================

def has_news():

    return cache_size() > 0


# ==========================================================
# MODULE EXPORTS
# ==========================================================

__all__ = [

    "api_key_available",

    "get_stock_news",

    "get_company_news",

    "get_market_news",

    "get_business_news",

    "get_news_by_category",

    "get_top_headlines",

    "get_trending_news",

    "search_news",

    "filter_news",

    "filter_news_by_date",

    "filter_by_source",

    "news_to_dataframe",

    "estimate_sentiment",

    "add_sentiment",

    "news_summary",

    "news_statistics",

    "news_report",

    "export_news",

    "cache_news",

    "load_cache",

    "save_cache",

    "refresh_cache",

    "reset_news_cache",

    "cache_size",

    "has_news",

    "unique_sources",

    "remove_duplicate_news"

]


# ==========================================================
# MAIN (Testing)
# ==========================================================

if __name__ == "__main__":

    initialize_news_cache()

    print("News Module Version 2.0 Loaded Successfully")    