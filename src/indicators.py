import pandas as pd
import ta


def calculate_indicators(df):
    """
    Calculate all technical indicators required
    for visualization and machine learning.
    """

    # Make a copy
    df = df.copy()

    # ----------------------------------------
    # Handle MultiIndex columns from yfinance
    # ----------------------------------------
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # ----------------------------------------
    # Remove duplicate columns if any
    # ----------------------------------------
    df = df.loc[:, ~df.columns.duplicated()]

    # ----------------------------------------
    # Simple Moving Average
    # ----------------------------------------
    df["SMA20"] = df["Close"].rolling(window=20).mean()
    df["SMA50"] = df["Close"].rolling(window=50).mean()

    # ----------------------------------------
    # Exponential Moving Average
    # ----------------------------------------
    df["EMA20"] = ta.trend.EMAIndicator(
        close=df["Close"],
        window=20
    ).ema_indicator()

    # ----------------------------------------
    # Relative Strength Index
    # ----------------------------------------
    df["RSI"] = ta.momentum.RSIIndicator(
        close=df["Close"],
        window=14
    ).rsi()

    # ----------------------------------------
    # MACD
    # ----------------------------------------
    macd = ta.trend.MACD(
        close=df["Close"]
    )

    df["MACD"] = macd.macd()
    df["MACD_Signal"] = macd.macd_signal()
    df["MACD_Histogram"] = macd.macd_diff()

    # ----------------------------------------
    # Bollinger Bands
    # ----------------------------------------
    bb = ta.volatility.BollingerBands(
        close=df["Close"],
        window=20,
        window_dev=2
    )

    df["BB_High"] = bb.bollinger_hband()
    df["BB_Low"] = bb.bollinger_lband()
    df["BB_Middle"] = bb.bollinger_mavg()
    df["BB_Width"] = bb.bollinger_wband()

    # ----------------------------------------
    # Average True Range
    # ----------------------------------------
    atr = ta.volatility.AverageTrueRange(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=14
    )

    df["ATR"] = atr.average_true_range()

    # ----------------------------------------
    # Stochastic Oscillator
    # ----------------------------------------
    stoch = ta.momentum.StochasticOscillator(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=14,
        smooth_window=3
    )

    df["Stoch_K"] = stoch.stoch()
    df["Stoch_D"] = stoch.stoch_signal()

    # ----------------------------------------
    # On Balance Volume
    # ----------------------------------------
    obv = ta.volume.OnBalanceVolumeIndicator(
        close=df["Close"],
        volume=df["Volume"]
    )

    df["OBV"] = obv.on_balance_volume()

    # ----------------------------------------
    # Average Directional Index
    # ----------------------------------------
    adx = ta.trend.ADXIndicator(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=14
    )

    df["ADX"] = adx.adx()

    # ----------------------------------------
    # Commodity Channel Index
    # ----------------------------------------
    cci = ta.trend.CCIIndicator(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=20
    )

    df["CCI"] = cci.cci()

    # ----------------------------------------
    # Williams %R
    # ----------------------------------------
    williams = ta.momentum.WilliamsRIndicator(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        lbp=14
    )

    df["WilliamsR"] = williams.williams_r()

    # ----------------------------------------
    # Fill Missing Values
    # ----------------------------------------
    df = df.bfill()

    return df