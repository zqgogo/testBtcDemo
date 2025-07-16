import requests
import pandas as pd
import matplotlib.pyplot as plt

def get_klines(symbol="BTCUSDT", interval="1h", limit=100):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["close"] = df["close"].astype(float)
    return df[["timestamp", "close"]]

def plot_price(df, symbol):
    plt.figure(figsize=(12, 6))
    plt.plot(df["timestamp"], df["close"], label=f"{symbol} Close Price", color="blue")
    plt.title(f"{symbol} Price - Last {len(df)} Bars")
    plt.xlabel("Time")
    plt.ylabel("Price (USDT)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# 主程序入口
if __name__ == "__main__":
    symbol = "BTCUSDT"  # 改成 ETHUSDT 或 SOLUSDT 可切换币种
    df = get_klines(symbol)
    plot_price(df, symbol)
