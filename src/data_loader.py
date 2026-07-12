# %%
import yfinance as yf

def load_stock_data(ticker, period="2y"):

    df = yf.download(
        ticker,
        period=period,
        auto_adjust=True
    )

    return df
# %%
from src.data_loader import load_stock_data

df = load_stock_data("HDFCBANK.NS")
# %%
# %%
df = load_stock_data("HDFCBANK.NS")
print(df.head())
# %%
