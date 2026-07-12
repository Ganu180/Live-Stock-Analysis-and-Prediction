import pandas as pd
import ta


import numpy as np
import pandas as pd

from ta.trend import (
    SMAIndicator,
    EMAIndicator,
    MACD,
    ADXIndicator
)

from ta.momentum import RSIIndicator

from ta.volatility import BollingerBands


def calculate_indicators(df):

    # -----------------------------
    # Empty dataframe check
    # -----------------------------
    if df is None or df.empty:
        return df

    # -----------------------------
    # Handle yfinance MultiIndex
    # -----------------------------
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # -----------------------------
    # Required columns check
    # -----------------------------
    required = ["Open", "High", "Low", "Close", "Volume"]

    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    # -----------------------------
    # Convert numeric columns
    # -----------------------------
    for col in required:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna().copy()

    # -----------------------------
    # Not enough data
    # -----------------------------
    if len(df) < 30:

        indicators = [
            "SMA20",
            "EMA20",
            "RSI",
            "MACD",
            "MACD_SIGNAL",
            "MACD_DIFF",
            "BB_UPPER",
            "BB_MIDDLE",
            "BB_LOWER",
            "ADX"
        ]

        for col in indicators:
            df[col] = np.nan

        return df

    # -----------------------------
    # SMA
    # -----------------------------
    try:
        df["SMA20"] = SMAIndicator(
            close=df["Close"],
            window=20
        ).sma_indicator()
    except:
        df["SMA20"] = np.nan

    # -----------------------------
    # EMA
    # -----------------------------
    try:
        df["EMA20"] = EMAIndicator(
            close=df["Close"],
            window=20
        ).ema_indicator()
    except:
        df["EMA20"] = np.nan

    # -----------------------------
    # RSI
    # -----------------------------
    try:
        df["RSI"] = RSIIndicator(
            close=df["Close"],
            window=14
        ).rsi()
    except:
        df["RSI"] = np.nan

    # -----------------------------
    # MACD
    # -----------------------------
    try:

        macd = MACD(df["Close"])

        df["MACD"] = macd.macd()
        df["MACD_SIGNAL"] = macd.macd_signal()
        df["MACD_DIFF"] = macd.macd_diff()

    except:

        df["MACD"] = np.nan
        df["MACD_SIGNAL"] = np.nan
        df["MACD_DIFF"] = np.nan

    # -----------------------------
    # Bollinger Bands
    # -----------------------------
    try:

        bb = BollingerBands(
            close=df["Close"],
            window=20,
            window_dev=2
        )

        df["BB_UPPER"] = bb.bollinger_hband()
        df["BB_MIDDLE"] = bb.bollinger_mavg()
        df["BB_LOWER"] = bb.bollinger_lband()

    except:

        df["BB_UPPER"] = np.nan
        df["BB_MIDDLE"] = np.nan
        df["BB_LOWER"] = np.nan

    # -----------------------------
    # ADX
    # -----------------------------
    try:

        adx = ADXIndicator(
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            window=14
        )

        df["ADX"] = adx.adx()

    except:

        df["ADX"] = np.nan

    return df