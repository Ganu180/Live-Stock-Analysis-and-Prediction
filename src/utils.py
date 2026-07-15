"""
==========================================================
Live Stock Analysis & Prediction
utils.py (Version 2.0)
==========================================================
Utility functions used throughout the application.
Compatible with:
- Python 3.12
- Streamlit Community Cloud
==========================================================
"""

import os
import csv
from datetime import datetime
from pathlib import Path

import pandas as pd

# ==========================================================
# Configuration
# ==========================================================

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

PREDICTION_HISTORY_FILE = DATA_DIR / "prediction_history.csv"

PREDICTION_COLUMNS = [
    "Date",
    "Time",
    "Ticker",
    "Current Price",
    "Predicted Price",
    "Signal"
]

# ==========================================================
# Date & Time Utilities
# ==========================================================

def current_date() -> str:
    """
    Returns today's date.
    Example:
    15-07-2026
    """
    return datetime.now().strftime("%d-%m-%Y")


def current_time() -> str:
    """
    Returns current time.
    Example:
    09:45:18 PM
    """
    return datetime.now().strftime("%I:%M:%S %p")


# ==========================================================
# Formatting Utilities
# ==========================================================

def format_currency(value):
    """
    Format number as currency.
    """

    try:
        return f"₹{float(value):,.2f}"
    except Exception:
        return "₹0.00"


def format_percentage(value):
    """
    Format decimal as percentage.
    """

    try:
        return f"{float(value):.2f}%"
    except Exception:
        return "0.00%"


# ==========================================================
# Prediction History File
# ==========================================================

def initialize_prediction_history():
    """
    Creates prediction history CSV if it does not exist.
    """

    if not PREDICTION_HISTORY_FILE.exists():

        df = pd.DataFrame(columns=PREDICTION_COLUMNS)

        df.to_csv(
            PREDICTION_HISTORY_FILE,
            index=False
        )


# Automatically initialize file
initialize_prediction_history()


# ==========================================================
# Trading Signal Generator
# ==========================================================

def generate_signal(current_price, predicted_price):
    """
    Generate BUY / SELL / HOLD signal.
    """

    try:

        current_price = float(current_price)
        predicted_price = float(predicted_price)

        change = (
            (predicted_price - current_price)
            / current_price
        ) * 100

        if change >= 2:
            return "BUY"

        elif change <= -2:
            return "SELL"

        else:
            return "HOLD"

    except Exception:
        return "HOLD"
# ==========================================================
# Prediction History Functions
# ==========================================================

def save_prediction_history(
    ticker,
    current_price,
    predicted_price,
    signal
):
    """
    Save prediction to CSV history.
    """

    try:

        initialize_prediction_history()

        new_record = pd.DataFrame([{
            "Date": current_date(),
            "Time": current_time(),
            "Ticker": str(ticker).upper(),
            "Current Price": round(float(current_price), 2),
            "Predicted Price": round(float(predicted_price), 2),
            "Signal": signal
        }])

        history = pd.read_csv(PREDICTION_HISTORY_FILE)

        history = pd.concat(
            [history, new_record],
            ignore_index=True
        )

        history.to_csv(
            PREDICTION_HISTORY_FILE,
            index=False
        )

        return True

    except Exception as e:
        print(f"Error saving prediction history: {e}")
        return False


# ==========================================================
# Load Prediction History
# ==========================================================

def load_prediction_history():
    """
    Load saved prediction history.
    """

    try:

        initialize_prediction_history()

        history = pd.read_csv(PREDICTION_HISTORY_FILE)

        if history.empty:
            return pd.DataFrame(columns=PREDICTION_COLUMNS)

        return history

    except Exception as e:

        print(f"Error loading history: {e}")

        return pd.DataFrame(columns=PREDICTION_COLUMNS)


# ==========================================================
# Clear Prediction History
# ==========================================================

def clear_prediction_history():
    """
    Remove all saved prediction history.
    """

    try:

        df = pd.DataFrame(columns=PREDICTION_COLUMNS)

        df.to_csv(
            PREDICTION_HISTORY_FILE,
            index=False
        )

        return True

    except Exception as e:

        print(f"Error clearing history: {e}")

        return False


# ==========================================================
# Latest Prediction
# ==========================================================

def latest_prediction():
    """
    Returns the most recent prediction.
    """

    try:

        history = load_prediction_history()

        if history.empty:
            return None

        return history.iloc[-1]

    except Exception:
        return None


# ==========================================================
# Prediction Count
# ==========================================================

def prediction_count():
    """
    Returns total number of predictions.
    """

    try:

        history = load_prediction_history()

        return len(history)

    except Exception:
        return 0
# ==========================================================
# Recommendation Engine
# ==========================================================

def recommendation(current_price, predicted_price):
    """
    Returns BUY / HOLD / SELL recommendation.
    """

    try:

        current_price = float(current_price)
        predicted_price = float(predicted_price)

        difference = (
            (predicted_price - current_price)
            / current_price
        ) * 100

        if difference >= 5:
            return "🟢 Strong Buy"

        elif difference >= 2:
            return "🟢 Buy"

        elif difference <= -5:
            return "🔴 Strong Sell"

        elif difference <= -2:
            return "🔴 Sell"

        else:
            return "🟡 Hold"

    except Exception:
        return "🟡 Hold"


# ==========================================================
# RSI Signal
# ==========================================================

def rsi_signal(rsi):
    """
    Returns signal based on RSI.
    """

    try:

        rsi = float(rsi)

        if rsi < 30:
            return "Oversold (Buy)"

        elif rsi > 70:
            return "Overbought (Sell)"

        else:
            return "Neutral"

    except Exception:
        return "Neutral"


# ==========================================================
# MACD Signal
# ==========================================================

def macd_signal(macd, signal_line):
    """
    Returns MACD trading signal.
    """

    try:

        macd = float(macd)
        signal_line = float(signal_line)

        if macd > signal_line:
            return "Bullish"

        elif macd < signal_line:
            return "Bearish"

        else:
            return "Neutral"

    except Exception:
        return "Neutral"


# ==========================================================
# Moving Average Signal
# ==========================================================

def moving_average_signal(close_price, sma20, sma50):
    """
    Generates Moving Average signal.
    """

    try:

        close_price = float(close_price)
        sma20 = float(sma20)
        sma50 = float(sma50)

        if close_price > sma20 > sma50:
            return "Strong Bullish"

        elif close_price > sma20:
            return "Bullish"

        elif close_price < sma20 < sma50:
            return "Strong Bearish"

        elif close_price < sma20:
            return "Bearish"

        else:
            return "Neutral"

    except Exception:
        return "Neutral"


# ==========================================================
# Overall Technical Signal
# ==========================================================

def technical_signal(
    current_price,
    predicted_price,
    rsi,
    macd,
    signal_line,
    sma20,
    sma50
):
    """
    Combine all technical indicators into one signal.
    """

    score = 0

    if generate_signal(current_price, predicted_price) == "BUY":
        score += 2
    elif generate_signal(current_price, predicted_price) == "SELL":
        score -= 2

    if rsi_signal(rsi) == "Oversold (Buy)":
        score += 1
    elif rsi_signal(rsi) == "Overbought (Sell)":
        score -= 1

    if macd_signal(macd, signal_line) == "Bullish":
        score += 1
    elif macd_signal(macd, signal_line) == "Bearish":
        score -= 1

    ma = moving_average_signal(
        current_price,
        sma20,
        sma50
    )

    if ma == "Strong Bullish":
        score += 2

    elif ma == "Bullish":
        score += 1

    elif ma == "Strong Bearish":
        score -= 2

    elif ma == "Bearish":
        score -= 1

    if score >= 3:
        return "🟢 BUY"

    elif score <= -3:
        return "🔴 SELL"

    return "🟡 HOLD"
# ==========================================================
# Validation Utilities
# ==========================================================

def is_valid_number(value):
    """
    Check whether the value can be converted to float.
    """

    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def safe_float(value, default=0.0):
    """
    Safely convert any value to float.
    """

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


# ==========================================================
# Portfolio Helper
# ==========================================================

def calculate_profit_loss(buy_price, current_price, quantity):
    """
    Calculate profit/loss information.
    """

    buy_price = safe_float(buy_price)
    current_price = safe_float(current_price)
    quantity = safe_float(quantity)

    investment = buy_price * quantity
    current_value = current_price * quantity
    profit_loss = current_value - investment

    if investment > 0:
        returns = (profit_loss / investment) * 100
    else:
        returns = 0.0

    return {
        "investment": investment,
        "current_value": current_value,
        "profit_loss": profit_loss,
        "returns": returns,
    }


# ==========================================================
# Export Prediction History
# ==========================================================

def export_prediction_history(filepath):
    """
    Export prediction history to CSV.
    """

    try:

        history = load_prediction_history()

        history.to_csv(filepath, index=False)

        return True

    except Exception as e:

        print(f"Export Error: {e}")

        return False


# ==========================================================
# Reset Prediction History
# ==========================================================

def reset_prediction_history():
    """
    Reset prediction history file.
    """

    return clear_prediction_history()


# ==========================================================
# Application Information
# ==========================================================

def application_information():
    """
    Returns project information.
    """

    return {
        "project": "Live Stock Analysis & Prediction",
        "version": "2.0",
        "language": "Python 3.12",
        "framework": "Streamlit",
        "prediction_model": "Random Forest + LSTM",
    }


# ==========================================================
# Public Functions
# ==========================================================

__all__ = [

    # Date & Time
    "current_date",
    "current_time",

    # Formatting
    "format_currency",
    "format_percentage",

    # Prediction
    "generate_signal",
    "save_prediction_history",
    "load_prediction_history",
    "clear_prediction_history",
    "latest_prediction",
    "prediction_count",

    # Recommendation
    "recommendation",
    "rsi_signal",
    "macd_signal",
    "moving_average_signal",
    "technical_signal",

    # Validation
    "safe_float",
    "is_valid_number",

    # Portfolio
    "calculate_profit_loss",

    # Export
    "export_prediction_history",
    "reset_prediction_history",

    # Info
    "application_information"
]