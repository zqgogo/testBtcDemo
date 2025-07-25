# main.py

"""
项目主入口脚本
- 更新指定交易对的K线数据（增量到 SQLite）
- 加载数据并绘制交互式蜡烛图
"""

import sys
import os

# 自动添加项目根目录到 sys.path（确保能导入 data/ 和 plot/）
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from datetime import datetime
from data.data_fetcher import update_klines
from data.db_manager import load_klines
from plot.plot_kline import plot_candlestick

# 1. 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("main.log"),
        logging.StreamHandler()
    ]
)

def main():
    symbol = 'BTCUSDT'
    intervals = ['15m', '1h', '4h', '1d']
    start = '2024-01-01'
    end = '2024-07-01'

    for interval in intervals:
        print(f"\n>>> 开始处理 {symbol} - {interval}")

        # 1. 更新数据（增量更新）
        update_klines(symbol, interval, start, end)

        # 2. 从数据库加载数据
        df = load_klines(symbol, interval, start, end)
        if df.empty:
            print(f"[ERROR] {symbol} - {interval} 没有加载到数据！")
            continue

        # 3. 绘制蜡烛图
        plot_candlestick(df, symbol, interval)
        print(f">>> {symbol} - {interval} 绘图完成\n")

if __name__ == '__main__':
    main()
