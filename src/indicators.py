"""
==========================================================
Live Stock Analysis & Prediction
Technical Indicators Module
Version : 2.0
==========================================================
"""

import numpy as np
import pandas as pd

from ta.trend import (
    SMAIndicator,
    EMAIndicator,
    MACD,
    ADXIndicator,
    CCIIndicator
)

from ta.momentum import (
    RSIIndicator,
    StochasticOscillator,
    WilliamsRIndicator
)

from ta.volatility import (
    BollingerBands,
    AverageTrueRange
)

from ta.volume import (
    OnBalanceVolumeIndicator,
    MFIIndicator,
    ChaikinMoneyFlowIndicator
)


# ==========================================================
# CHECK REQUIRED COLUMNS
# ==========================================================

REQUIRED_COLUMNS = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume"
]


def validate_dataframe(df: pd.DataFrame) -> bool:
    """
    Validate stock dataframe.
    """

    if df is None:
        return False

    if df.empty:
        return False

    for column in REQUIRED_COLUMNS:

        if column not in df.columns:
            return False

    return True


# ==========================================================
# SAFE COLUMN
# ==========================================================

def safe_series(df, column):

    if column in df.columns:

        return df[column]

    return pd.Series(
        np.nan,
        index=df.index
    )


# ==========================================================
# CLEAN DATAFRAME
# ==========================================================

def clean_dataframe(df):

    df = df.copy()

    df.columns = [str(c).strip() for c in df.columns]

    numeric_columns = [

        "Open",

        "High",

        "Low",

        "Close",

        "Volume"

    ]

    for col in numeric_columns:

        df[col] = pd.to_numeric(

            df[col],

            errors="coerce"

        )

    df = df.dropna()

    return df


# ==========================================================
# CREATE EMPTY INDICATORS
# Prevent KeyErrors
# ==========================================================

def create_empty_indicators(df):

    indicator_columns = [

        "SMA20",

        "SMA50",

        "SMA200",

        "EMA20",

        "EMA50",

        "RSI",

        "MACD",

        "MACD_SIGNAL",

        "MACD_DIFF",

        "BB_UPPER",

        "BB_MIDDLE",

        "BB_LOWER",

        "ADX",

        "ATR",

        "OBV",

        "STOCH",

        "STOCH_SIGNAL",

        "CCI",

        "WILLIAMS_R",

        "MFI",

        "CMF",

        "VWAP"

    ]

    for column in indicator_columns:

        if column not in df.columns:

            df[column] = np.nan

    return df


# ==========================================================
# MAIN FUNCTION
# ==========================================================

def calculate_indicators(df):
    """
    Main Indicator Function

    Returns
    -------
    DataFrame
    """

    if len(df) < 20:
        return df

    if not validate_dataframe(df):

        return pd.DataFrame()

    df = clean_dataframe(df)

    df = create_empty_indicators(df)

    if len(df) < 20:

        return df
    # ======================================================
    # SIMPLE MOVING AVERAGES (SMA)
    # ======================================================

    try:

        df["SMA20"] = SMAIndicator(
            close=df["Close"],
            window=20
        ).sma_indicator()

    except Exception:

        df["SMA20"] = np.nan

    try:

        df["SMA50"] = SMAIndicator(
            close=df["Close"],
            window=50
        ).sma_indicator()

    except Exception:

        df["SMA50"] = np.nan

    try:

        df["SMA200"] = SMAIndicator(
            close=df["Close"],
            window=200
        ).sma_indicator()

    except Exception:

        df["SMA200"] = np.nan

    # ======================================================
    # EXPONENTIAL MOVING AVERAGES (EMA)
    # ======================================================

    try:

        df["EMA20"] = EMAIndicator(
            close=df["Close"],
            window=20
        ).ema_indicator()

    except Exception:

        df["EMA20"] = np.nan

    try:

        df["EMA50"] = EMAIndicator(
            close=df["Close"],
            window=50
        ).ema_indicator()

    except Exception:

        df["EMA50"] = np.nan

    # ======================================================
    # RSI
    # ======================================================

    try:

        df["RSI"] = RSIIndicator(
            close=df["Close"],
            window=14
        ).rsi()

    except Exception:

        df["RSI"] = np.nan

    # ======================================================
    # MACD
    # ======================================================

    try:

        macd = MACD(
            close=df["Close"],
            window_slow=26,
            window_fast=12,
            window_sign=9
        )

        df["MACD"] = macd.macd()

        df["MACD_SIGNAL"] = macd.macd_signal()

        df["MACD_DIFF"] = macd.macd_diff()

    except Exception:

        df["MACD"] = np.nan

        df["MACD_SIGNAL"] = np.nan

        df["MACD_DIFF"] = np.nan

    # ======================================================
    # REPLACE INF VALUES
    # ======================================================

    df.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )
    # ======================================================
    # BOLLINGER BANDS
    # ======================================================

    try:

        bb = BollingerBands(
            close=df["Close"],
            window=20,
            window_dev=2
        )

        df["BB_UPPER"] = bb.bollinger_hband()

        df["BB_MIDDLE"] = bb.bollinger_mavg()

        df["BB_LOWER"] = bb.bollinger_lband()

    except Exception:

        df["BB_UPPER"] = np.nan

        df["BB_MIDDLE"] = np.nan

        df["BB_LOWER"] = np.nan

    # ======================================================
    # ADX
    # ======================================================

    try:

        if len(df) >= 28:

            adx = ADXIndicator(

                high=df["High"],

                low=df["Low"],

                close=df["Close"],

                window=14

            )

            df["ADX"] = adx.adx()

        else:

            df["ADX"] = np.nan

    except Exception:

        df["ADX"] = np.nan

    # ======================================================
    # ATR
    # ======================================================

    try:

        atr = AverageTrueRange(

            high=df["High"],

            low=df["Low"],

            close=df["Close"],

            window=14

        )

        df["ATR"] = atr.average_true_range()

    except Exception:

        df["ATR"] = np.nan

    # ======================================================
    # OBV
    # ======================================================

    try:

        obv = OnBalanceVolumeIndicator(

            close=df["Close"],

            volume=df["Volume"]

        )

        df["OBV"] = obv.on_balance_volume()

    except Exception:

        df["OBV"] = np.nan

    # ======================================================
    # STOCHASTIC OSCILLATOR
    # ======================================================

    try:

        stoch = StochasticOscillator(

            high=df["High"],

            low=df["Low"],

            close=df["Close"],

            window=14,

            smooth_window=3

        )

        df["STOCH"] = stoch.stoch()

        df["STOCH_SIGNAL"] = stoch.stoch_signal()

    except Exception:

        df["STOCH"] = np.nan

        df["STOCH_SIGNAL"] = np.nan

    # ======================================================
    # CCI
    # ======================================================

    try:

        cci = CCIIndicator(

            high=df["High"],

            low=df["Low"],

            close=df["Close"],

            window=20

        )

        df["CCI"] = cci.cci()

    except Exception:

        df["CCI"] = np.nan

    # ======================================================
    # WILLIAMS %R
    # ======================================================

    try:

        williams = WilliamsRIndicator(

            high=df["High"],

            low=df["Low"],

            close=df["Close"],

            lbp=14

        )

        df["WILLIAMS_R"] = williams.williams_r()

    except Exception:

        df["WILLIAMS_R"] = np.nan
    # ======================================================
    # MONEY FLOW INDEX (MFI)
    # ======================================================

    try:

        mfi = MFIIndicator(

            high=df["High"],

            low=df["Low"],

            close=df["Close"],

            volume=df["Volume"],

            window=14

        )

        df["MFI"] = mfi.money_flow_index()

    except Exception:

        df["MFI"] = np.nan

    # ======================================================
    # CHAIKIN MONEY FLOW (CMF)
    # ======================================================

    try:

        cmf = ChaikinMoneyFlowIndicator(

            high=df["High"],

            low=df["Low"],

            close=df["Close"],

            volume=df["Volume"],

            window=20

        )

        df["CMF"] = cmf.chaikin_money_flow()

    except Exception:

        df["CMF"] = np.nan

    # ======================================================
    # VWAP (Volume Weighted Average Price)
    # ======================================================

    try:

        typical_price = (

            df["High"]

            + df["Low"]

            + df["Close"]

        ) / 3

        cumulative_tp_volume = (

            typical_price * df["Volume"]

        ).cumsum()

        cumulative_volume = df["Volume"].cumsum()

        df["VWAP"] = (

            cumulative_tp_volume /

            cumulative_volume.replace(0, np.nan)

        )

    except Exception:

        df["VWAP"] = np.nan

    # ======================================================
    # FINAL CLEANUP
    # ======================================================

    df.replace(

        [np.inf, -np.inf],

        np.nan,

        inplace=True

    )

    # Forward fill missing values

    df.ffill(inplace=True)

    # Backward fill remaining missing values

    df.bfill(inplace=True)

    # Ensure indicator columns exist

    expected_columns = [

        "SMA20",
        "SMA50",
        "SMA200",
        "EMA20",
        "EMA50",
        "RSI",
        "MACD",
        "MACD_SIGNAL",
        "MACD_DIFF",
        "BB_UPPER",
        "BB_MIDDLE",
        "BB_LOWER",
        "ADX",
        "ATR",
        "OBV",
        "STOCH",
        "STOCH_SIGNAL",
        "CCI",
        "WILLIAMS_R",
        "MFI",
        "CMF",
        "VWAP"

    ]

    for column in expected_columns:

        if column not in df.columns:

            df[column] = np.nan

    return df                