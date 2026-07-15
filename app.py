# ==========================================================
# LIVE STOCK ANALYSIS & PREDICTION
# Author : Ganesh Gokhale
# ==========================================================

# -----------------------------
# Standard Libraries
# -----------------------------
import os
import warnings
from datetime import datetime

# -----------------------------
# Data Handling
# -----------------------------
import numpy as np
import pandas as pd

# -----------------------------
# Streamlit
# -----------------------------
import streamlit as st

# -----------------------------
# Visualization
# -----------------------------
import plotly.graph_objects as go

# -----------------------------
# Stock Data
# -----------------------------
import yfinance as yf

# -----------------------------
# Machine Learning
# -----------------------------
import joblib

try:
    import tensorflow as tf
    load_model = tf.keras.models.load_model
    TENSORFLOW_AVAILABLE = True
except Exception:
    TENSORFLOW_AVAILABLE = False

# -----------------------------
# Project Modules
# -----------------------------
from src.indicators import calculate_indicators

from src.visualization import (
    candlestick_chart,
    rsi_chart,
    macd_chart,
    bollinger_chart,
    volume_chart
)

from src.company_info import company_report

from src.news import get_stock_news

from src.portfolio import (
    load_portfolio,
    add_stock,
    remove_stock,
    portfolio_summary,
)

from src.ai_recommendation import generate_recommendation

from src.pdf_report import create_pdf_report

from src.email_alert import (
    save_alert,
    load_alerts,
    delete_alert,
    check_alerts,
    validate_email,
    get_alert_types
)

from src.utils import (
    save_prediction_history,
    load_prediction_history,
    format_currency,
    format_percentage
)

warnings.filterwarnings("ignore")

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Live Stock Analysis & Prediction",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# STREAMLIT SECRETS
# ==========================================================

EMAIL = st.secrets.get("EMAIL_ADDRESS", "")
PASSWORD = st.secrets.get("EMAIL_APP_PASSWORD", "")
NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", "")

# ==========================================================
# LOAD MODELS
# ==========================================================

rf_model = None
lstm_model = None

try:
    rf_model = joblib.load("models/random_forest.pkl")
except Exception:
    pass

if TENSORFLOW_AVAILABLE:

    try:
        lstm_model = load_model("models/lstm_model.keras")
    except Exception:
        lstm_model = None

# ==========================================================
# TITLE
# ==========================================================

st.title("📈 Live Stock Analysis & Prediction System")

st.caption(
    "Real-time Stock Analysis using Technical Indicators, "
    "Machine Learning and Interactive Visualizations"
)

st.divider()

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("⚙️ Settings")

stock_list = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "LT.NS",
    "ITC.NS",
    "AXISBANK.NS",
    "BHARTIARTL.NS"
]

ticker = st.sidebar.selectbox(
    "Select Stock",
    stock_list,
    index=3
)

period = st.sidebar.selectbox(
    "Historical Period",
    [
        "6mo",
        "1y",
        "2y",
        "5y"
    ],
    index=2
)

interval = st.sidebar.selectbox(
    "Interval",
    [
        "1d",
        "1wk",
        "1mo"
    ]
)

auto_refresh = st.sidebar.checkbox(
    "Auto Refresh (60 sec)",
    value=False
)

if auto_refresh:

    from streamlit_autorefresh import st_autorefresh

    st_autorefresh(
        interval=60000,
        key="stock_refresh"
    )

st.sidebar.divider()

st.sidebar.markdown("### ℹ️ Selected Stock")

st.sidebar.success(ticker)
# ==========================================================
# DOWNLOAD STOCK DATA
# ==========================================================

ticker = ticker.strip().upper()

if ticker == "":
    st.error("Please select a valid stock.")
    st.stop()

with st.spinner("Downloading latest stock data..."):

    try:

        df = yf.download(
            tickers=ticker,
            period=period,
            interval=interval,
            auto_adjust=True,
            progress=False,
            threads=False
        )

    except Exception as e:

        st.error(f"Unable to download stock data.\n\n{e}")
        st.stop()

# ==========================================================
# VALIDATE DATA
# ==========================================================

if df is None or df.empty:

    st.error(f"No stock data found for **{ticker}**")
    st.stop()

# ==========================================================
# HANDLE MULTIINDEX FROM YFINANCE
# ==========================================================

if isinstance(df.columns, pd.MultiIndex):

    df.columns = df.columns.get_level_values(0)

# ==========================================================
# ENSURE REQUIRED COLUMNS
# ==========================================================

required_columns = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume"
]

missing = [
    col for col in required_columns
    if col not in df.columns
]

if missing:

    st.error(
        f"Missing required columns:\n\n{missing}"
    )

    st.stop()

# ==========================================================
# CONVERT TO NUMERIC
# ==========================================================

for col in required_columns:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

df = df.dropna()

if df.empty:

    st.error("No usable data after cleaning.")
    st.stop()

# ==========================================================
# CALCULATE TECHNICAL INDICATORS
# ==========================================================

try:

    df = calculate_indicators(df)

except Exception as e:

    st.warning(
        f"Unable to calculate some indicators.\n\n{e}"
    )

# ==========================================================
# LATEST DATA
# ==========================================================

latest = df.iloc[-1]

current_price = float(latest["Close"])

previous_close = float(df["Close"].iloc[-2]) if len(df) > 1 else current_price

price_change = current_price - previous_close

price_change_percent = (
    (price_change / previous_close) * 100
    if previous_close != 0
    else 0
)

# ==========================================================
# SAFE VALUE FUNCTION
# Prevents KeyError
# ==========================================================

def safe_value(column):

    if column not in df.columns:
        return None

    value = latest[column]

    if pd.isna(value):
        return None

    return float(value)

# ==========================================================
# INDICATOR VALUES
# ==========================================================

sma20 = safe_value("SMA20")
sma50 = safe_value("SMA50")
ema20 = safe_value("EMA20")
rsi = safe_value("RSI")

macd = safe_value("MACD")
macd_signal = safe_value("MACD_SIGNAL")

adx = safe_value("ADX")

bb_upper = safe_value("BB_UPPER")
bb_middle = safe_value("BB_MIDDLE")
bb_lower = safe_value("BB_LOWER")

# ==========================================================
# PRICE SIGNAL
# ==========================================================

if sma20 is not None and ema20 is not None:

    if current_price > sma20 and current_price > ema20:

        trend = "Bullish 📈"

    elif current_price < sma20 and current_price < ema20:

        trend = "Bearish 📉"

    else:

        trend = "Sideways ➖"

else:

    trend = "Not Available"

# ==========================================================
# COMPANY INFORMATION
# ==========================================================

try:

    company = company_report(ticker)

except Exception:

    company = {}

# ==========================================================
# NEWS
# ==========================================================

try:

    news = get_stock_news(
        ticker.replace(".NS", "")
    )

except Exception:

    news = []

# ==========================================================
# CREATE TABS
# ==========================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(
    [
        "📊 Dashboard",
        "📈 Charts",
        "🤖 Prediction",
        "🏢 Company",
        "📰 News",
        "💼 Portfolio",
        "📧 Alerts",
        "🧠 AI Recommendation",
        "📄 PDF Report",
        "📊 History"
    ]
)
# ==========================================================
# TAB 1 : DASHBOARD
# ==========================================================

with tab1:

    st.header("📊 Stock Dashboard")

    st.divider()

    # ======================================================
    # PRICE METRICS
    # ======================================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Current Price",
        f"₹{current_price:.2f}",
        f"{price_change:.2f}"
    )

    c2.metric(
        "Change %",
        f"{price_change_percent:.2f}%"
    )

    c3.metric(
        "Trend",
        trend
    )

    c4.metric(
        "Volume",
        f"{int(latest['Volume']):,}"
    )

    st.divider()

    # ======================================================
    # TECHNICAL INDICATORS
    # ======================================================

    st.subheader("Technical Indicators")

    i1, i2, i3, i4 = st.columns(4)

    i1.metric(
        "SMA 20",
        f"{sma20:.2f}" if sma20 is not None else "N/A"
    )

    i2.metric(
        "EMA 20",
        f"{ema20:.2f}" if ema20 is not None else "N/A"
    )

    i3.metric(
        "RSI",
        f"{rsi:.2f}" if rsi is not None else "N/A"
    )

    i4.metric(
        "ADX",
        f"{adx:.2f}" if adx is not None else "N/A"
    )

    st.divider()

    # ======================================================
    # MACD
    # ======================================================

    m1, m2 = st.columns(2)

    m1.metric(
        "MACD",
        f"{macd:.2f}" if macd is not None else "N/A"
    )

    m2.metric(
        "Signal Line",
        f"{macd_signal:.2f}" if macd_signal is not None else "N/A"
    )

    st.divider()

    # ======================================================
    # BOLLINGER BANDS
    # ======================================================

    st.subheader("Bollinger Bands")

    b1, b2, b3 = st.columns(3)

    b1.metric(
        "Upper Band",
        f"{bb_upper:.2f}" if bb_upper is not None else "N/A"
    )

    b2.metric(
        "Middle Band",
        f"{bb_middle:.2f}" if bb_middle is not None else "N/A"
    )

    b3.metric(
        "Lower Band",
        f"{bb_lower:.2f}" if bb_lower is not None else "N/A"
    )

    st.divider()

    # ======================================================
    # PRICE SUMMARY
    # ======================================================

    st.subheader("Today's Summary")

    summary = pd.DataFrame({

        "Metric": [

            "Open",

            "High",

            "Low",

            "Close",

            "Volume"

        ],

        "Value": [

            f"₹{latest['Open']:.2f}",

            f"₹{latest['High']:.2f}",

            f"₹{latest['Low']:.2f}",

            f"₹{latest['Close']:.2f}",

            f"{int(latest['Volume']):,}"

        ]

    })

    st.dataframe(

        summary,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ======================================================
    # COMPANY INFORMATION
    # ======================================================

    st.subheader("Company Information")

    if company:

        c1, c2 = st.columns(2)

        with c1:

            st.write("**Company** :", company.get("company_name", "N/A"))

            st.write("**Sector** :", company.get("sector", "N/A"))

            st.write("**Industry** :", company.get("industry", "N/A"))

            st.write("**Employees** :", company.get("employees", "N/A"))

        with c2:

            st.write("**Market Cap** :", company.get("market_cap", "N/A"))

            st.write("**P/E Ratio** :", company.get("pe_ratio", "N/A"))

            st.write("**Dividend Yield** :", company.get("dividend_yield", "N/A"))

            st.write("**52 Week Range** :", company.get("week_range", "N/A"))

    else:

        st.info("Company information is not available.")
# ==========================================================
# TAB 2 : CHARTS
# ==========================================================

with tab2:

    st.header("📈 Interactive Charts")

    st.divider()

    # ------------------------------------------------------
    # Chart Selection
    # ------------------------------------------------------

    chart_option = st.selectbox(
        "Select Chart",
        [
            "Candlestick",
            "Volume",
            "RSI",
            "MACD",
            "Bollinger Bands"
        ]
    )

    st.divider()

    # ------------------------------------------------------
    # Candlestick Chart
    # ------------------------------------------------------

    if chart_option == "Candlestick":

        st.subheader("Candlestick Chart")

        try:

            fig = candlestick_chart(df)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        except Exception as e:

            st.error(f"Unable to create chart.\n{e}")

    # ------------------------------------------------------
    # Volume Chart
    # ------------------------------------------------------

    elif chart_option == "Volume":

        st.subheader("Volume Chart")

        try:

            fig = volume_chart(df)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        except Exception as e:

            st.error(e)

    # ------------------------------------------------------
    # RSI Chart
    # ------------------------------------------------------

    elif chart_option == "RSI":

        st.subheader("Relative Strength Index")

        if "RSI" in df.columns:

            try:

                fig = rsi_chart(df)

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            except Exception as e:

                st.error(e)

        else:

            st.warning("RSI not available.")

    # ------------------------------------------------------
    # MACD Chart
    # ------------------------------------------------------

    elif chart_option == "MACD":

        st.subheader("MACD")

        if (
            "MACD" in df.columns
            and
            "MACD_SIGNAL" in df.columns
        ):

            try:

                fig = macd_chart(df)

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            except Exception as e:

                st.error(e)

        else:

            st.warning("MACD not available.")

    # ------------------------------------------------------
    # Bollinger Bands
    # ------------------------------------------------------

    elif chart_option == "Bollinger Bands":

        st.subheader("Bollinger Bands")

        if (
            "BB_UPPER" in df.columns
            and
            "BB_LOWER" in df.columns
        ):

            try:

                fig = bollinger_chart(df)

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            except Exception as e:

                st.error(e)

        else:

            st.warning("Bollinger Bands not available.")

    st.divider()

    # ------------------------------------------------------
    # Latest Technical Indicator Values
    # ------------------------------------------------------

    st.subheader("Latest Indicator Values")

    indicator_df = pd.DataFrame({

        "Indicator":[
            "SMA20",
            "EMA20",
            "RSI",
            "MACD",
            "MACD Signal",
            "ADX"
        ],

        "Value":[

            sma20,

            ema20,

            rsi,

            macd,

            macd_signal,

            adx

        ]

    })

    st.dataframe(

        indicator_df,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ------------------------------------------------------
    # Download Historical Data
    # ------------------------------------------------------

    csv = df.to_csv().encode("utf-8")

    st.download_button(

        "⬇ Download Historical Data",

        data=csv,

        file_name=f"{ticker}_history.csv",

        mime="text/csv"

    )
# ==========================================================
# TAB 3 : STOCK PREDICTION
# ==========================================================

with tab3:

    st.header("🤖 AI Stock Price Prediction")

    st.divider()

    st.write(
        "Predict the next closing price using trained Machine Learning models."
    )

    st.divider()

    # ------------------------------------------------------
    # Prepare Input Features
    # ------------------------------------------------------

    feature_names = [
        "Open",
        "High",
        "Low",
        "Volume",
        "SMA20",
        "EMA20",
        "RSI",
        "MACD",
        "ADX"
    ]

    features = {}

    for feature in feature_names:

        if feature in df.columns:

            value = latest.get(feature)

            if pd.isna(value):

                value = 0

        else:

            value = 0

        features[feature] = float(value)

    input_df = pd.DataFrame([features])

    st.subheader("Input Features")

    st.dataframe(
        input_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ------------------------------------------------------
    # Prediction Button
    # ------------------------------------------------------

    predict_btn = st.button(
        "🚀 Predict Next Closing Price",
        use_container_width=True
    )

    predicted_price = None
    lstm_prediction = None

    if predict_btn:

        # ==============================================
        # RANDOM FOREST
        # ==============================================

        if rf_model is not None:

            try:

                predicted_price = float(
                    rf_model.predict(input_df)[0]
                )

            except Exception as e:

                st.error(f"Random Forest Error\n\n{e}")

        else:

            st.warning("Random Forest model not found.")

        # ==============================================
        # LSTM
        # ==============================================

        if lstm_model is not None:

            try:

                close_prices = df["Close"].tail(60).values

                if len(close_prices) == 60:

                    x = close_prices.reshape(1, 60, 1)

                    lstm_prediction = float(
                        lstm_model.predict(
                            x,
                            verbose=0
                        )[0][0]
                    )

            except Exception as e:

                st.warning(f"LSTM Error\n\n{e}")

        st.divider()

        # ==============================================
        # DISPLAY PREDICTIONS
        # ==============================================

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Current Price",
            f"₹{current_price:.2f}"
        )

        if predicted_price is not None:

            col2.metric(
                "Random Forest",
                f"₹{predicted_price:.2f}",
                f"{predicted_price-current_price:.2f}"
            )

        if lstm_prediction is not None:

            col3.metric(
                "LSTM",
                f"₹{lstm_prediction:.2f}",
                f"{lstm_prediction-current_price:.2f}"
            )

        st.divider()

        # ==============================================
        # BUY / SELL / HOLD SIGNAL
        # ==============================================

        if predicted_price is not None:

            if predicted_price > current_price:

                signal = "BUY"

                st.success("🟢 BUY Signal")

            elif predicted_price < current_price:

                signal = "SELL"

                st.error("🔴 SELL Signal")

            else:

                signal = "HOLD"

                st.info("🟡 HOLD Signal")

            confidence = (
                abs(predicted_price-current_price)
                / current_price
            ) * 100

            st.metric(
                "Prediction Confidence",
                f"{confidence:.2f}%"
            )

            # ======================================
            # SAVE PREDICTION HISTORY
            # ======================================

            try:

                save_prediction_history(

                    ticker=ticker,

                    current_price=current_price,

                    predicted_price=predicted_price,

                    signal=signal

                )

            except Exception:

                pass

        st.divider()

        # ==============================================
        # EMAIL ALERT CHECK
        # ==============================================

        try:

            check_alerts(

                ticker=ticker,

                current_price=current_price,

                predicted_price=predicted_price,

                signal=signal

            )

        except Exception:

            pass            
# ==========================================================
# TAB 4 : COMPANY INFORMATION
# ==========================================================

with tab4:

    st.header("🏢 Company Information")

    st.divider()

    try:

        info = company_report(ticker)

        if info:

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("Basic Details")

                st.write("**Company Name:**", info.get("company_name", "N/A"))
                st.write("**Sector:**", info.get("sector", "N/A"))
                st.write("**Industry:**", info.get("industry", "N/A"))
                st.write("**Country:**", info.get("country", "N/A"))
                st.write("**Website:**", info.get("website", "N/A"))

            with col2:

                st.subheader("Market Statistics")

                st.write("**Market Cap:**", info.get("market_cap", "N/A"))
                st.write("**P/E Ratio:**", info.get("pe_ratio", "N/A"))
                st.write("**EPS:**", info.get("eps", "N/A"))
                st.write("**Dividend Yield:**", info.get("dividend_yield", "N/A"))
                st.write("**52 Week High:**", info.get("high_52week", "N/A"))
                st.write("**52 Week Low:**", info.get("low_52week", "N/A"))

            st.divider()

            st.subheader("Business Summary")

            st.write(
                info.get(
                    "description",
                    "Company description not available."
                )
            )

        else:

            st.warning("Company information is not available.")

    except Exception as e:

        st.error(f"Unable to load company information.\n\n{e}")


# ==========================================================
# TAB 5 : STOCK NEWS
# ==========================================================

with tab5:

    st.header("📰 Latest Stock News")

    st.divider()

    try:

        company_name = ticker.replace(".NS", "")

        news_list = get_stock_news(company_name)

        if len(news_list) == 0:

            st.info("No latest news available.")

        else:

            for article in news_list:

                st.subheader(article.get("title", "No Title"))

                st.write(article.get("description", ""))

                st.caption(
                    f"Source : {article.get('source', {}).get('name','Unknown')}"
                )

                st.write(
                    f"Published : {article.get('publishedAt','N/A')}"
                )

                if article.get("url"):

                    st.link_button(
                        "Read Full Article",
                        article["url"]
                    )

                st.divider()

    except Exception as e:

        st.error(f"Unable to fetch news.\n\n{e}")
# ==========================================================
# TAB 6 : PORTFOLIO MANAGEMENT
# ==========================================================

with tab6:

    st.header("💼 Portfolio Management")

    st.divider()

    # ======================================================
    # ADD STOCK
    # ======================================================

    st.subheader("Add Stock")

    col1, col2, col3 = st.columns(3)

    with col1:

        portfolio_ticker = st.selectbox(
            "Stock",
            stock_list,
            key="portfolio_stock"
        )

    with col2:

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1,
            step=1
        )

    with col3:

        buy_price = st.number_input(
            "Buy Price (₹)",
            min_value=0.0,
            value=float(current_price),
            step=1.0
        )

    if st.button("➕ Add to Portfolio"):

        try:

            add_stock(

                stock=portfolio_ticker,

                quantity=quantity,

                buy_price=buy_price

            )

            st.success("Stock added successfully!")

            st.rerun()

        except Exception as e:

            st.error(e)

    st.divider()

    # ======================================================
    # LOAD PORTFOLIO
    # ======================================================

    portfolio, total_investment, current_value, profit_loss, returns = portfolio_summary()

    if portfolio.empty:
       st.info("Portfolio is empty.")
    else:
       st.subheader("Portfolio Holdings")

    st.dataframe(
        portfolio,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==================================================
    # SUMMARY
    # ==================================================

    total_investment = portfolio["Investment"].sum()

    current_value = portfolio["Current Value"].sum()

    profit_loss = current_value - total_investment

    if total_investment != 0:
        returns = (profit_loss / total_investment) * 100
    else:
        returns = 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Investment",
        f"₹{total_investment:,.2f}"
    )

    c2.metric(
        "Current Value",
        f"₹{current_value:,.2f}"
    )

    c3.metric(
        "Profit / Loss",
        f"₹{profit_loss:,.2f}"
    )

    c4.metric(
        "Return",
        f"{returns:.2f}%"
    )

    st.divider()

    # ==================================================
    # PIE CHART
    # ==================================================

    st.subheader("Portfolio Allocation")

    fig = go.Figure(
        data=[
            go.Pie(
                labels=portfolio["Stock"],
                values=portfolio["Current Value"],
                hole=0.45
            )
        ]
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.divider()

    # ==================================================
    # REMOVE STOCK
    # ==================================================

    st.subheader("Remove Stock")

    delete_stock = st.selectbox(

        "Select Stock",

        portfolio["Ticker"].tolist()

    )

    if st.button("🗑 Remove Stock"):

        try:

            remove_stock(delete_stock)

            st.success("Stock removed.")

            st.rerun()

        except Exception as e:

                st.error(e)
# ==========================================================
# TAB 7 : EMAIL ALERTS
# ==========================================================

with tab7:

    st.header("📧 Email Alerts")

    st.write(
        "Create price alerts and receive email notifications."
    )

    st.divider()

    email = st.text_input(
        "Email Address"
    )

    alert_type = st.selectbox(
        "Alert Type",
        get_alert_types()
    )

    target_price = st.number_input(
        "Target Price",
        min_value=0.0,
        value=float(current_price),
        step=1.0
    )

    if st.button("Save Alert"):

        if validate_email(email):

            try:

                save_alert(

                    email=email,

                    ticker=ticker,

                    alert_type=alert_type,

                    target_price=target_price

                )

                st.success("Alert Saved Successfully!")

            except Exception as e:

                st.error(e)

        else:

            st.error("Please enter a valid email address.")

    st.divider()

    st.subheader("Saved Alerts")

    alerts = load_alerts()

    if alerts.empty:

        st.info("No alerts found.")

    else:

        st.dataframe(
            alerts,
            use_container_width=True,
            hide_index=True
        )

        delete_index = st.selectbox(
            "Delete Alert",
            alerts.index
        )

        if st.button("Delete Selected Alert"):

            delete_alert(delete_index)

            st.success("Alert Deleted Successfully.")

            st.rerun()

# ==========================================================
# AUTO CHECK EMAIL ALERTS
# ==========================================================

signal = "HOLD"

if predicted_price is not None:

    if predicted_price > current_price:

        signal = "BUY"

    elif predicted_price < current_price:

        signal = "SELL"

try:

    check_alerts(

        ticker=ticker,

        current_price=current_price,

        predicted_price=predicted_price,

        signal=signal

    )

except Exception:

    pass

# ==========================================================
# AI RECOMMENDATION
# ==========================================================

st.divider()

st.header("🧠 AI Recommendation")

try:

    recommendation = generate_recommendation(

        ticker=ticker,

        current_price=current_price,

        predicted_price=predicted_price,

        rsi=rsi,

        macd=macd,

        adx=adx

    )

    st.success(recommendation)

except Exception as e:

    st.warning("Unable to generate AI recommendation.")

    st.code(str(e))
# ==========================================================
# PDF REPORT
# ==========================================================

st.divider()

st.header("📄 Generate PDF Report")

if st.button("Generate Report"):

    try:

        report_data = {

            "ticker": ticker,
            "current_price": current_price,
            "predicted_price": predicted_price,
            "trend": trend,
            "rsi": rsi,
            "macd": macd,
            "adx": adx,
            "sma20": sma20,
            "ema20": ema20

        }

        pdf_path = create_pdf_report(report_data)

        with open(pdf_path, "rb") as file:

            st.download_button(

                label="⬇ Download PDF Report",

                data=file,

                file_name=f"{ticker}_Stock_Report.pdf",

                mime="application/pdf"

            )

        st.success("Report generated successfully!")

    except Exception as e:

        st.error(f"Unable to generate report.\n\n{e}")

# ==========================================================
# PREDICTION HISTORY
# ==========================================================

st.divider()

st.header("📊 Prediction History")

try:

    history = load_prediction_history()

    if history.empty:

        st.info("No prediction history available.")

    else:

        st.dataframe(

            history,

            use_container_width=True,

            hide_index=True

        )

        csv = history.to_csv(index=False).encode("utf-8")

        st.download_button(

            "⬇ Download Prediction History",

            data=csv,

            file_name="prediction_history.csv",

            mime="text/csv"

        )

except Exception as e:

    st.warning(str(e))
# ==========================================================
# PDF REPORT
# ==========================================================

st.divider()

st.header("📄 Generate PDF Report")

if st.button("Generate Report"):

    try:

        report_data = {

            "ticker": ticker,
            "current_price": current_price,
            "predicted_price": predicted_price,
            "trend": trend,
            "rsi": rsi,
            "macd": macd,
            "adx": adx,
            "sma20": sma20,
            "ema20": ema20

        }

        pdf_path = create_pdf_report(report_data)

        with open(pdf_path, "rb") as file:

            st.download_button(

                label="⬇ Download PDF Report",

                data=file,

                file_name=f"{ticker}_Stock_Report.pdf",

                mime="application/pdf"

            )

        st.success("Report generated successfully!")

    except Exception as e:

        st.error(f"Unable to generate report.\n\n{e}")

# ==========================================================
# PREDICTION HISTORY
# ==========================================================

st.divider()

st.header("📊 Prediction History")

try:

    history = load_prediction_history()

    if history.empty:

        st.info("No prediction history available.")

    else:

        st.dataframe(

            history,

            use_container_width=True,

            hide_index=True

        )

        csv = history.to_csv(index=False).encode("utf-8")

        st.download_button(

            "⬇ Download Prediction History",

            data=csv,

            file_name="prediction_history.csv",

            mime="text/csv"

        )

except Exception as e:

    st.warning(str(e)) 
# ==========================================================
# FINAL SECTION : ABOUT / FOOTER
# ==========================================================

st.divider()

with st.expander("ℹ About This Project", expanded=False):

    st.markdown("""
## Live Stock Analysis & Prediction

This project provides real-time stock market analysis using
Yahoo Finance data and Machine Learning.

### Features

- Live Stock Price
- Technical Indicators
- Candlestick Charts
- Company Information
- Latest News
- Random Forest Prediction
- Portfolio Management
- Email Alerts
- PDF Report Generation
- AI Recommendation

### Technologies

- Python
- Streamlit
- Pandas
- Plotly
- Scikit-learn
- TensorFlow (Optional)
- yFinance
- NewsAPI
- ReportLab

Developed by **Ganesh Gokhale**
""")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Ticker",
        ticker
    )

with col2:

    st.metric(
        "Rows Loaded",
        len(df)
    )

with col3:

    st.metric(
        "Last Close",
        f"₹{current_price:.2f}"
    )

st.divider()

st.caption(
    "© 2026 Live Stock Analysis & Prediction | Built using Streamlit"
)                            
