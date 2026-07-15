"""
==========================================================
Live Stock Analysis & Prediction
Visualization Module
Version : 2.0
==========================================================
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ==========================================================
# DEFAULT LAYOUT
# ==========================================================

DEFAULT_TEMPLATE = "plotly_white"
DEFAULT_HEIGHT = 500


# ==========================================================
# VALIDATION
# ==========================================================

def validate_dataframe(df, columns):

    if df is None:
        raise ValueError("DataFrame is None.")

    if df.empty:
        raise ValueError("DataFrame is empty.")

    missing = []

    for column in columns:

        if column not in df.columns:
            missing.append(column)

    if missing:

        raise ValueError(

            f"Missing columns: {', '.join(missing)}"

        )

    return True


# ==========================================================
# COMMON LAYOUT
# ==========================================================

def apply_layout(

    fig,

    title,

    x_title="Date",

    y_title="Price",

    height=DEFAULT_HEIGHT

):

    fig.update_layout(

        title=title,

        template=DEFAULT_TEMPLATE,

        height=height,

        hovermode="x unified",

        legend=dict(

            orientation="h",

            yanchor="bottom",

            y=1.02,

            xanchor="right",

            x=1

        ),

        margin=dict(

            l=40,

            r=30,

            t=60,

            b=40

        )

    )

    fig.update_xaxes(

        title=x_title,

        showgrid=True

    )

    fig.update_yaxes(

        title=y_title,

        showgrid=True

    )

    return fig


# ==========================================================
# CLOSING PRICE CHART
# ==========================================================

def closing_chart(df):

    validate_dataframe(

        df,

        ["Close"]

    )

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=df.index,

            y=df["Close"],

            mode="lines",

            line=dict(

                width=2

            ),

            name="Close Price"

        )

    )

    apply_layout(

        fig,

        "Closing Price"

    )

    return fig


# ==========================================================
# CANDLESTICK CHART
# ==========================================================

def candlestick_chart(df):

    validate_dataframe(

        df,

        [

            "Open",

            "High",

            "Low",

            "Close"

        ]

    )

    fig = go.Figure()

    fig.add_trace(

        go.Candlestick(

            x=df.index,

            open=df["Open"],

            high=df["High"],

            low=df["Low"],

            close=df["Close"],

            name="Candlestick"

        )

    )

    apply_layout(

        fig,

        "Candlestick Chart",

        height=650

    )

    fig.update_layout(

        xaxis_rangeslider_visible=True

    )

    return fig


# ==========================================================
# VOLUME CHART
# ==========================================================

def volume_chart(df):

    validate_dataframe(

        df,

        ["Volume"]

    )

    fig = go.Figure()

    fig.add_trace(

        go.Bar(

            x=df.index,

            y=df["Volume"],

            name="Volume"

        )

    )

    apply_layout(

        fig,

        "Trading Volume",

        y_title="Volume",

        height=350

    )

    return fig
# ==========================================================
# MOVING AVERAGE CHART
# ==========================================================

def moving_average_chart(df):

    validate_dataframe(
        df,
        ["Close", "SMA20", "SMA50", "EMA20"]
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["Close"],
            mode="lines",
            name="Close",
            line=dict(width=2)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["SMA20"],
            mode="lines",
            name="SMA 20"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["SMA50"],
            mode="lines",
            name="SMA 50"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["EMA20"],
            mode="lines",
            name="EMA 20"
        )
    )

    apply_layout(
        fig,
        "Moving Average Analysis"
    )

    return fig


# ==========================================================
# RSI CHART
# ==========================================================

def rsi_chart(df):

    validate_dataframe(
        df,
        ["RSI"]
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["RSI"],
            mode="lines",
            name="RSI"
        )
    )

    fig.add_hline(
        y=70,
        line_dash="dash",
        annotation_text="Overbought"
    )

    fig.add_hline(
        y=30,
        line_dash="dash",
        annotation_text="Oversold"
    )

    apply_layout(
        fig,
        "Relative Strength Index",
        y_title="RSI",
        height=400
    )

    fig.update_yaxes(
        range=[0, 100]
    )

    return fig


# ==========================================================
# MACD CHART
# ==========================================================

def macd_chart(df):

    validate_dataframe(
        df,
        ["MACD", "MACD_Signal"]
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["MACD"],
            mode="lines",
            name="MACD"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["MACD_Signal"],
            mode="lines",
            name="Signal"
        )
    )

    apply_layout(
        fig,
        "MACD Indicator",
        y_title="MACD",
        height=450
    )

    return fig


# ==========================================================
# BOLLINGER BANDS
# ==========================================================

def bollinger_chart(df):

    validate_dataframe(
        df,
        [
            "Close",
            "BB_High",
            "BB_Low"
        ]
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["Close"],
            mode="lines",
            name="Close"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["BB_High"],
            mode="lines",
            name="Upper Band"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["BB_Low"],
            mode="lines",
            fill="tonexty",
            name="Lower Band"
        )
    )

    apply_layout(
        fig,
        "Bollinger Bands"
    )

    return fig


# ==========================================================
# PRICE + VOLUME CHART
# ==========================================================

def price_volume_chart(df):

    validate_dataframe(
        df,
        [
            "Close",
            "Volume"
        ]
    )

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.7, 0.3]
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["Close"],
            name="Close"
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df["Volume"],
            name="Volume"
        ),
        row=2,
        col=1
    )

    fig.update_layout(
        template=DEFAULT_TEMPLATE,
        title="Price and Volume",
        height=700,
        hovermode="x unified"
    )

    return fig


# ==========================================================
# OHLC CHART
# ==========================================================

def ohlc_chart(df):

    validate_dataframe(
        df,
        [
            "Open",
            "High",
            "Low",
            "Close"
        ]
    )

    fig = go.Figure()

    fig.add_trace(
        go.Ohlc(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="OHLC"
        )
    )

    apply_layout(
        fig,
        "OHLC Chart",
        height=650
    )

    return fig
# ==========================================================
# DAILY RETURNS CHART
# ==========================================================

def daily_returns_chart(df):

    validate_dataframe(
        df,
        ["Close"]
    )

    returns = df["Close"].pct_change() * 100

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=df.index,

            y=returns,

            mode="lines",

            name="Daily Return (%)"

        )

    )

    apply_layout(

        fig,

        "Daily Returns",

        y_title="Return (%)"

    )

    return fig


# ==========================================================
# CUMULATIVE RETURNS
# ==========================================================

def cumulative_returns_chart(df):

    validate_dataframe(
        df,
        ["Close"]
    )

    cumulative = (

        (1 + df["Close"].pct_change())

        .cumprod()

        * 100

    )

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=df.index,

            y=cumulative,

            mode="lines",

            name="Cumulative Return"

        )

    )

    apply_layout(

        fig,

        "Cumulative Returns",

        y_title="Growth (%)"

    )

    return fig


# ==========================================================
# RETURN HISTOGRAM
# ==========================================================

def returns_histogram(df):

    validate_dataframe(
        df,
        ["Close"]
    )

    returns = df["Close"].pct_change().dropna()

    fig = go.Figure()

    fig.add_trace(

        go.Histogram(

            x=returns,

            nbinsx=40,

            name="Returns"

        )

    )

    apply_layout(

        fig,

        "Return Distribution",

        x_title="Daily Return",

        y_title="Frequency"

    )

    return fig


# ==========================================================
# PORTFOLIO ALLOCATION
# ==========================================================

def portfolio_allocation_chart(portfolio_df):

    validate_dataframe(

        portfolio_df,

        [

            "Ticker",

            "Investment"

        ]

    )

    fig = px.pie(

        portfolio_df,

        names="Ticker",

        values="Investment",

        title="Portfolio Allocation"

    )

    fig.update_layout(

        template=DEFAULT_TEMPLATE,

        height=550

    )

    return fig


# ==========================================================
# PORTFOLIO PERFORMANCE
# ==========================================================

def portfolio_performance_chart(portfolio_df):

    validate_dataframe(

        portfolio_df,

        [

            "Ticker",

            "Profit"

        ]

    )

    fig = px.bar(

        portfolio_df,

        x="Ticker",

        y="Profit",

        title="Portfolio Profit / Loss"

    )

    fig.update_layout(

        template=DEFAULT_TEMPLATE,

        height=500

    )

    return fig


# ==========================================================
# RISK VS RETURN
# ==========================================================

def risk_return_chart(portfolio_df):

    validate_dataframe(

        portfolio_df,

        [

            "Ticker",

            "Risk",

            "Return"

        ]

    )

    fig = px.scatter(

        portfolio_df,

        x="Risk",

        y="Return",

        text="Ticker",

        title="Risk vs Return"

    )

    fig.update_traces(

        textposition="top center"

    )

    fig.update_layout(

        template=DEFAULT_TEMPLATE,

        height=550

    )

    return fig


# ==========================================================
# CORRELATION HEATMAP
# ==========================================================

def correlation_heatmap(price_df):

    if price_df.empty:

        raise ValueError(

            "Price DataFrame is empty."

        )

    corr = price_df.corr()

    fig = px.imshow(

        corr,

        text_auto=True,

        aspect="auto",

        title="Correlation Heatmap"

    )

    fig.update_layout(

        template=DEFAULT_TEMPLATE,

        height=650

    )

    return fig
# ==========================================================
# STOCK PRICE PREDICTION CHART
# ==========================================================

def prediction_chart(
    historical_df,
    predicted_df
):
    """
    Plot historical vs predicted prices.
    """

    validate_dataframe(
        historical_df,
        ["Close"]
    )

    validate_dataframe(
        predicted_df,
        ["Predicted"]
    )

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=historical_df.index,

            y=historical_df["Close"],

            mode="lines",

            name="Historical"

        )

    )

    fig.add_trace(

        go.Scatter(

            x=predicted_df.index,

            y=predicted_df["Predicted"],

            mode="lines",

            line=dict(dash="dash"),

            name="Prediction"

        )

    )

    apply_layout(

        fig,

        "Historical vs Predicted Price"

    )

    return fig


# ==========================================================
# BUY / SELL SIGNAL CHART
# ==========================================================

def signal_chart(df):

    validate_dataframe(

        df,

        [

            "Close",

            "Signal"

        ]

    )

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=df.index,

            y=df["Close"],

            mode="lines",

            name="Close"

        )

    )

    buy = df[df["Signal"] == "BUY"]

    sell = df[df["Signal"] == "SELL"]

    if not buy.empty:

        fig.add_trace(

            go.Scatter(

                x=buy.index,

                y=buy["Close"],

                mode="markers",

                marker=dict(

                    size=12,

                    symbol="triangle-up"

                ),

                name="BUY"

            )

        )

    if not sell.empty:

        fig.add_trace(

            go.Scatter(

                x=sell.index,

                y=sell["Close"],

                mode="markers",

                marker=dict(

                    size=12,

                    symbol="triangle-down"

                ),

                name="SELL"

            )

        )

    apply_layout(

        fig,

        "Buy / Sell Signals"

    )

    return fig


# ==========================================================
# DRAWDOWN CHART
# ==========================================================

def drawdown_chart(df):

    validate_dataframe(
        df,
        ["Close"]
    )

    price = df["Close"]

    running_max = price.cummax()

    drawdown = (
        (price - running_max)
        / running_max
    ) * 100

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=df.index,

            y=drawdown,

            fill="tozeroy",

            name="Drawdown"

        )

    )

    apply_layout(

        fig,

        "Maximum Drawdown",

        y_title="Drawdown (%)"

    )

    return fig


# ==========================================================
# ROLLING VOLATILITY
# ==========================================================

def volatility_chart(
    df,
    window=20
):

    validate_dataframe(
        df,
        ["Close"]
    )

    volatility = (

        df["Close"]

        .pct_change()

        .rolling(window)

        .std()

        * np.sqrt(252)

        * 100

    )

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=df.index,

            y=volatility,

            mode="lines",

            name="Volatility"

        )

    )

    apply_layout(

        fig,

        "Rolling Volatility",

        y_title="Annualized %"

    )

    return fig


# ==========================================================
# MULTI STOCK COMPARISON
# ==========================================================

def comparison_chart(price_df):

    if price_df.empty:

        raise ValueError(
            "Price DataFrame is empty."
        )

    fig = go.Figure()

    for column in price_df.columns:

        fig.add_trace(

            go.Scatter(

                x=price_df.index,

                y=price_df[column],

                mode="lines",

                name=column

            )

        )

    apply_layout(

        fig,

        "Multi Stock Comparison"

    )

    return fig


# ==========================================================
# TECHNICAL DASHBOARD
# ==========================================================

def technical_dashboard(df):

    validate_dataframe(

        df,

        [

            "Close",

            "Volume",

            "RSI",

            "MACD",

            "MACD_Signal"

        ]

    )

    fig = make_subplots(

        rows=3,

        cols=1,

        shared_xaxes=True,

        vertical_spacing=0.05,

        row_heights=[0.5, 0.25, 0.25]

    )

    fig.add_trace(

        go.Scatter(

            x=df.index,

            y=df["Close"],

            name="Close"

        ),

        row=1,

        col=1

    )

    fig.add_trace(

        go.Scatter(

            x=df.index,

            y=df["RSI"],

            name="RSI"

        ),

        row=2,

        col=1

    )

    fig.add_trace(

        go.Scatter(

            x=df.index,

            y=df["MACD"],

            name="MACD"

        ),

        row=3,

        col=1

    )

    fig.add_trace(

        go.Scatter(

            x=df.index,

            y=df["MACD_Signal"],

            name="Signal"

        ),

        row=3,

        col=1

    )

    fig.update_layout(

        template=DEFAULT_TEMPLATE,

        title="Technical Analysis Dashboard",

        height=900,

        hovermode="x unified"

    )

    return fig
# ==========================================================
# PORTFOLIO GROWTH CHART
# ==========================================================

def portfolio_growth_chart(df):

    validate_dataframe(
        df,
        ["Portfolio Value"]
    )

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=df.index,

            y=df["Portfolio Value"],

            mode="lines",

            name="Portfolio Value"

        )

    )

    apply_layout(

        fig,

        "Portfolio Growth",

        y_title="Portfolio Value"

    )

    return fig


# ==========================================================
# ASSET ALLOCATION TREEMAP
# ==========================================================

def asset_treemap(df):

    validate_dataframe(
        df,
        ["Ticker", "Investment"]
    )

    fig = px.treemap(

        df,

        path=["Ticker"],

        values="Investment",

        title="Asset Allocation Treemap"

    )

    fig.update_layout(

        template=DEFAULT_TEMPLATE,

        height=650

    )

    return fig


# ==========================================================
# SECTOR ALLOCATION
# ==========================================================

def sector_allocation_chart(df):

    validate_dataframe(
        df,
        ["Sector", "Investment"]
    )

    fig = px.pie(

        df,

        names="Sector",

        values="Investment",

        title="Sector Allocation"

    )

    fig.update_layout(

        template=DEFAULT_TEMPLATE,

        height=550

    )

    return fig


# ==========================================================
# NEWS SENTIMENT CHART
# ==========================================================

def sentiment_chart(news_df):

    validate_dataframe(
        news_df,
        ["Sentiment"]
    )

    sentiment = (

        news_df["Sentiment"]

        .value_counts()

        .reset_index()

    )

    sentiment.columns = [

        "Sentiment",

        "Count"

    ]

    fig = px.bar(

        sentiment,

        x="Sentiment",

        y="Count",

        title="News Sentiment Analysis"

    )

    fig.update_layout(

        template=DEFAULT_TEMPLATE,

        height=450

    )

    return fig


# ==========================================================
# FINANCIAL METRICS CHART
# ==========================================================

def financial_metrics_chart(df):

    validate_dataframe(

        df,

        [

            "Metric",

            "Value"

        ]

    )

    fig = px.bar(

        df,

        x="Metric",

        y="Value",

        title="Financial Metrics"

    )

    fig.update_layout(

        template=DEFAULT_TEMPLATE,

        height=550

    )

    return fig


# ==========================================================
# MONTHLY RETURNS
# ==========================================================

def monthly_returns_chart(df):

    validate_dataframe(
        df,
        ["Close"]
    )

    returns = (

        df["Close"]

        .resample("M")

        .last()

        .pct_change()

        * 100

    )

    monthly = returns.reset_index()

    monthly.columns = [

        "Date",

        "Return"

    ]

    fig = px.bar(

        monthly,

        x="Date",

        y="Return",

        title="Monthly Returns"

    )

    fig.update_layout(

        template=DEFAULT_TEMPLATE,

        height=500

    )

    return fig


# ==========================================================
# PERFORMANCE DASHBOARD
# ==========================================================

def performance_dashboard(df):

    validate_dataframe(
        df,
        [
            "Close",
            "Volume"
        ]
    )

    fig = make_subplots(

        rows=2,

        cols=2,

        subplot_titles=(

            "Close",

            "Volume",

            "Daily Returns",

            "Distribution"

        )

    )

    fig.add_trace(

        go.Scatter(

            x=df.index,

            y=df["Close"],

            name="Close"

        ),

        row=1,

        col=1

    )

    fig.add_trace(

        go.Bar(

            x=df.index,

            y=df["Volume"],

            name="Volume"

        ),

        row=1,

        col=2

    )

    returns = (

        df["Close"]

        .pct_change()

        .dropna()

    )

    fig.add_trace(

        go.Scatter(

            x=returns.index,

            y=returns,

            name="Returns"

        ),

        row=2,

        col=1

    )

    fig.add_trace(

        go.Histogram(

            x=returns,

            name="Distribution"

        ),

        row=2,

        col=2

    )

    fig.update_layout(

        template=DEFAULT_TEMPLATE,

        title="Performance Dashboard",

        height=900,

        hovermode="x unified"

    )

    return fig
# ==========================================================
# EXPORT FIGURE
# ==========================================================

def export_chart(
    fig,
    filename="chart.html"
):
    """
    Export Plotly figure to HTML.
    """

    if fig is None:
        return False

    try:

        fig.write_html(
            filename
        )

        return True

    except Exception as e:

        print(e)

        return False


# ==========================================================
# SAVE IMAGE
# ==========================================================

def save_chart_image(
    fig,
    filename="chart.png",
    width=1200,
    height=700
):
    """
    Save Plotly figure as PNG.
    (Requires kaleido package.)
    """

    if fig is None:
        return False

    try:

        fig.write_image(

            filename,

            width=width,

            height=height

        )

        return True

    except Exception as e:

        print(e)

        return False


# ==========================================================
# CHANGE THEME
# ==========================================================

def set_theme(theme="plotly_white"):
    """
    Change default Plotly theme.
    """

    global DEFAULT_TEMPLATE

    DEFAULT_TEMPLATE = theme


# ==========================================================
# FIGURE SUMMARY
# ==========================================================

def figure_information(fig):

    if fig is None:

        return {

            "Traces": 0,

            "Layout": None

        }

    return {

        "Traces": len(fig.data),

        "Layout": fig.layout.title.text

    }


# ==========================================================
# CREATE EMPTY FIGURE
# ==========================================================

def empty_chart(title="No Data Available"):

    fig = go.Figure()

    fig.update_layout(

        title=title,

        template=DEFAULT_TEMPLATE,

        height=400

    )

    fig.add_annotation(

        text="No data available.",

        x=0.5,

        y=0.5,

        showarrow=False,

        font=dict(size=18)

    )

    return fig


# ==========================================================
# MODULE VERSION
# ==========================================================

VERSION = "2.0"


# ==========================================================
# MODULE EXPORTS
# ==========================================================

__all__ = [

    "closing_chart",
    "candlestick_chart",
    "volume_chart",

    "moving_average_chart",
    "rsi_chart",
    "macd_chart",
    "bollinger_chart",
    "price_volume_chart",
    "ohlc_chart",

    "daily_returns_chart",
    "cumulative_returns_chart",
    "returns_histogram",

    "portfolio_allocation_chart",
    "portfolio_performance_chart",
    "portfolio_growth_chart",
    "asset_treemap",
    "sector_allocation_chart",

    "risk_return_chart",
    "correlation_heatmap",

    "prediction_chart",
    "signal_chart",
    "drawdown_chart",
    "volatility_chart",
    "comparison_chart",
    "technical_dashboard",

    "sentiment_chart",
    "financial_metrics_chart",
    "monthly_returns_chart",
    "performance_dashboard",

    "export_chart",
    "save_chart_image",
    "figure_information",
    "empty_chart",

    "set_theme",
    "apply_layout",
    "validate_dataframe",

    "VERSION"
]


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    print("Visualization Module Version 2.0 Loaded Successfully")