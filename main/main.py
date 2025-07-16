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
    # 2. 配置参数
    symbol   = "BTCUSDT"
    interval = "1h"
    start_dt = datetime(2024, 1, 1)
    end_dt   = datetime.now()

    logging.info(f"开始执行主流程：{symbol} [{interval}] 从 {start_dt} 到 {end_dt}")

    # 3. 更新数据库
    update_klines(symbol, interval, start_dt, end_dt)

    # 4. 从数据库加载数据
    df = load_klines(symbol, interval, start_dt, end_dt)
    if df.empty:
        logging.error("加载到的数据为空，检查数据库或时间范围设置！")
        return

    logging.info(f"加载到 {len(df)} 条数据，准备绘图")

    # 5. 绘图
    plot_candlestick(df, symbol, interval)
    logging.info("绘图完成，程序结束。")

if __name__ == "__main__":
    main()
