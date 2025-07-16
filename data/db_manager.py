# db_manager.py
"""
数据库管理模块（SQLite）

功能：
- 创建数据表
- 插入K线数据
- 查询最新时间戳
- 加载指定时间范围的数据
"""

import sqlite3
import pandas as pd
from typing import Optional
from datetime import datetime
import logging

# 初始化日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("data/db.log"),
        logging.StreamHandler()
    ]
)

DB_PATH = "data/kline.db"

def connect_db():
    """连接到 SQLite 数据库"""
    return sqlite3.connect(DB_PATH)

def create_table(symbol: str, interval: str):
    """
    创建表结构（如果不存在）
    :param symbol: 币种（如BTCUSDT）
    :param interval: 周期（如1h）
    """
    table = f"{symbol}_{interval}"
    with connect_db() as conn:
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {table} (
                timestamp TEXT PRIMARY KEY,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL
            )
        """)
    logging.info(f"[DB] 表已确认存在：{table}")

def insert_klines(symbol: str, interval: str, df: pd.DataFrame):
    """
    插入K线数据
    :param df: 包含 timestamp, open, high, low, close, volume 的DataFrame
    """
    table = f"{symbol}_{interval}"
    df = df.copy()
    df["timestamp"] = df["timestamp"].astype(str)
    with connect_db() as conn:
        try:
            df.to_sql(table, conn, if_exists="append", index=False, method="multi")
            logging.info(f"[DB] 成功插入 {len(df)} 条记录 -> 表 {table}")
        except Exception as e:
            logging.error(f"[DB] 插入失败: {e}")

def get_latest_timestamp(symbol: str, interval: str) -> Optional[datetime]:
    """
    获取某表的最新一条时间戳（用于增量更新）
    """
    table = f"{symbol}_{interval}"
    try:
        with connect_db() as conn:
            cursor = conn.execute(f"SELECT MAX(timestamp) FROM {table}")
            row = cursor.fetchone()
            if row and row[0]:
                return datetime.fromisoformat(row[0])
    except Exception as e:
        logging.warning(f"[DB] 获取最新时间失败: {e}")
    return None

def load_klines(symbol: str, interval: str, start: Optional[datetime] = None, end: Optional[datetime] = None) -> pd.DataFrame:
    """
    从数据库加载指定时间范围的K线数据
    """
    table = f"{symbol}_{interval}"
    try:
        with connect_db() as conn:
            query = f"SELECT * FROM {table}"
            if start and end:
                query += f" WHERE timestamp >= '{start.isoformat()}' AND timestamp <= '{end.isoformat()}'"
            elif start:
                query += f" WHERE timestamp >= '{start.isoformat()}'"
            elif end:
                query += f" WHERE timestamp <= '{end.isoformat()}'"
            df = pd.read_sql(query, conn, parse_dates=["timestamp"])
            logging.info(f"[DB] 加载数据 {len(df)} 条 -> {table}")
            return df
    except Exception as e:
        logging.error(f"[DB] 加载失败：{e}")
        return pd.DataFrame()
