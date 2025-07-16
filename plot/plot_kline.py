import plotly.graph_objects as go

def plot_candlestick(df, symbol="BTCUSDT", interval="1h"):
    fig = go.Figure(data=[
        go.Candlestick(
            x=df["timestamp"],
            open=df["open"].astype(float),
            high=df["high"].astype(float),
            low=df["low"].astype(float),
            close=df["close"].astype(float),
            name="Price"
        )
    ])

    fig.update_layout(
        title=f"{symbol} K线图 ({interval})",
        xaxis_title="时间",
        yaxis_title="价格 (USDT)",
        xaxis_rangeslider_visible=False,
        hovermode='x unified'
    )
    fig.show()
