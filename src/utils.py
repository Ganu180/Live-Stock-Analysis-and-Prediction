import pandas as pd
import numpy as np
from datetime import datetime
import os

# =====================================================
# Currency Formatter
# =====================================================

def format_currency(value):

    try:
        return f"₹ {value:,.2f}"
    except:
        return "N/A"


# =====================================================
# Percentage Formatter
# =====================================================

def format_percentage(value):

    try:
        return f"{value:.2f}%"
    except:
        return "N/A"


# =====================================================
# Number Formatter
# =====================================================

def format_number(value):

    try:
        return f"{value:,}"
    except:
        return "N/A"


# =====================================================
# Get Current Date
# =====================================================

def current_date():

    return datetime.now().strftime("%d-%m-%Y")


# =====================================================
# Get Current Time
# =====================================================

def current_time():

    return datetime.now().strftime("%H:%M:%S")


# =====================================================
# Get Date & Time
# =====================================================

def current_datetime():

    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# =====================================================
# Buy / Hold / Sell Signal
# =====================================================

def generate_signal(current_price, predicted_price):

    difference = predicted_price - current_price

    percentage = (difference / current_price) * 100

    if percentage > 1:

        signal = "BUY"

    elif percentage < -1:

        signal = "SELL"

    else:

        signal = "HOLD"

    return signal, percentage


# =====================================================
# Prediction History
# =====================================================

def save_prediction_history(
    ticker,
    current_price,
    predicted_price,
    signal
):

    os.makedirs("data", exist_ok=True)

    file = "data/prediction_history.csv"

    row = {

        "Date": current_date(),

        "Time": current_time(),

        "Stock": ticker,

        "Current Price": current_price,

        "Predicted Price": predicted_price,

        "Signal": signal

    }

    if os.path.exists(file):

        df = pd.read_csv(file)

        df = pd.concat(
            [df, pd.DataFrame([row])],
            ignore_index=True
        )

    else:

        df = pd.DataFrame([row])

    df.to_csv(file, index=False)


# =====================================================
# Load Prediction History
# =====================================================

def load_prediction_history():

    file = "data/prediction_history.csv"

    if os.path.exists(file):

        return pd.read_csv(file)

    return pd.DataFrame()


# =====================================================
# Profit / Loss
# =====================================================

def calculate_profit(buy_price, current_price, quantity):

    investment = buy_price * quantity

    current_value = current_price * quantity

    profit = current_value - investment

    return investment, current_value, profit


# =====================================================
# Return Percentage
# =====================================================

def calculate_return_percentage(
    investment,
    current_value
):

    if investment == 0:

        return 0

    return ((current_value - investment) / investment) * 100


# =====================================================
# Moving Average Trend
# =====================================================

def moving_average_signal(sma20, sma50):

    if sma20 > sma50:

        return "Bullish"

    elif sma20 < sma50:

        return "Bearish"

    else:

        return "Neutral"


# =====================================================
# RSI Signal
# =====================================================

def rsi_signal(rsi):

    if rsi > 70:

        return "Overbought"

    elif rsi < 30:

        return "Oversold"

    else:

        return "Neutral"


# =====================================================
# MACD Signal
# =====================================================

def macd_signal(macd, signal):

    if macd > signal:

        return "Bullish"

    elif macd < signal:

        return "Bearish"

    else:

        return "Neutral"


# =====================================================
# Overall Recommendation
# =====================================================

def recommendation(
    predicted_signal,
    rsi_status,
    macd_status,
    ma_status
):

    score = 0

    if predicted_signal == "BUY":
        score += 1

    elif predicted_signal == "SELL":
        score -= 1

    if rsi_status == "Oversold":
        score += 1

    elif rsi_status == "Overbought":
        score -= 1

    if macd_status == "Bullish":
        score += 1

    elif macd_status == "Bearish":
        score -= 1

    if ma_status == "Bullish":
        score += 1

    elif ma_status == "Bearish":
        score -= 1

    if score >= 3:

        return "STRONG BUY"

    elif score >= 1:

        return "BUY"

    elif score == 0:

        return "HOLD"

    elif score <= -3:

        return "STRONG SELL"

    else:

        return "SELL"


# =====================================================
# Data Information
# =====================================================

def dataframe_info(df):

    info = {

        "Rows": df.shape[0],

        "Columns": df.shape[1],

        "Missing Values": df.isnull().sum().sum(),

        "Duplicate Rows": df.duplicated().sum()

    }

    return info


# =====================================================
# Clean Data
# =====================================================

def clean_dataframe(df):

    df = df.copy()

    df = df.drop_duplicates()

    df = df.ffill()

    df = df.bfill()

    return df 