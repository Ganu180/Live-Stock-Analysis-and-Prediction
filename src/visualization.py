import plotly.graph_objects as go


# -------------------------------------------------
# Closing Price Chart
# -------------------------------------------------

def closing_chart(df):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["Close"],
            mode="lines",
            name="Close Price"
        )
    )

    fig.update_layout(
        title="Closing Price",
        template="plotly_white",
        height=500,
        xaxis_title="Date",
        yaxis_title="Price"
    )

    return fig


# -------------------------------------------------
# Candlestick Chart
# -------------------------------------------------

def candlestick_chart(df):

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

    fig.update_layout(
        title="Candlestick Chart",
        template="plotly_white",
        height=650,
        xaxis_rangeslider_visible=True
    )

    return fig


# -------------------------------------------------
# Volume Chart
# -------------------------------------------------

def volume_chart(df):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df["Volume"],
            name="Volume"
        )
    )

    fig.update_layout(
        title="Trading Volume",
        template="plotly_white",
        height=350,
        xaxis_title="Date",
        yaxis_title="Volume"
    )

    return fig


# -------------------------------------------------
# Moving Average Chart
# -------------------------------------------------

def moving_average_chart(df):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["Close"],
            name="Close"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["SMA20"],
            name="SMA 20"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["SMA50"],
            name="SMA 50"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["EMA20"],
            name="EMA 20"
        )
    )

    fig.update_layout(
        title="Moving Averages",
        template="plotly_white",
        height=500,
        xaxis_title="Date",
        yaxis_title="Price"
    )

    return fig


# -------------------------------------------------
# RSI Chart
# -------------------------------------------------

def rsi_chart(df):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["RSI"],
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

    fig.update_layout(
        title="Relative Strength Index (RSI)",
        template="plotly_white",
        height=400,
        yaxis=dict(range=[0, 100])
    )

    return fig


# -------------------------------------------------
# MACD Chart
# -------------------------------------------------

def macd_chart(df):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["MACD"],
            name="MACD"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["MACD_Signal"],
            name="Signal"
        )
    )

    fig.update_layout(
        title="MACD Indicator",
        template="plotly_white",
        height=450
    )

    return fig


# -------------------------------------------------
# Bollinger Bands Chart
# -------------------------------------------------

def bollinger_chart(df):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["Close"],
            name="Close"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["BB_High"],
            name="Upper Band"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["BB_Low"],
            name="Lower Band"
        )
    )

    fig.update_layout(
        title="Bollinger Bands",
        template="plotly_white",
        height=500
    )

    return fig