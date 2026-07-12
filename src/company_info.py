import yfinance as yf
import pandas as pd


def get_company_info(ticker):
    """
    Returns company information for the given ticker.
    """

    try:
        stock = yf.Ticker(ticker)

        info = stock.info

        company = {
            "Company Name": info.get("longName", "N/A"),
            "Symbol": info.get("symbol", ticker),
            "Sector": info.get("sector", "N/A"),
            "Industry": info.get("industry", "N/A"),
            "Country": info.get("country", "N/A"),
            "City": info.get("city", "N/A"),
            "Website": info.get("website", "N/A"),

            "Current Price": info.get("currentPrice", "N/A"),
            "Previous Close": info.get("previousClose", "N/A"),
            "Open": info.get("open", "N/A"),
            "Day High": info.get("dayHigh", "N/A"),
            "Day Low": info.get("dayLow", "N/A"),

            "52 Week High": info.get("fiftyTwoWeekHigh", "N/A"),
            "52 Week Low": info.get("fiftyTwoWeekLow", "N/A"),

            "Market Cap": info.get("marketCap", "N/A"),
            "Enterprise Value": info.get("enterpriseValue", "N/A"),

            "P/E Ratio": info.get("trailingPE", "N/A"),
            "Forward P/E": info.get("forwardPE", "N/A"),
            "EPS": info.get("trailingEps", "N/A"),
            "Book Value": info.get("bookValue", "N/A"),

            "Dividend Yield": info.get("dividendYield", "N/A"),
            "Dividend Rate": info.get("dividendRate", "N/A"),

            "Beta": info.get("beta", "N/A"),

            "Volume": info.get("volume", "N/A"),
            "Average Volume": info.get("averageVolume", "N/A"),

            "Employees": info.get("fullTimeEmployees", "N/A"),

            "Currency": info.get("currency", "N/A"),

            "Exchange": info.get("exchange", "N/A"),

            "Business Summary": info.get("longBusinessSummary", "N/A")
        }

        return company

    except Exception as e:

        return {
            "Error": str(e)
        }


def company_dataframe(company):

    return pd.DataFrame(
        company.items(),
        columns=["Field", "Value"]
    )