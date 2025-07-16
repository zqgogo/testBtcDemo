# data_fetcher.py
"""
数据获取模块 - 从 Binance 获取历史K线并更新本地数据库

支持：
- 增量拉取
- 自动补全历史缺失部分
"""

import time
import requests
import pandas as pd
from datetime import datetime
from data.db_manager import create_table, insert_klines, get_latest_timestamp
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("data/fetch.log"),
        logging.StreamHandler()
    ]
)

def fetch_klines(symbol, interval, start_ts, end_ts):
    """
    向 Binance API 请求历史K线数据（支持分页获取）

    参数说明:
    ----------
    symbol : str
        币种，例如 'BTCUSDT'

    interval : str
        时间周期，参考 Binance 文档，合法值包括：
            '1m', '3m', '5m', '15m', '30m',
            '1h', '2h', '4h', '6h', '8h', '12h',
            '1d', '3d', '1w', '1M'

    start_ts : int
        起始时间戳，单位为毫秒（ms）

    end_ts : int
        结束时间戳，单位为毫秒（ms）

    返回:
    -------
    list
        返回 Binance 原始数据（二维数组），每个元素是一根K线
    """
    logging.info(f"[Fetch] 开始获取 {symbol} {interval}...")
    url = "https://api.binance.com/api/v3/klines"
    data = []
    limit = 1000
    while start_ts < end_ts:
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
            "startTime": start_ts,
            "endTime": end_ts
        }
        try:
            resp = requests.get(url, params=params)
            raw = resp.json()
            if not raw or 'code' in raw:
                logging.warning(f"[Fetch] 返回空或错误：{raw}")
                break
            data += raw
            start_ts = raw[-1][0] + 1
            if len(raw) < limit:
                break
            time.sleep(0.2)
        except Exception as e:
            logging.error(f"[Fetch] 请求失败：{e}")
            break
    return data

def update_klines(symbol, interval, start_dt, end_dt):
    """
    更新数据库中某币种+周期的K线数据（增量拉取）

    参数说明:
    ----------
    symbol : str
        币种交易对，例如：'BTCUSDT', 'ETHUSDT', 'SOLUSDT'
        必须是 Binance 支持的合约或现货对（建议大写）

    interval : str
        周期，可选值（Binance 支持）如下：
            '1m', '3m', '5m', '15m', '30m',
            '1h', '2h', '4h', '6h', '8h', '12h',
            '1d', '3d', '1w', '1M'

    start_dt : datetime
        起始时间，必须是 Python 的 datetime 类型

    end_dt : datetime
        结束时间，必须是 Python 的 datetime 类型

    返回:
    -------
    无返回值，但会将数据写入本地 SQLite 数据库中，
    并根据已有数据判断是否进行增量更新。
    """
    logging.info(f"[Update] {symbol}-{interval} 更新开始：{start_dt} → {end_dt}")
    create_table(symbol, interval)
    last_dt = get_latest_timestamp(symbol, interval)

    if last_dt and last_dt >= end_dt:
        logging.info("[Update] 数据已是最新，无需更新")
        return

    from_ts = int((last_dt.timestamp() + 1) * 1000) if last_dt else int(start_dt.timestamp() * 1000)
    to_ts = int(end_dt.timestamp() * 1000)

    raw = fetch_klines(symbol, interval, from_ts, to_ts)
    if not raw:
        logging.warning("[Update] 没有新数据拉取")
        return

    df = pd.DataFrame(raw, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df[["timestamp", "open", "high", "low", "close", "volume"]]
    insert_klines(symbol, interval, df)
