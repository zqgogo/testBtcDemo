# QuantAI - 基于 Binance API 的量化投资工具

QuantAI 是一个为个人投资者打造的轻量级量化工具，支持从 Binance 获取加密货币 K 线数据，缓存本地并可视化显示交互式蜡烛图。项目设计强调模块化、低耦合，适合用于策略开发、回测和 AI 模型数据准备。

---

## ✅ 功能特性

* 📦 **数据缓存（SQLite）**：自动保存历史数据到本地数据库，避免重复请求
* 🔄 **增量更新**：智能检测最新时间戳，只拉取新增数据
* 📈 **交互式K线图**：使用 Plotly 绘制蜡烛图，支持鼠标悬停/点击查看价格
* ⚙️ **模块化设计**：分离数据获取、数据库管理、可视化模块，低耦合高可维护
* 🔁 **灵活配置**：任意币种（如 BTC/ETH/SOL）、周期（如 1h/1d）、时间范围

---

## 📁 项目结构

```
myquant/
├── data/
│   ├── db_manager.py         # SQLite 数据库管理模块
│   ├── data_fetcher.py       # Binance 数据抓取与增量更新模块
│   ├── kline.db              # 本地 SQLite 数据库（缓存K线数据）
│   ├── db.log                # 数据库操作日志
│   └── fetch.log             # 数据抓取日志
│
├── plot/
│   └── plot_kline.py         # 交互式蜡烛图绘制模块
│
├── main.py                   # 入口脚本：示例调用获取&绘制流程
└── README.md                 # 项目说明文档
```

---

## ⚙️ 快速开始

1. 克隆项目并进入目录

   ```bash
   git clone <repo_url>
   cd myquant
   ```

2. (可选) 创建并激活虚拟环境

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. 安装依赖

   ```bash
   pip install requests pandas plotly
   ```

4. 修改 `main.py` 中参数并运行：

   ```bash
   python main.py
   ```

---

## 🔧 参数说明

| 参数         | 类型         | 示例值                  | 说明                                |
| ---------- | ---------- | -------------------- | --------------------------------- |
| `symbol`   | `str`      | `"BTCUSDT"`          | 交易对名称，必须大写，符合 Binance API         |
| `interval` | `str`      | `"1h"`               | 周期（可选值）：                          |
|            |            |                      | `'1m','3m','5m','15m','30m',`     |
|            |            |                      | `'1h','2h','4h','6h','8h','12h',` |
|            |            |                      | `'1d','3d','1w','1M'`             |
| `start_dt` | `datetime` | `datetime(2024,1,1)` | 起始时间（Python datetime 对象）          |
| `end_dt`   | `datetime` | `datetime.now()`     | 结束时间（Python datetime 对象）          |

---

## 📜 日志说明

* 使用 Python 标准库 `logging` 进行日志管理
* 日志文件保存在：

  * `data/db.log`（数据库操作日志）
  * `data/fetch.log`（数据抓取日志）
* 控制台和文件双输出，记录 INFO/WARNING/ERROR 级别信息

---

## 📝 代码规范

1. **注释 & 文档**

   * 每个函数带详细 `docstring`，说明参数类型、范围、格式与返回值
   * 模块头部说明功能，方便自动生成文档

2. **日志输出**

   * 使用 `logging` 模块，按等级输出
   * 在关键流程节点与异常处记录日志

3. **模块化设计**

   * 职责单一：数据库操作、数据抓取、绘图互不耦合
   * 使用类型注解，符合 PEP8

---

## 🚀 未来规划

* 添加技术指标（MA、MACD、RSI）和策略信号标注
* 回测引擎模块拆分
* AI 模型预测集成
* Web 界面或监控端集成

