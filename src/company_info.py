"""
==========================================================
Live Stock Analysis & Prediction
Company Information Module
Version : 2.0
==========================================================
"""

import pandas as pd
import yfinance as yf

# ==========================================================
# VALIDATION
# ==========================================================

def validate_ticker(ticker):
    """
    Validate stock ticker.
    """

    if not isinstance(ticker, str):
        return False

    ticker = ticker.strip().upper()

    return len(ticker) > 0


# ==========================================================
# GET TICKER OBJECT
# ==========================================================

def get_ticker(ticker):
    """
    Returns Yahoo Finance ticker object.
    """

    if not validate_ticker(ticker):
        raise ValueError("Invalid ticker symbol.")

    return yf.Ticker(
        ticker.strip().upper()
    )


# ==========================================================
# SAFE INFO
# ==========================================================

def get_info(ticker):
    """
    Returns company information dictionary.
    """

    try:

        stock = get_ticker(ticker)

        return stock.info

    except Exception:

        return {}


# ==========================================================
# SAFE VALUE
# ==========================================================

def safe_value(info, key, default="N/A"):
    """
    Safely read a value from info dictionary.
    """

    if not isinstance(info, dict):
        return default

    return info.get(key, default)


# ==========================================================
# COMPANY PROFILE
# ==========================================================

def get_company_profile(ticker):
    """
    Returns company profile.
    """

    info = get_info(ticker)

    return {

        "Symbol":
            safe_value(info, "symbol"),

        "Company":
            safe_value(info, "longName"),

        "Sector":
            safe_value(info, "sector"),

        "Industry":
            safe_value(info, "industry"),

        "Country":
            safe_value(info, "country"),

        "Website":
            safe_value(info, "website"),

        "Employees":
            safe_value(info, "fullTimeEmployees"),

        "CEO":
            safe_value(info, "companyOfficers"),

        "Business Summary":
            safe_value(info, "longBusinessSummary")

    }


# ==========================================================
# BASIC COMPANY DETAILS
# ==========================================================

def company_details(ticker):
    """
    Returns basic company details.
    """

    info = get_info(ticker)

    return pd.DataFrame(

        {

            "Field": [

                "Company",

                "Sector",

                "Industry",

                "Country",

                "Website",

                "Employees"

            ],

            "Value": [

                safe_value(info, "longName"),

                safe_value(info, "sector"),

                safe_value(info, "industry"),

                safe_value(info, "country"),

                safe_value(info, "website"),

                safe_value(info, "fullTimeEmployees")

            ]

        }

    )


# ==========================================================
# COMPANY DESCRIPTION
# ==========================================================

def company_description(ticker):
    """
    Returns company description.
    """

    info = get_info(ticker)

    return safe_value(

        info,

        "longBusinessSummary"

    )
# ==========================================================
# MARKET INFORMATION
# ==========================================================

def market_information(ticker):
    """
    Returns market information.
    """

    info = get_info(ticker)

    return {

        "Current Price":
            safe_value(info, "currentPrice"),

        "Previous Close":
            safe_value(info, "previousClose"),

        "Open":
            safe_value(info, "open"),

        "Day High":
            safe_value(info, "dayHigh"),

        "Day Low":
            safe_value(info, "dayLow"),

        "52 Week High":
            safe_value(info, "fiftyTwoWeekHigh"),

        "52 Week Low":
            safe_value(info, "fiftyTwoWeekLow"),

        "Volume":
            safe_value(info, "volume"),

        "Average Volume":
            safe_value(info, "averageVolume")

    }


# ==========================================================
# VALUATION
# ==========================================================

def valuation_metrics(ticker):
    """
    Returns valuation metrics.
    """

    info = get_info(ticker)

    return {

        "Market Cap":
            safe_value(info, "marketCap"),

        "Enterprise Value":
            safe_value(info, "enterpriseValue"),

        "Trailing PE":
            safe_value(info, "trailingPE"),

        "Forward PE":
            safe_value(info, "forwardPE"),

        "PEG Ratio":
            safe_value(info, "pegRatio"),

        "Price To Book":
            safe_value(info, "priceToBook"),

        "Book Value":
            safe_value(info, "bookValue"),

        "Price To Sales":
            safe_value(info, "priceToSalesTrailing12Months")

    }


# ==========================================================
# DIVIDEND INFORMATION
# ==========================================================

def dividend_information(ticker):

    info = get_info(ticker)

    return {

        "Dividend Rate":
            safe_value(info, "dividendRate"),

        "Dividend Yield":
            safe_value(info, "dividendYield"),

        "Ex Dividend Date":
            safe_value(info, "exDividendDate"),

        "Payout Ratio":
            safe_value(info, "payoutRatio"),

        "Five Year Avg Yield":
            safe_value(info, "fiveYearAvgDividendYield")

    }


# ==========================================================
# SHARE INFORMATION
# ==========================================================

def share_information(ticker):

    info = get_info(ticker)

    return {

        "Shares Outstanding":
            safe_value(info, "sharesOutstanding"),

        "Float Shares":
            safe_value(info, "floatShares"),

        "Shares Short":
            safe_value(info, "sharesShort"),

        "Held By Insiders":
            safe_value(info, "heldPercentInsiders"),

        "Held By Institutions":
            safe_value(info, "heldPercentInstitutions")

    }


# ==========================================================
# FINANCIAL RATIOS
# ==========================================================

def financial_ratios(ticker):

    info = get_info(ticker)

    return {

        "Current Ratio":
            safe_value(info, "currentRatio"),

        "Quick Ratio":
            safe_value(info, "quickRatio"),

        "Debt To Equity":
            safe_value(info, "debtToEquity"),

        "Return On Assets":
            safe_value(info, "returnOnAssets"),

        "Return On Equity":
            safe_value(info, "returnOnEquity"),

        "Gross Margin":
            safe_value(info, "grossMargins"),

        "Operating Margin":
            safe_value(info, "operatingMargins"),

        "Profit Margin":
            safe_value(info, "profitMargins")

    }


# ==========================================================
# KEY STATISTICS
# ==========================================================

def key_statistics(ticker):
    """
    Returns important company statistics.
    """

    info = get_info(ticker)

    return pd.DataFrame({

        "Metric": [

            "Market Cap",

            "PE Ratio",

            "EPS",

            "Beta",

            "Dividend Yield",

            "52W High",

            "52W Low",

            "ROE",

            "ROA"

        ],

        "Value": [

            safe_value(info, "marketCap"),

            safe_value(info, "trailingPE"),

            safe_value(info, "trailingEps"),

            safe_value(info, "beta"),

            safe_value(info, "dividendYield"),

            safe_value(info, "fiftyTwoWeekHigh"),

            safe_value(info, "fiftyTwoWeekLow"),

            safe_value(info, "returnOnEquity"),

            safe_value(info, "returnOnAssets")

        ]

    })
# ==========================================================
# BALANCE SHEET
# ==========================================================

def balance_sheet(ticker):
    """
    Returns annual balance sheet.
    """

    try:

        stock = get_ticker(ticker)

        return stock.balance_sheet

    except Exception:

        return pd.DataFrame()


# ==========================================================
# QUARTERLY BALANCE SHEET
# ==========================================================

def quarterly_balance_sheet(ticker):

    try:

        stock = get_ticker(ticker)

        return stock.quarterly_balance_sheet

    except Exception:

        return pd.DataFrame()


# ==========================================================
# INCOME STATEMENT
# ==========================================================

def income_statement(ticker):

    try:

        stock = get_ticker(ticker)

        return stock.financials

    except Exception:

        return pd.DataFrame()


# ==========================================================
# QUARTERLY INCOME STATEMENT
# ==========================================================

def quarterly_income_statement(ticker):

    try:

        stock = get_ticker(ticker)

        return stock.quarterly_financials

    except Exception:

        return pd.DataFrame()


# ==========================================================
# CASH FLOW
# ==========================================================

def cash_flow(ticker):

    try:

        stock = get_ticker(ticker)

        return stock.cashflow

    except Exception:

        return pd.DataFrame()


# ==========================================================
# QUARTERLY CASH FLOW
# ==========================================================

def quarterly_cash_flow(ticker):

    try:

        stock = get_ticker(ticker)

        return stock.quarterly_cashflow

    except Exception:

        return pd.DataFrame()


# ==========================================================
# EARNINGS
# ==========================================================

def earnings(ticker):

    try:

        stock = get_ticker(ticker)

        return stock.earnings

    except Exception:

        return pd.DataFrame()


# ==========================================================
# QUARTERLY EARNINGS
# ==========================================================

def quarterly_earnings(ticker):

    try:

        stock = get_ticker(ticker)

        return stock.quarterly_earnings

    except Exception:

        return pd.DataFrame()


# ==========================================================
# DIVIDEND HISTORY
# ==========================================================

def dividend_history(ticker):

    try:

        stock = get_ticker(ticker)

        dividends = stock.dividends

        if dividends.empty:
            return pd.DataFrame()

        return dividends.reset_index()

    except Exception:

        return pd.DataFrame()


# ==========================================================
# STOCK SPLITS
# ==========================================================

def stock_splits(ticker):

    try:

        stock = get_ticker(ticker)

        splits = stock.splits

        if splits.empty:
            return pd.DataFrame()

        return splits.reset_index()

    except Exception:

        return pd.DataFrame()


# ==========================================================
# INSTITUTIONAL HOLDERS
# ==========================================================

def institutional_holders(ticker):

    try:

        stock = get_ticker(ticker)

        holders = stock.institutional_holders

        if holders is None:
            return pd.DataFrame()

        return holders

    except Exception:

        return pd.DataFrame()


# ==========================================================
# MAJOR HOLDERS
# ==========================================================

def major_holders(ticker):

    try:

        stock = get_ticker(ticker)

        holders = stock.major_holders

        if holders is None:
            return pd.DataFrame()

        return holders

    except Exception:

        return pd.DataFrame()


# ==========================================================
# MUTUAL FUND HOLDERS
# ==========================================================

def mutualfund_holders(ticker):

    try:

        stock = get_ticker(ticker)

        holders = stock.mutualfund_holders

        if holders is None:
            return pd.DataFrame()

        return holders

    except Exception:

        return pd.DataFrame()
# ==========================================================
# ANALYST RECOMMENDATIONS
# ==========================================================

def analyst_recommendations(ticker):
    """
    Returns analyst recommendations.
    """

    try:

        stock = get_ticker(ticker)

        recommendations = stock.recommendations

        if recommendations is None:
            return pd.DataFrame()

        return recommendations

    except Exception:

        return pd.DataFrame()


# ==========================================================
# SUSTAINABILITY (ESG)
# ==========================================================

def sustainability(ticker):
    """
    Returns ESG/Sustainability data.
    """

    try:

        stock = get_ticker(ticker)

        data = stock.sustainability

        if data is None:
            return pd.DataFrame()

        return data

    except Exception:

        return pd.DataFrame()


# ==========================================================
# ANALYST PRICE TARGETS
# ==========================================================

def analyst_price_targets(ticker):
    """
    Returns analyst price targets.
    """

    info = get_info(ticker)

    return {

        "Current Price":
            safe_value(info, "currentPrice"),

        "Target Mean":
            safe_value(info, "targetMeanPrice"),

        "Target High":
            safe_value(info, "targetHighPrice"),

        "Target Low":
            safe_value(info, "targetLowPrice"),

        "Recommendation":
            safe_value(info, "recommendationKey"),

        "Recommendation Mean":
            safe_value(info, "recommendationMean")

    }


# ==========================================================
# COMPANY REPORT
# ==========================================================

def company_report(ticker):
    """
    Complete company report.
    """

    return {

        "Profile":
            get_company_profile(ticker),

        "Market":
            market_information(ticker),

        "Valuation":
            valuation_metrics(ticker),

        "Financial Ratios":
            financial_ratios(ticker),

        "Dividend":
            dividend_information(ticker),

        "Share Information":
            share_information(ticker),

        "Price Targets":
            analyst_price_targets(ticker)

    }


# ==========================================================
# FINANCIAL SUMMARY
# ==========================================================

def financial_summary(ticker):

    info = get_info(ticker)

    return pd.DataFrame({

        "Metric": [

            "Revenue",

            "Net Income",

            "Free Cash Flow",

            "EBITDA",

            "Operating Cash Flow",

            "Market Cap",

            "Enterprise Value"

        ],

        "Value": [

            safe_value(info, "totalRevenue"),

            safe_value(info, "netIncomeToCommon"),

            safe_value(info, "freeCashflow"),

            safe_value(info, "ebitda"),

            safe_value(info, "operatingCashflow"),

            safe_value(info, "marketCap"),

            safe_value(info, "enterpriseValue")

        ]

    })


# ==========================================================
# MODULE EXPORTS
# ==========================================================

__all__ = [

    "validate_ticker",
    "get_ticker",
    "get_info",
    "safe_value",

    "get_company_profile",
    "company_details",
    "company_description",

    "market_information",
    "valuation_metrics",
    "financial_ratios",
    "dividend_information",
    "share_information",

    "key_statistics",
    "financial_summary",

    "balance_sheet",
    "quarterly_balance_sheet",

    "income_statement",
    "quarterly_income_statement",

    "cash_flow",
    "quarterly_cash_flow",

    "earnings",
    "quarterly_earnings",

    "dividend_history",
    "stock_splits",

    "institutional_holders",
    "major_holders",
    "mutualfund_holders",

    "analyst_recommendations",
    "analyst_price_targets",

    "sustainability",

    "company_report"

]


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    print("Company Information Module Version 2.0 Loaded Successfully")