import requests
import pandas as pd

# Replace with your own NewsAPI key
API_KEY = "412a4d28d0264fb29bd86db6fc7cdadd"

BASE_URL = "https://newsapi.org/v2/everything"


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