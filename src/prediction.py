import pandas as pd
import ta
import joblib
from pathlib import Path

# ----------------------------
# Load Model
# ----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "random_forest.pkl"

model = joblib.load(MODEL_PATH)

# ----------------------------
# Add Technical Indicators
# ----------------------------

def add_indicators(df):

    df = df.copy()

    # Handle MultiIndex columns from yfinance
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df["SMA_20"] = df["Close"].rolling(window=20).mean()

    df["SMA_50"] = df["Close"].rolling(window=50).mean()

    df["EMA_20"] = df["Close"].ewm(span=20, adjust=False).mean()

    df["RSI"] = ta.momentum.RSIIndicator(
        close=df["Close"],
        window=14
    ).rsi()

    macd = ta.trend.MACD(close=df["Close"])

    df["MACD"] = macd.macd()

    df["MACD_Signal"] = macd.macd_signal()

    bb = ta.volatility.BollingerBands(
        close=df["Close"],
        window=20
    )

    df["BB_High"] = bb.bollinger_hband()

    df["BB_Low"] = bb.bollinger_lband()

    atr = ta.volatility.AverageTrueRange(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=14
    )

    df["ATR"] = atr.average_true_range()

    return df


# ----------------------------
# Predict Next Price
# ----------------------------

def predict_next_price(df):

    df = add_indicators(df)

    df = df.dropna()

    latest = df.iloc[-1]

    X = pd.DataFrame({
        "Open": [latest["Open"]],
        "High": [latest["High"]],
        "Low": [latest["Low"]],
        "Close": [latest["Close"]],
        "Volume": [latest["Volume"]],
        "SMA_20": [latest["SMA_20"]],
        "SMA_50": [latest["SMA_50"]],
        "EMA_20": [latest["EMA_20"]],
        "RSI": [latest["RSI"]],
        "MACD": [latest["MACD"]],
        "MACD_Signal": [latest["MACD_Signal"]],
        "BB_High": [latest["BB_High"]],
        "BB_Low": [latest["BB_Low"]],
        "ATR": [latest["ATR"]]
    })

    prediction = model.predict(X)

    return float(prediction[0])