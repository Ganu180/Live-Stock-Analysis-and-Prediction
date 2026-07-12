import pandas as pd
import yfinance as yf
import os

# -----------------------------------------
# Portfolio File
# -----------------------------------------

PORTFOLIO_FILE = "data/portfolio.csv"

# -----------------------------------------
# Create Portfolio File
# -----------------------------------------

def initialize_portfolio():

    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(PORTFOLIO_FILE):

        df = pd.DataFrame(columns=[
            "Stock",
            "Quantity",
            "Buy Price"
        ])

        df.to_csv(PORTFOLIO_FILE, index=False)


# -----------------------------------------
# Load Portfolio
# -----------------------------------------

def load_portfolio():

    initialize_portfolio()

    return pd.read_csv(PORTFOLIO_FILE)


# -----------------------------------------
# Save Portfolio
# -----------------------------------------

def save_portfolio(df):

    df.to_csv(PORTFOLIO_FILE, index=False)


# -----------------------------------------
# Add Stock
# -----------------------------------------

def add_stock(stock, quantity, buy_price):

    df = load_portfolio()

    new_row = pd.DataFrame({
        "Stock": [stock],
        "Quantity": [quantity],
        "Buy Price": [buy_price]
    })

    df = pd.concat([df, new_row], ignore_index=True)

    save_portfolio(df)


# -----------------------------------------
# Delete Stock
# -----------------------------------------

def delete_stock(index):

    df = load_portfolio()

    df = df.drop(index)

    df.reset_index(drop=True, inplace=True)

    save_portfolio(df)


# -----------------------------------------
# Current Stock Price
# -----------------------------------------

def get_current_price(stock):

    try:

        data = yf.download(
            stock,
            period="1d",
            progress=False,
            auto_adjust=True
        )

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        return float(data["Close"].iloc[-1])

    except:

        return None


# -----------------------------------------
# Portfolio Summary
# -----------------------------------------

def portfolio_summary():

    df = load_portfolio()

    if df.empty:

        return df, 0, 0, 0

    current_prices = []

    investments = []

    current_values = []

    profits = []

    returns = []

    for _, row in df.iterrows():

        current = get_current_price(row["Stock"])

        if current is None:
            current = 0

        investment = row["Quantity"] * row["Buy Price"]

        current_value = row["Quantity"] * current

        profit = current_value - investment

        return_percent = 0

        if investment > 0:
            return_percent = (profit / investment) * 100

        current_prices.append(round(current,2))
        investments.append(round(investment,2))
        current_values.append(round(current_value,2))
        profits.append(round(profit,2))
        returns.append(round(return_percent,2))

    df["Current Price"] = current_prices

    df["Investment"] = investments

    df["Current Value"] = current_values

    df["Profit/Loss"] = profits

    df["Return %"] = returns

    total_investment = df["Investment"].sum()

    total_value = df["Current Value"].sum()

    total_profit = total_value - total_investment

    return df, total_investment, total_value, total_profit