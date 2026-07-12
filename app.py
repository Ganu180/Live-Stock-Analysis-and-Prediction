import streamlit as st
import pandas as pd
import yfinance as yf
import os
from streamlit_autorefresh import st_autorefresh

EMAIL = st.secrets["EMAIL_ADDRESS"]
PASSWORD = st.secrets["EMAIL_APP_PASSWORD"]

# Visualization
from src.visualization import (
    closing_chart,
    candlestick_chart,
    volume_chart,
    moving_average_chart,
    rsi_chart,
    macd_chart,
    bollinger_chart
)

# Indicators
from src.indicators import calculate_indicators

# Prediction
from src.prediction import predict_next_price

# Company Information
from src.company_info import (
    get_company_info,
    company_dataframe
)

# News
from src.news import get_stock_news

# Portfolio
from src.portfolio import (
    add_stock,
    portfolio_summary,
    initialize_portfolio
)

# Utilities
from src.utils import (
    current_date,
    current_time,
    generate_signal,
    save_prediction_history,
    load_prediction_history,
    format_currency,
    recommendation,
    rsi_signal,
    macd_signal,
    moving_average_signal
)

# Email_alerts
from src.email_alert import (
    save_alert,
    load_alerts,
    delete_alert,
    validate_email,
    get_alert_types,
    check_alerts
)


# ---------------------------------------
# Page Configuration
# ---------------------------------------

st.set_page_config(
    page_title="Live Stock Market Analysis & Prediction",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------
# Auto Refresh
# ---------------------------------------

st_autorefresh(
    interval=60000,
    key="refresh"
)

# ---------------------------------------
# Title
# ---------------------------------------

st.title("📈 Live Stock Market Analysis & Prediction")

st.markdown(
"""
Analyze live market data using Machine Learning,
technical indicators and interactive dashboards.
"""
)

# ---------------------------------------
# Sidebar
# ---------------------------------------

st.sidebar.title("⚙ Settings")

ticker = st.sidebar.text_input(
    "Stock Symbol",
    value="HDFCBANK.NS"
)

period = st.sidebar.selectbox(
    "Historical Data",
    [
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y"
    ],
    index=2
)

refresh = st.sidebar.button("🔄 Refresh Data")

# ---------------------------------------
# Download Data
# ---------------------------------------

with st.spinner("Downloading stock data..."):

    df = yf.download(
        ticker,
        period=period,
        auto_adjust=True,
        progress=False
    )

# ---------------------------------------
# Fix MultiIndex
# ---------------------------------------

if isinstance(df.columns, pd.MultiIndex):

    df.columns = df.columns.get_level_values(0)

df = df.loc[:, ~df.columns.duplicated()]

if df.empty:

    st.error("Unable to download stock data.")

    st.stop()

# ---------------------------------------
# Calculate Indicators
# ---------------------------------------

df = calculate_indicators(df)

# ---------------------------------------
# Latest Values
# ---------------------------------------

latest = df.iloc[-1]

current_price = float(latest["Close"])

high_price = float(latest["High"])

low_price = float(latest["Low"])

volume = int(latest["Volume"])

# ---------------------------------------
# Tabs
# ---------------------------------------

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "📊 Overview",
        "📈 Indicators",
        "🤖 Prediction",
        "🏢 Company",
        "📰 News",
        "💼 Portfolio",
        "📧 Email Alerts"
    ]
)
# ==========================================================
# TAB 1 : OVERVIEW
# ==========================================================

with tab1:

    st.header("📊 Live Market Overview")

    st.success(f"Showing live data for **{ticker}**")

    # ----------------------------------------------------
    # KPI Cards
    # ----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Current Price",
        f"₹ {current_price:.2f}"
    )

    col2.metric(
        "Today's High",
        f"₹ {high_price:.2f}"
    )

    col3.metric(
        "Today's Low",
        f"₹ {low_price:.2f}"
    )

    col4.metric(
        "Volume",
        f"{volume:,}"
    )

    st.divider()

    # ----------------------------------------------------
    # Historical Data
    # ----------------------------------------------------

    st.subheader("Recent Historical Data")

    st.dataframe(
        df.tail(10),
        use_container_width=True
    )

    st.divider()

    # ----------------------------------------------------
    # Closing Price Chart
    # ----------------------------------------------------

    st.subheader("📈 Closing Price")

    try:

        fig = closing_chart(df)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    except Exception as e:

        st.error(e)

    st.divider()

    # ----------------------------------------------------
    # Candlestick Chart
    # ----------------------------------------------------

    st.subheader("🕯 Candlestick Chart")

    try:

        fig = candlestick_chart(df)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    except Exception as e:

        st.error(e)

    st.divider()

    # ----------------------------------------------------
    # Volume Chart
    # ----------------------------------------------------

    st.subheader("📊 Trading Volume")

    try:

        fig = volume_chart(df)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    except Exception as e:

        st.error(e)

    st.divider()

    # ----------------------------------------------------
    # Moving Average
    # ----------------------------------------------------

    st.subheader("📉 Moving Average")

    try:

        fig = moving_average_chart(df)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    except Exception as e:

        st.error(e)

    st.divider()

    # ----------------------------------------------------
    # Latest Indicator Values
    # ----------------------------------------------------

    st.subheader("Latest Technical Indicators")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "SMA20",
        f"{latest['SMA20']:.2f}"
    )

    c2.metric(
        "SMA50",
        f"{latest['SMA50']:.2f}"
    )

    c3.metric(
        "EMA20",
        f"{latest['EMA20']:.2f}"
    )

    c4.metric(
        "RSI",
        f"{latest['RSI']:.2f}"
    )

    c5, c6, c7 = st.columns(3)

    c5.metric(
        "MACD",
        f"{latest['MACD']:.2f}"
    )

    c6.metric(
        "Signal",
        f"{latest['MACD_Signal']:.2f}"
    )

    c7.metric(
        "ATR",
        f"{latest['ATR']:.2f}"
    )

    st.divider()

    # ----------------------------------------------------
    # Summary
    # ----------------------------------------------------

    st.subheader("Market Summary")

    st.write(f"**Current Closing Price:** ₹ {current_price:.2f}")

    st.write(f"**Highest Price Today:** ₹ {high_price:.2f}")

    st.write(f"**Lowest Price Today:** ₹ {low_price:.2f}")

    st.write(f"**Trading Volume:** {volume:,}")

    st.write(f"**Historical Records:** {len(df)}")
    # ==========================================================
# TAB 2 : TECHNICAL INDICATORS
# ==========================================================

with tab2:

    st.header("📈 Technical Indicators Dashboard")

    st.write(
        "Analyze the stock using technical indicators such as RSI, MACD, "
        "Bollinger Bands and Moving Averages."
    )

    # -----------------------------------------------------
    # RSI Chart
    # -----------------------------------------------------

    st.subheader("📊 Relative Strength Index (RSI)")

    try:

        fig = rsi_chart(df)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    except Exception as e:

        st.error(e)

    st.divider()

    # -----------------------------------------------------
    # MACD Chart
    # -----------------------------------------------------

    st.subheader("📈 MACD")

    try:

        fig = macd_chart(df)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    except Exception as e:

        st.error(e)

    st.divider()

    # -----------------------------------------------------
    # Bollinger Bands
    # -----------------------------------------------------

    st.subheader("📉 Bollinger Bands")

    try:

        fig = bollinger_chart(df)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    except Exception as e:

        st.error(e)

    st.divider()

    # -----------------------------------------------------
    # Indicator Values
    # -----------------------------------------------------

    st.subheader("Latest Indicator Values")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "RSI",
        f"{latest['RSI']:.2f}"
    )

    c2.metric(
        "MACD",
        f"{latest['MACD']:.2f}"
    )

    c3.metric(
        "MACD Signal",
        f"{latest['MACD_Signal']:.2f}"
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "Upper Band",
        f"{latest['BB_High']:.2f}"
    )

    c5.metric(
        "Middle Band",
        f"{latest['BB_Middle']:.2f}"
    )

    c6.metric(
        "Lower Band",
        f"{latest['BB_Low']:.2f}"
    )

    st.divider()

    # -----------------------------------------------------
    # Indicator Status
    # -----------------------------------------------------

    st.subheader("Indicator Analysis")

    rsi_status = rsi_signal(
        latest["RSI"]
    )

    macd_status = macd_signal(
        latest["MACD"],
        latest["MACD_Signal"]
    )

    ma_status = moving_average_signal(
        latest["SMA20"],
        latest["SMA50"]
    )

    col1, col2, col3 = st.columns(3)

    if rsi_status == "Oversold":
        col1.success(f"RSI : {rsi_status}")

    elif rsi_status == "Overbought":
        col1.error(f"RSI : {rsi_status}")

    else:
        col1.info(f"RSI : {rsi_status}")

    if macd_status == "Bullish":
        col2.success(f"MACD : {macd_status}")

    else:
        col2.error(f"MACD : {macd_status}")

    if ma_status == "Bullish":
        col3.success(f"Moving Average : {ma_status}")

    else:
        col3.error(f"Moving Average : {ma_status}")

    st.divider()

    # -----------------------------------------------------
    # Interpretation
    # -----------------------------------------------------

    st.subheader("Technical Interpretation")

    if latest["RSI"] > 70:

        st.warning(
            "RSI is above 70. "
            "The stock may be overbought."
        )

    elif latest["RSI"] < 30:

        st.success(
            "RSI is below 30. "
            "The stock may be oversold."
        )

    else:

        st.info(
            "RSI is in the normal trading range."
        )

    if latest["MACD"] > latest["MACD_Signal"]:

        st.success(
            "MACD is above the Signal Line. "
            "Bullish momentum detected."
        )

    else:

        st.warning(
            "MACD is below the Signal Line. "
            "Bearish momentum detected."
        )

    if latest["Close"] > latest["BB_High"]:

        st.warning(
            "Price is trading above the Upper Bollinger Band."
        )

    elif latest["Close"] < latest["BB_Low"]:

        st.success(
            "Price is trading below the Lower Bollinger Band."
        )

    else:

        st.info(
            "Price is trading within the Bollinger Bands."
        )

    st.divider()

    # -----------------------------------------------------
    # Overall Recommendation
    # -----------------------------------------------------

    st.subheader("Overall Technical Recommendation")

    tech_recommendation = recommendation(
        "HOLD",
        rsi_status,
        macd_status,
        ma_status
    )

    if tech_recommendation == "STRONG BUY":

        st.success("🟢 STRONG BUY")

    elif tech_recommendation == "BUY":

        st.success("🟢 BUY")

    elif tech_recommendation == "HOLD":

        st.warning("🟡 HOLD")

    elif tech_recommendation == "SELL":

        st.error("🔴 SELL")

    else:

        st.error("🔴 STRONG SELL")
# ==========================================================
# TAB 3 : PREDICTION
# ==========================================================

with tab3:

    st.header("🤖 Stock Price Prediction")

    st.write(
        "Predict tomorrow's closing price using the trained Machine Learning model."
    )

    st.divider()

    # --------------------------------------------
    # Current Market Information
    # --------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Current Price",
        f"₹ {current_price:.2f}"
    )

    c2.metric(
        "Today's High",
        f"₹ {high_price:.2f}"
    )

    c3.metric(
        "Today's Low",
        f"₹ {low_price:.2f}"
    )

    c4.metric(
        "Volume",
        f"{volume:,}"
    )

    st.divider()

    predict_button = st.button(
        "🚀 Predict Tomorrow Price",
        use_container_width=True
    )

    if predict_button:

        try:

            # -----------------------------------------
            # Random Forest Prediction
            # -----------------------------------------

            predicted_price = predict_next_price(df)

            predicted_price = float(predicted_price)

            difference = predicted_price - current_price

            expected_return = (
                difference / current_price
            ) * 100

            signal, percentage = generate_signal(
                current_price,
                predicted_price
            )

            save_prediction_history(
                ticker,
                current_price,
                predicted_price,
                signal
            )

            st.success("Prediction Completed Successfully!")

            st.divider()

            # -----------------------------------------
            # Prediction Metrics
            # -----------------------------------------

            p1, p2, p3, p4 = st.columns(4)

            p1.metric(
                "Current Price",
                f"₹ {current_price:.2f}"
            )

            p2.metric(
                "Predicted Price",
                f"₹ {predicted_price:.2f}"
            )

            p3.metric(
                "Price Difference",
                f"₹ {difference:.2f}"
            )

            p4.metric(
                "Expected Return",
                f"{expected_return:.2f}%"
            )

            st.divider()

            # -----------------------------------------
            # Recommendation
            # -----------------------------------------

            st.subheader("Recommendation")

            if signal == "BUY":

                st.success(
                    "🟢 BUY\n\n"
                    "The model predicts an upward movement."
                )

            elif signal == "SELL":

                st.error(
                    "🔴 SELL\n\n"
                    "The model predicts a downward movement."
                )

            else:

                st.warning(
                    "🟡 HOLD\n\n"
                    "The predicted movement is very small."
                )

            st.divider()

            # -----------------------------------------
            # Prediction Comparison
            # -----------------------------------------

            comparison = pd.DataFrame({

                "Category": [
                    "Current Price",
                    "Predicted Price"
                ],

                "Price": [
                    current_price,
                    predicted_price
                ]

            })

            st.subheader("Prediction Comparison")

            st.bar_chart(
                comparison.set_index("Category")
            )

            st.divider()

            # -----------------------------------------
            # Technical Summary
            # -----------------------------------------

            st.subheader("Technical Summary")

            st.write(f"**RSI:** {latest['RSI']:.2f}")

            st.write(f"**MACD:** {latest['MACD']:.2f}")

            st.write(f"**MACD Signal:** {latest['MACD_Signal']:.2f}")

            st.write(f"**SMA20:** {latest['SMA20']:.2f}")

            st.write(f"**SMA50:** {latest['SMA50']:.2f}")

            st.write(f"**ATR:** {latest['ATR']:.2f}")

            st.divider()

            # -----------------------------------------
            # Prediction Details
            # -----------------------------------------

            st.subheader("Prediction Details")

            st.info(
                f"""
Stock : {ticker}

Current Price : ₹ {current_price:.2f}

Predicted Tomorrow Price : ₹ {predicted_price:.2f}

Expected Return : {expected_return:.2f} %

Signal : {signal}
"""
            )

        except Exception as e:

            st.error(
                f"Prediction Error : {e}"
            )

    else:

        st.info(
            "Click the button above to generate a prediction."
        )
from src.company_info import get_company_info, company_dataframe
# ==========================================================
# TAB 4 : COMPANY INFORMATION
# ==========================================================

with tab4:

    st.header("🏢 Company Information")

    try:

        company = get_company_info(ticker)

        # --------------------------------------------------
        # Error Check
        # --------------------------------------------------

        if "Error" in company:

            st.error(company["Error"])

        else:

            st.success(
                f"Company Profile : {company['Company Name']}"
            )

            st.divider()

            # --------------------------------------------------
            # Basic Information
            # --------------------------------------------------

            c1, c2 = st.columns(2)

            with c1:

                st.subheader("Basic Details")

                st.write(
                    "**Company Name:**",
                    company["Company Name"]
                )

                st.write(
                    "**Stock Symbol:**",
                    company["Symbol"]
                )

                st.write(
                    "**Sector:**",
                    company["Sector"]
                )

                st.write(
                    "**Industry:**",
                    company["Industry"]
                )

                st.write(
                    "**Country:**",
                    company["Country"]
                )

                st.write(
                    "**City:**",
                    company["City"]
                )

            with c2:

                st.subheader("Trading Details")

                st.write(
                    "**Current Price:**",
                    company["Current Price"]
                )

                st.write(
                    "**Previous Close:**",
                    company["Previous Close"]
                )

                st.write(
                    "**Open:**",
                    company["Open"]
                )

                st.write(
                    "**Day High:**",
                    company["Day High"]
                )

                st.write(
                    "**Day Low:**",
                    company["Day Low"]
                )

            st.divider()

            # --------------------------------------------------
            # Financial Metrics
            # --------------------------------------------------

            st.subheader("Financial Metrics")

            m1, m2, m3 = st.columns(3)

            m1.metric(
                "Market Cap",
                company["Market Cap"]
            )

            m2.metric(
                "P/E Ratio",
                company["P/E Ratio"]
            )

            m3.metric(
                "EPS",
                company["EPS"]
            )

            m4, m5, m6 = st.columns(3)

            m4.metric(
                "Dividend Yield",
                company["Dividend Yield"]
            )

            m5.metric(
                "Dividend Rate",
                company["Dividend Rate"]
            )

            m6.metric(
                "Beta",
                company["Beta"]
            )

            st.divider()

            # --------------------------------------------------
            # 52 Week Statistics
            # --------------------------------------------------

            st.subheader("52 Week Statistics")

            w1, w2 = st.columns(2)

            w1.metric(
                "52 Week High",
                company["52 Week High"]
            )

            w2.metric(
                "52 Week Low",
                company["52 Week Low"]
            )

            st.divider()

            # --------------------------------------------------
            # Volume Information
            # --------------------------------------------------

            st.subheader("Volume")

            v1, v2 = st.columns(2)

            v1.metric(
                "Today's Volume",
                company["Volume"]
            )

            v2.metric(
                "Average Volume",
                company["Average Volume"]
            )

            st.divider()

            # --------------------------------------------------
            # Employees
            # --------------------------------------------------

            st.subheader("Organization")

            o1, o2 = st.columns(2)

            o1.metric(
                "Employees",
                company["Employees"]
            )

            o2.metric(
                "Currency",
                company["Currency"]
            )

            st.write(
                "**Exchange:**",
                company["Exchange"]
            )

            st.write(
                "**Website:**",
                company["Website"]
            )

            st.divider()

            # --------------------------------------------------
            # Company Summary
            # --------------------------------------------------

            st.subheader("Business Summary")

            st.write(
                company["Business Summary"]
            )

            st.divider()

            # --------------------------------------------------
            # Complete Information Table
            # --------------------------------------------------

            st.subheader("Complete Company Information")

            st.dataframe(
                company_dataframe(company),
                use_container_width=True,
                hide_index=True
            )

    except Exception as e:

        st.error(f"Error : {e}")

from src.news import get_stock_news
# ==========================================================
# TAB 5 : FINANCIAL NEWS
# ==========================================================

with tab5:

    st.header("📰 Latest Financial News")

    st.write(
        "Latest news related to the selected company."
    )

    st.divider()

    try:

        # ------------------------------------------
        # Fetch News
        # ------------------------------------------

        news_df = get_stock_news(ticker)

        if news_df.empty:

            st.warning(
                "No recent news found."
            )

        else:

            st.success(
                f"Showing {len(news_df)} latest articles."
            )

            st.divider()

            # ------------------------------------------
            # Display News
            # ------------------------------------------

            for index, row in news_df.iterrows():

                st.subheader(row["Title"])

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        "**Source:**",
                        row["Source"]
                    )

                with col2:

                    st.write(
                        "**Published:**",
                        row["Published"]
                    )

                if row["Author"]:

                    st.write(
                        "**Author:**",
                        row["Author"]
                    )

                if row["Description"]:

                    st.write(row["Description"])

                if row["URL"]:

                    st.markdown(
                        f"[📖 Read Full Article]({row['URL']})"
                    )

                st.divider()

            # ------------------------------------------
            # News Table
            # ------------------------------------------

            st.subheader("News Summary")

            st.dataframe(
                news_df[
                    [
                        "Title",
                        "Source",
                        "Published"
                    ]
                ],
                use_container_width=True
            )

            # ------------------------------------------
            # Download News
            # ------------------------------------------

            csv = news_df.to_csv(index=False)

            st.download_button(

                label="📥 Download News CSV",

                data=csv,

                file_name=f"{ticker}_news.csv",

                mime="text/csv"

            )

    except Exception as e:

        st.error(f"News Error : {e}")

from src.portfolio import (
    initialize_portfolio,
    add_stock,
    delete_stock,
    portfolio_summary
)
# ==========================================================
# TAB 6 : PORTFOLIO TRACKER
# ==========================================================

with tab6:

    st.header("💼 Portfolio Tracker")

    initialize_portfolio()

    st.write(
        "Track your stock investments with live market prices."
    )

    st.divider()

    # --------------------------------------------------
    # Add Stock
    # --------------------------------------------------

    st.subheader("➕ Add New Stock")

    c1, c2, c3 = st.columns(3)

    with c1:

        portfolio_stock = st.text_input(
            "Stock Symbol",
            value=ticker,
            key="portfolio_stock"
        )

    with c2:

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=10
        )

    with c3:

        buy_price = st.number_input(
            "Buy Price",
            min_value=0.0,
            value=float(current_price)
        )

    if st.button(
        "Add to Portfolio",
        use_container_width=True
    ):

        add_stock(
            portfolio_stock,
            quantity,
            buy_price
        )

        st.success(
            "Stock added successfully!"
        )

        st.rerun()

    st.divider()

    # --------------------------------------------------
    # Portfolio Summary
    # --------------------------------------------------

    portfolio_df, investment, value, profit = portfolio_summary()

    if portfolio_df.empty:

        st.info("Portfolio is empty.")

    else:

        st.subheader("📊 Portfolio Summary")

        p1, p2, p3 = st.columns(3)

        p1.metric(
            "Investment",
            f"₹ {investment:,.2f}"
        )

        p2.metric(
            "Current Value",
            f"₹ {value:,.2f}"
        )

        p3.metric(
            "Profit / Loss",
            f"₹ {profit:,.2f}"
        )

        st.divider()

        st.subheader("📋 Holdings")

        st.dataframe(
            portfolio_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # ----------------------------------------------
        # Portfolio Download
        # ----------------------------------------------

        csv = portfolio_df.to_csv(index=False)

        st.download_button(

            label="📥 Download Portfolio",

            data=csv,

            file_name="portfolio.csv",

            mime="text/csv"

        )

        st.divider()

        # ----------------------------------------------
        # Delete Stock
        # ----------------------------------------------

        st.subheader("🗑 Delete Stock")

        delete_index = st.selectbox(

            "Select Row",

            portfolio_df.index

        )

        if st.button("Delete Selected Stock"):

            delete_stock(delete_index)

            st.success("Stock Deleted Successfully")

            st.rerun()

        st.divider()

        # ----------------------------------------------
        # Portfolio Pie Chart
        # ----------------------------------------------

        st.subheader("🥧 Portfolio Distribution")

        pie_data = portfolio_df.groupby(
            "Stock"
        )["Investment"].sum()

        st.pyplot(
            pie_data.plot.pie(
                autopct="%1.1f%%",
                ylabel=""
            ).figure
        )

        st.divider()

        # ----------------------------------------------
        # Profit Chart
        # ----------------------------------------------

        st.subheader("📈 Profit / Loss")

        profit_chart = portfolio_df.set_index(
            "Stock"
        )["Profit/Loss"]

        st.bar_chart(profit_chart)

# ==========================================================
# TAB 7 : EMAIL ALERTS
# ==========================================================

with tab7:

    st.header("📧 Stock Email Alerts")

    st.write("Create price or signal alerts for your selected stock.")

    st.divider()

    email = st.text_input("Receiver Email")

    alert_type = st.selectbox(
        "Alert Type",
        get_alert_types()
    )

    target_price = st.number_input(
        "Target Price",
        min_value=0.0,
        value=float(current_price)
    )

    if st.button("Save Alert"):

        if validate_email(email):

            save_alert(
                email=email,
                ticker=ticker,
                alert_type=alert_type,
                target_price=target_price
            )

            st.success("Alert Saved Successfully!")

        else:

            st.error("Invalid Email Address")

    st.divider()

    st.subheader("Saved Alerts")

    alerts = load_alerts()

    if alerts.empty:

        st.info("No Alerts Found")

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

            st.success("Alert Deleted Successfully")

            st.rerun()

signal = "HOLD"

check_alerts(
    ticker=ticker,
    current_price=current_price,
    signal=signal,
    sender_email=os.getenv("iamganeshgokhale180@gmail.com"),
    app_password=os.getenv("cbxl cefy pmtc ybjr")
)            

# ==========================================================
# PREDICTION HISTORY
# ==========================================================

st.divider()

st.header("📜 Prediction History")

history = load_prediction_history()

if history.empty:

    st.info("No prediction history available.")

else:

    st.dataframe(
        history,
        use_container_width=True,
        hide_index=True
    )

    csv = history.to_csv(index=False)

    st.download_button(

        label="📥 Download Prediction History",

        data=csv,

        file_name="prediction_history.csv",

        mime="text/csv"

    )

# ==========================================================
# SIDEBAR INFORMATION
# ==========================================================

st.sidebar.divider()

st.sidebar.header("📊 Live Information")

st.sidebar.metric(

    "Current Price",

    f"₹ {current_price:.2f}"

)

st.sidebar.metric(

    "Today's High",

    f"₹ {high_price:.2f}"

)

st.sidebar.metric(

    "Today's Low",

    f"₹ {low_price:.2f}"

)

st.sidebar.metric(

    "Volume",

    f"{volume:,}"

)

st.sidebar.divider()

st.sidebar.subheader("Technical Indicators")

st.sidebar.write(

    f"RSI : {latest['RSI']:.2f}"

)

st.sidebar.write(

    f"MACD : {latest['MACD']:.2f}"

)

st.sidebar.write(

    f"SMA20 : {latest['SMA20']:.2f}"

)

st.sidebar.write(

    f"SMA50 : {latest['SMA50']:.2f}"

)

st.sidebar.divider()

# ==========================================================
# DATA DOWNLOAD
# ==========================================================

st.header("⬇ Download Data")

download_df = df.copy()

csv = download_df.to_csv().encode("utf-8")

st.download_button(

    label="📥 Download Historical Stock Data",

    data=csv,

    file_name=f"{ticker}_historical_data.csv",

    mime="text/csv"

)

# ==========================================================
# DATASET INFORMATION
# ==========================================================

st.divider()

st.header("📊 Dataset Information")

c1, c2, c3 = st.columns(3)

c1.metric(

    "Rows",

    len(df)

)

c2.metric(

    "Columns",

    len(df.columns)

)

c3.metric(

    "Missing Values",

    int(df.isnull().sum().sum())

)

st.write("Columns Available")

st.write(list(df.columns))

# ==========================================================
# LAST UPDATED
# ==========================================================

st.divider()

st.info(

    f"""
Last Updated

Date : {current_date()}

Time : {current_time()}

Stock : {ticker}
"""
)


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.markdown(
"""
---
### 📈 Live Stock Analysis & Prediction

Developed using:

- Streamlit
- Python
- Plotly
- yfinance
- Machine Learning
- Technical Indicators
- Random Forest
- LSTM
- Pandas
- NumPy

Features Included

✅ Live Stock Price

✅ Candlestick Chart

✅ Technical Indicators

✅ Company Information

✅ Financial News

✅ Portfolio Tracker

✅ Machine Learning Prediction

✅ Prediction History

✅ CSV Download

© 2026 Ganesh Gokhale
"""
)
