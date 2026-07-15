"""
==========================================================
Live Stock Analysis & Prediction
Portfolio Module
Version : 2.0
==========================================================
"""

import os
from typing import Optional

import pandas as pd
import yfinance as yf

# ==========================================================
# PATHS
# ==========================================================

DATA_FOLDER = "data"

PORTFOLIO_FILE = os.path.join(
    DATA_FOLDER,
    "portfolio.csv"
)

# ==========================================================
# CREATE DATA FOLDER
# ==========================================================

os.makedirs(DATA_FOLDER, exist_ok=True)

# ==========================================================
# INITIALIZE PORTFOLIO
# ==========================================================

def initialize_portfolio():
    """
    Creates portfolio CSV if it does not exist.
    """

    if not os.path.exists(PORTFOLIO_FILE):

        df = pd.DataFrame(
            columns=[
                "Stock",
                "Quantity",
                "Buy Price"
            ]
        )

        df.to_csv(
            PORTFOLIO_FILE,
            index=False
        )

# ==========================================================
# LOAD PORTFOLIO
# ==========================================================

def load_portfolio():

    initialize_portfolio()

    try:

        df = pd.read_csv(PORTFOLIO_FILE)

    except Exception:

        df = pd.DataFrame(
            columns=[
                "Stock",
                "Quantity",
                "Buy Price"
            ]
        )

    return df

# ==========================================================
# SAVE PORTFOLIO
# ==========================================================

def save_portfolio(df):

    df.to_csv(
        PORTFOLIO_FILE,
        index=False
    )

# ==========================================================
# VALIDATION
# ==========================================================

def validate_stock(stock):

    if not isinstance(stock, str):
        return False

    stock = stock.strip().upper()

    return len(stock) > 0


def validate_quantity(quantity):

    try:

        quantity = float(quantity)

        return quantity > 0

    except Exception:

        return False


def validate_price(price):

    try:

        price = float(price)

        return price > 0

    except Exception:

        return False

# ==========================================================
# ADD STOCK
# ==========================================================

def add_stock(
    stock,
    quantity,
    buy_price
):

    stock = stock.strip().upper()

    if not validate_stock(stock):
        raise ValueError("Invalid stock symbol.")

    if not validate_quantity(quantity):
        raise ValueError("Invalid quantity.")

    if not validate_price(buy_price):
        raise ValueError("Invalid buy price.")

    df = load_portfolio()

    quantity = float(quantity)
    buy_price = float(buy_price)

    # Merge duplicate stock

    existing = df["Stock"].str.upper() == stock

    if existing.any():

        index = df[existing].index[0]

        old_qty = float(df.loc[index, "Quantity"])
        old_price = float(df.loc[index, "Buy Price"])

        total_qty = old_qty + quantity

        avg_price = (
            (old_qty * old_price) +
            (quantity * buy_price)
        ) / total_qty

        df.loc[index, "Quantity"] = total_qty
        df.loc[index, "Buy Price"] = round(avg_price, 2)

    else:

        new_row = pd.DataFrame([{

            "Stock": stock,

            "Quantity": quantity,

            "Buy Price": buy_price

        }])

        df = pd.concat(
            [df, new_row],
            ignore_index=True
        )

    save_portfolio(df)
# ==========================================================
# REMOVE STOCK
# ==========================================================

def remove_stock(stock):

    """
    Remove stock using ticker symbol.
    """

    stock = stock.strip().upper()

    df = load_portfolio()

    if df.empty:
        return False

    df["Stock"] = df["Stock"].astype(str).str.upper()

    df = df[df["Stock"] != stock]

    save_portfolio(df)

    return True


# ==========================================================
# DELETE STOCK BY INDEX
# ==========================================================

def delete_stock(index):

    """
    Delete stock by dataframe index.
    """

    df = load_portfolio()

    if df.empty:
        return False

    if index not in df.index:
        return False

    df = df.drop(index)

    df.reset_index(
        drop=True,
        inplace=True
    )

    save_portfolio(df)

    return True


# ==========================================================
# UPDATE STOCK
# ==========================================================

def update_stock(
    stock,
    quantity=None,
    buy_price=None
):

    stock = stock.strip().upper()

    df = load_portfolio()

    if df.empty:
        return False

    df["Stock"] = df["Stock"].astype(str).str.upper()

    rows = df[df["Stock"] == stock]

    if rows.empty:
        return False

    idx = rows.index[0]

    if quantity is not None:

        if validate_quantity(quantity):

            df.loc[idx, "Quantity"] = float(quantity)

    if buy_price is not None:

        if validate_price(buy_price):

            df.loc[idx, "Buy Price"] = float(buy_price)

    save_portfolio(df)

    return True


# ==========================================================
# CLEAR PORTFOLIO
# ==========================================================

def clear_portfolio():

    df = pd.DataFrame(
        columns=[
            "Stock",
            "Quantity",
            "Buy Price"
        ]
    )

    save_portfolio(df)


# ==========================================================
# LIVE PRICE
# ==========================================================

def get_current_price(stock) -> Optional[float]:

    """
    Returns latest market price.
    """

    try:

        stock = stock.strip().upper()

        ticker = yf.Ticker(stock)

        info = ticker.fast_info

        if info is not None:

            price = info.get("lastPrice")

            if price is not None:

                return float(price)

    except Exception:
        pass

    try:

        data = yf.download(
            stock,
            period="5d",
            progress=False,
            auto_adjust=True
        )

        if data.empty:
            return None

        if isinstance(
            data.columns,
            pd.MultiIndex
        ):
            data.columns = data.columns.get_level_values(0)

        return float(
            data["Close"].iloc[-1]
        )

    except Exception:

        return None


# ==========================================================
# MULTIPLE STOCK PRICES
# ==========================================================

def get_current_prices(stocks):

    prices = {}

    for stock in stocks:

        prices[stock] = get_current_price(stock)

    return prices
# ==========================================================
# PORTFOLIO SUMMARY
# ==========================================================

def portfolio_summary():
    """
    Returns

    df
    total investment
    total current value
    total profit
    total return %
    """

    df = load_portfolio()

    if df.empty:

        return (
            df,
            0.0,
            0.0,
            0.0,
            0.0
        )

    current_prices = []
    investments = []
    current_values = []
    profits = []
    returns = []

    total_investment = 0.0
    total_current = 0.0

    for _, row in df.iterrows():

        stock = str(row["Stock"]).upper()

        quantity = float(row["Quantity"])

        buy_price = float(row["Buy Price"])

        current_price = get_current_price(stock)

        if current_price is None:
            current_price = 0.0

        investment = quantity * buy_price

        current_value = quantity * current_price

        profit = current_value - investment

        if investment > 0:

            return_percent = (
                profit / investment
            ) * 100

        else:

            return_percent = 0.0

        current_prices.append(
            round(current_price, 2)
        )

        investments.append(
            round(investment, 2)
        )

        current_values.append(
            round(current_value, 2)
        )

        profits.append(
            round(profit, 2)
        )

        returns.append(
            round(return_percent, 2)
        )

        total_investment += investment

        total_current += current_value

    df["Current Price"] = current_prices

    df["Investment"] = investments

    df["Current Value"] = current_values

    df["Profit/Loss"] = profits

    df["Return %"] = returns

    total_profit = total_current - total_investment

    if total_investment > 0:

        total_return = (
            total_profit / total_investment
        ) * 100

    else:

        total_return = 0.0

    return (

        df,

        round(total_investment, 2),

        round(total_current, 2),

        round(total_profit, 2),

        round(total_return, 2)

    )


# ==========================================================
# TOTAL INVESTMENT
# ==========================================================

def get_total_investment():

    _, investment, _, _, _ = portfolio_summary()

    return investment


# ==========================================================
# TOTAL CURRENT VALUE
# ==========================================================

def get_total_current_value():

    _, _, current_value, _, _ = portfolio_summary()

    return current_value


# ==========================================================
# TOTAL PROFIT
# ==========================================================

def get_total_profit():

    _, _, _, profit, _ = portfolio_summary()

    return profit


# ==========================================================
# TOTAL RETURN %
# ==========================================================

def get_total_return():

    _, _, _, _, returns = portfolio_summary()

    return returns
# ==========================================================
# PORTFOLIO STATISTICS
# ==========================================================

def portfolio_statistics():
    """
    Returns portfolio statistics.
    """

    df, investment, current_value, profit, returns = portfolio_summary()

    if df.empty:

        return {
            "Total Stocks": 0,
            "Total Investment": 0,
            "Current Value": 0,
            "Profit": 0,
            "Return %": 0,
            "Best Stock": None,
            "Worst Stock": None
        }

    best_stock = df.loc[
        df["Return %"].idxmax(),
        "Stock"
    ]

    worst_stock = df.loc[
        df["Return %"].idxmin(),
        "Stock"
    ]

    return {

        "Total Stocks": len(df),

        "Total Investment": investment,

        "Current Value": current_value,

        "Profit": profit,

        "Return %": returns,

        "Best Stock": best_stock,

        "Worst Stock": worst_stock

    }


# ==========================================================
# PORTFOLIO ALLOCATION
# ==========================================================

def portfolio_allocation():
    """
    Returns dataframe with portfolio allocation.
    """

    df, _, current_value, _, _ = portfolio_summary()

    if df.empty:

        return df

    allocation = []

    for _, row in df.iterrows():

        value = row["Current Value"]

        if current_value == 0:

            allocation.append(0)

        else:

            allocation.append(

                round(

                    (value / current_value) * 100,

                    2

                )

            )

    df["Allocation %"] = allocation

    return df


# ==========================================================
# EXPORT PORTFOLIO
# ==========================================================

def export_portfolio(file_name="portfolio_export.csv"):
    """
    Export latest portfolio summary.
    """

    df, _, _, _, _ = portfolio_summary()

    df.to_csv(

        file_name,

        index=False

    )

    return file_name


# ==========================================================
# SEARCH STOCK
# ==========================================================

def search_stock(stock):

    stock = stock.strip().upper()

    df = load_portfolio()

    if df.empty:

        return pd.DataFrame()

    df["Stock"] = df["Stock"].astype(str).str.upper()

    return df[

        df["Stock"] == stock

    ]


# ==========================================================
# STOCK EXISTS
# ==========================================================

def stock_exists(stock):

    stock = stock.strip().upper()

    df = load_portfolio()

    if df.empty:

        return False

    return (

        stock in

        df["Stock"].astype(str).str.upper().values

    )


# ==========================================================
# NUMBER OF STOCKS
# ==========================================================

def portfolio_size():

    return len(load_portfolio())


# ==========================================================
# IS PORTFOLIO EMPTY
# ==========================================================

def is_empty():

    return load_portfolio().empty
# ==========================================================
# SORT PORTFOLIO
# ==========================================================

def sort_portfolio(
    by="Profit/Loss",
    ascending=False
):
    """
    Sort portfolio by any column.
    """

    df, _, _, _, _ = portfolio_summary()

    if df.empty:
        return df

    if by not in df.columns:
        return df

    return df.sort_values(
        by=by,
        ascending=ascending
    ).reset_index(drop=True)


# ==========================================================
# TOP GAINERS
# ==========================================================

def top_gainers(limit=5):

    df = sort_portfolio(
        by="Return %",
        ascending=False
    )

    return df.head(limit)


# ==========================================================
# TOP LOSERS
# ==========================================================

def top_losers(limit=5):

    df = sort_portfolio(
        by="Return %",
        ascending=True
    )

    return df.head(limit)


# ==========================================================
# FILTER PROFITABLE STOCKS
# ==========================================================

def profitable_stocks():

    df, _, _, _, _ = portfolio_summary()

    if df.empty:
        return df

    return df[df["Profit/Loss"] > 0]


# ==========================================================
# FILTER LOSS MAKING STOCKS
# ==========================================================

def loss_stocks():

    df, _, _, _, _ = portfolio_summary()

    if df.empty:
        return df

    return df[df["Profit/Loss"] < 0]


# ==========================================================
# REFRESH LIVE PRICES
# ==========================================================

def refresh_portfolio():

    """
    Refreshes portfolio by recalculating
    live market prices.
    """

    return portfolio_summary()


# ==========================================================
# CLEAN PORTFOLIO
# ==========================================================

def clean_portfolio():

    df = load_portfolio()

    if df.empty:
        return

    df.drop_duplicates(
        subset=["Stock"],
        keep="first",
        inplace=True
    )

    df.dropna(inplace=True)

    df["Quantity"] = pd.to_numeric(
        df["Quantity"],
        errors="coerce"
    )

    df["Buy Price"] = pd.to_numeric(
        df["Buy Price"],
        errors="coerce"
    )

    df.dropna(inplace=True)

    df = df[
        (df["Quantity"] > 0)
        &
        (df["Buy Price"] > 0)
    ]

    save_portfolio(df)


# ==========================================================
# GET STOCK LIST
# ==========================================================

def get_stock_list():

    df = load_portfolio()

    if df.empty:
        return []

    return df["Stock"].tolist()


# ==========================================================
# PORTFOLIO VALUE HISTORY
# ==========================================================

def portfolio_value():

    """
    Returns current portfolio value.
    """

    _, _, current_value, _, _ = portfolio_summary()

    return current_value


# ==========================================================
# RELOAD PORTFOLIO
# ==========================================================

def reload_portfolio():

    return load_portfolio()
# ==========================================================
# PORTFOLIO ANALYTICS
# ==========================================================

def portfolio_analytics():
    """
    Returns portfolio analytics dictionary.
    """

    df, investment, current_value, profit, returns = portfolio_summary()

    analytics = {
        "Total Stocks": len(df),
        "Investment": investment,
        "Current Value": current_value,
        "Profit": profit,
        "Return %": returns
    }

    if not df.empty:

        analytics["Average Return"] = round(
            df["Return %"].mean(),
            2
        )

        analytics["Best Return"] = round(
            df["Return %"].max(),
            2
        )

        analytics["Worst Return"] = round(
            df["Return %"].min(),
            2
        )

        analytics["Average Investment"] = round(
            df["Investment"].mean(),
            2
        )

    else:

        analytics["Average Return"] = 0
        analytics["Best Return"] = 0
        analytics["Worst Return"] = 0
        analytics["Average Investment"] = 0

    return analytics


# ==========================================================
# GAINERS COUNT
# ==========================================================

def gainers_count():

    df, _, _, _, _ = portfolio_summary()

    if df.empty:
        return 0

    return int((df["Profit/Loss"] > 0).sum())


# ==========================================================
# LOSERS COUNT
# ==========================================================

def losers_count():

    df, _, _, _, _ = portfolio_summary()

    if df.empty:
        return 0

    return int((df["Profit/Loss"] < 0).sum())


# ==========================================================
# BREAK EVEN COUNT
# ==========================================================

def breakeven_count():

    df, _, _, _, _ = portfolio_summary()

    if df.empty:
        return 0

    return int((df["Profit/Loss"] == 0).sum())


# ==========================================================
# PORTFOLIO REPORT
# ==========================================================

def portfolio_report():

    df, investment, current_value, profit, returns = portfolio_summary()

    return {
        "Portfolio": df,
        "Investment": investment,
        "Current Value": current_value,
        "Profit": profit,
        "Return": returns,
        "Statistics": portfolio_statistics(),
        "Analytics": portfolio_analytics()
    }


# ==========================================================
# RESET PORTFOLIO
# ==========================================================

def reset_portfolio():

    initialize_portfolio()

    empty = pd.DataFrame(
        columns=[
            "Stock",
            "Quantity",
            "Buy Price"
        ]
    )

    save_portfolio(empty)

    return True


# ==========================================================
# MODULE EXPORTS
# ==========================================================

__all__ = [
    "initialize_portfolio",
    "load_portfolio",
    "save_portfolio",
    "add_stock",
    "remove_stock",
    "delete_stock",
    "update_stock",
    "clear_portfolio",
    "get_current_price",
    "get_current_prices",
    "portfolio_summary",
    "portfolio_statistics",
    "portfolio_allocation",
    "portfolio_analytics",
    "portfolio_report",
    "portfolio_size",
    "portfolio_value",
    "get_stock_list",
    "stock_exists",
    "search_stock",
    "top_gainers",
    "top_losers",
    "profitable_stocks",
    "loss_stocks",
    "refresh_portfolio",
    "clean_portfolio",
    "reload_portfolio",
    "reset_portfolio",
]    