# HYPERLIQUID

Exchange plugin for bt_api framework — decentralized perpetual futures exchange.

[![PyPI Version](https://img.shields.io/pypi/v/bt_api_hyperliquid.svg)](https://pypi.org/project/bt_api_hyperliquid/)
[![Python Versions](https://img.shields.io/pypi/pyversions/bt_api_hyperliquid.svg)](https://pypi.org/project/bt_api_hyperliquid/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/cloudQuant/bt_api_hyperliquid/actions/workflows/ci.yml/badge.svg)](https://github.com/cloudQuant/bt_api_hyperliquid/actions)
[![Docs](https://readthedocs.org/projects/bt-api-hyperliquid/badge/?version=latest)](https://bt-api-hyperliquid.readthedocs.io/)

---

## English | [中文](#中文)

### Overview

[Hyperliquid](https://hyperliquid.gitbook.io/hyperliquid-docs/) is a **decentralized perpetual futures exchange** built on its own Layer 1 blockchain (Hyperliquid L1). This plugin integrates Hyperliquid into the [bt_api](https://github.com/cloudQuant/bt_api_py) unified trading framework, supporting both **SPOT** and **SWAP (perpetual futures)** markets.

### Features

- **REST API** — market data queries, order management, account queries
- **WebSocket feeds** — real-time ticker, order book, account and trade streams
- **Multi-asset-type** — supports both SPOT and perpetual futures (USDC-margined)
- **Ethereum-style auth** — uses Ethereum private keys for signing (no API keys required)
- **High rate limits** — 1200 requests/minute to `/info` endpoint

### Exchange Codes

| Code | Description | Asset Type |
|------|-------------|------------|
| `HYPERLIQUID___SPOT` | Hyperliquid spot markets | SPOT |
| `HYPERLIQUID___SWAP` | Hyperliquid perpetual futures | SWAP |

### Installation

```bash
pip install bt_api_hyperliquid
```

Or install from source:

```bash
git clone https://github.com/cloudQuant/bt_api_hyperliquid
cd bt_api_hyperliquid
pip install -e .
```

### Quick Start

```python
from bt_api import BtApi

# Hyperliquid uses Ethereum-style private key authentication
# (API keys are NOT used; the private key signs requests)
api = BtApi(
    exchange_kwargs={
        "HYPERLIQUID___SPOT": {
            "private_key": "0xYourEthereumPrivateKey",  # or api_secret
        },
        "HYPERLIQUID___SWAP": {
            "private_key": "0xYourEthereumPrivateKey",
        }
    }
)

# Get ticker data
ticker = api.get_tick("HYPERLIQUID___SPOT", "BTCUSDT")
print(ticker)

# Get order book depth
depth = api.get_depth("HYPERLIQUID___SWAP", "BTC/USDC")
print(depth)

# Get K-line / bars
bars = api.get_kline("HYPERLIQUID___SWAP", "BTC/USDC", "1h")
print(bars)
```

### Supported Operations

| Operation | SPOT | SWAP | Notes |
|-----------|:----:|:----:|-------|
| Ticker | ✅ | ✅ | `get_tick()` |
| OrderBook (Depth) | ✅ | ✅ | `get_depth()` |
| K-Line (Bars) | ✅ | ✅ | `get_kline()` |
| Recent Trades | ✅ | ✅ | `get_recent_trades()` |
| Exchange Info | ✅ | ✅ | `get_exchange_info()` |
| Account Balance | ✅ | ✅ | `get_balance()` |
| Order Management | ✅ | ✅ | `make_order`, `cancel_order` |
| WebSocket Stream | ✅ | ✅ | `subscribe()` |
| User Fills | ✅ | ✅ | `get_user_fills()` |
| Funding Info | ✅ | ✅ | `get_user_funding()` |

### Architecture

```
bt_api_hyperliquid/
├── src/bt_api_hyperliquid/
│   ├── containers/              # Data containers
│   │   ├── accounts/           # Account data
│   │   ├── balances/          # Balance data
│   │   ├── orders/             # Order data (REST & WebSocket)
│   │   ├── tickers/            # Ticker data
│   │   └── trades/            # Trade data
│   ├── exchange_data/           # Exchange metadata & symbol routing
│   ├── feeds/live_hyperliquid/ # REST & WebSocket feed implementations
│   │   ├── request_base.py     # HyperliquidRequestData (REST feed)
│   │   ├── spot.py             # SPOT-specific feeds & WebSocket
│   │   ├── account_wss_base.py # Account WebSocket stream
│   │   └── market_wss_base.py  # Market data WebSocket stream
│   ├── errors/                 # Error translator
│   ├── registry_registration.py # Exchange registry wiring
│   └── plugin.py               # Plugin entry point
├── tests/                      # Unit tests
└── docs/                       # Documentation
```

### API Reference

#### Feed Classes

- **`HyperliquidRequestData`** — REST feed for SWAP markets; supports ticker, depth, kline, order management, account queries
- **`HyperliquidRequestDataSpot`** — REST feed for SPOT markets; same interface as above

#### WebSocket Classes

- **`HyperliquidMarketWssDataSpot`** — Market data WebSocket (ticker, orderbook, trades)
- **`HyperliquidAccountWssDataSpot`** — Account WebSocket (orders, trades, positions)

#### Container Classes

- **`HyperliquidTickerData`** — Ticker data container
- **`HyperliquidRequestOrderData`** — Order data from REST API
- **`HyperliquidSpotWssOrderData`** — Order data from WebSocket stream
- **`HyperliquidBalanceData`** — Balance / clearinghouse state container
- **`HyperliquidTradeData`** — Trade / fill data container

#### Exchange Data Classes

- **`HyperliquidExchangeData`** — Base exchange metadata (REST/WSS URLs, symbol mapping, kline periods)
- **`HyperliquidExchangeDataSpot`** — SPOT-specific metadata
- **`HyperliquidExchangeDataSwap`** — SWAP-specific metadata

### Online Documentation

| Resource | Link |
|----------|------|
| English Docs | https://bt-api-hyperliquid.readthedocs.io/ |
| Chinese Docs | https://bt-api-hyperliquid.readthedocs.io/zh/latest/ |
| GitHub Repository | https://github.com/cloudQuant/bt_api_hyperliquid |
| Issue Tracker | https://github.com/cloudQuant/bt_api_hyperliquid/issues |
| Hyperliquid API Docs | https://hyperliquid.gitbook.io/hyperliquid-docs/ |

### Requirements

- Python 3.9+
- bt_api_base >= 0.15, < 1.0
- `eth_account` (for Ethereum key signing)

### License

MIT License — see [LICENSE](LICENSE) for details.

### Support

- Report bugs via [GitHub Issues](https://github.com/cloudQuant/bt_api_hyperliquid/issues)
- Email: yunjinqi@gmail.com

---

## 中文

### 概述

[Hyperliquid](https://hyperliquid.gitbook.io/hyperliquid-docs/) 是一个**去中心化永续期货交易所**，运行于其自主研发的 Layer 1 区块链（Hyperliquid L1）上。本插件将 Hyperliquid 接入 [bt_api](https://github.com/cloudQuant/bt_api_py) 统一交易框架，支持**现货（SPOT）**和**永续合约（SWAP）**两类市场。

### 功能特点

- **REST API** — 行情查询、订单管理、账户查询
- **WebSocket 推送** — 实时行情、订单簿、账户和成交推送
- **多市场类型** — 支持现货和 USDC 保证金永续期货
- **以太坊风格认证** — 使用以太坊私钥签名（无需 API Key）
- **高请求限额** — `/info` 接口 1200 次/分钟

### 交易所代码

| 代码 | 描述 | 资产类型 |
|------|------|----------|
| `HYPERLIQUID___SPOT` | Hyperliquid 现货市场 | SPOT |
| `HYPERLIQUID___SWAP` | Hyperliquid 永续期货 | SWAP |

### 安装

```bash
pip install bt_api_hyperliquid
```

或从源码安装：

```bash
git clone https://github.com/cloudQuant/bt_api_hyperliquid
cd bt_api_hyperliquid
pip install -e .
```

### 快速开始

```python
from bt_api import BtApi

# Hyperliquid 使用以太坊私钥进行签名认证
# （不使用 API Key，私钥用于签名请求）
api = BtApi(
    exchange_kwargs={
        "HYPERLIQUID___SPOT": {
            "private_key": "0x您的以太坊私钥",  # 也可用 api_secret
        },
        "HYPERLIQUID___SWAP": {
            "private_key": "0x您的以太坊私钥",
        }
    }
)

# 获取行情
ticker = api.get_tick("HYPERLIQUID___SPOT", "BTCUSDT")
print(ticker)

# 获取订单簿深度
depth = api.get_depth("HYPERLIQUID___SWAP", "BTC/USDC")
print(depth)

# 获取 K 线数据
bars = api.get_kline("HYPERLIQUID___SWAP", "BTC/USDC", "1h")
print(bars)
```

### 支持的操作

| 操作 | SPOT | SWAP | 说明 |
|------|:----:|:----:|------|
| 行情 | ✅ | ✅ | `get_tick()` |
| 订单簿 | ✅ | ✅ | `get_depth()` |
| K 线 | ✅ | ✅ | `get_kline()` |
| 最新成交 | ✅ | ✅ | `get_recent_trades()` |
| 交易所信息 | ✅ | ✅ | `get_exchange_info()` |
| 账户余额 | ✅ | ✅ | `get_balance()` |
| 订单管理 | ✅ | ✅ | `make_order`, `cancel_order` |
| WebSocket 推送 | ✅ | ✅ | `subscribe()` |
| 用户成交 | ✅ | ✅ | `get_user_fills()` |
| 资金费率 | ✅ | ✅ | `get_user_funding()` |

### 架构

```
bt_api_hyperliquid/
├── src/bt_api_hyperliquid/
│   ├── containers/              # 数据容器
│   │   ├── accounts/           # 账户数据
│   │   ├── balances/          # 余额数据
│   │   ├── orders/             # 订单数据（REST & WebSocket）
│   │   ├── tickers/            # 行情数据
│   │   └── trades/            # 成交数据
│   ├── exchange_data/           # 交易所元数据 & 交易对路由
│   ├── feeds/live_hyperliquid/ # REST & WebSocket feed 实现
│   │   ├── request_base.py     # HyperliquidRequestData (REST)
│   │   ├── spot.py             # SPOT 专用 feed & WebSocket
│   │   ├── account_wss_base.py # 账户 WebSocket 流
│   │   └── market_wss_base.py  # 行情 WebSocket 流
│   ├── errors/                 # 错误翻译器
│   ├── registry_registration.py # 交易所注册 wiring
│   └── plugin.py               # 插件入口
├── tests/                      # 单元测试
└── docs/                       # 文档
```

### API 参考

#### Feed 类

- **`HyperliquidRequestData`** — SWAP 市场 REST feed；支持行情、深度、K 线、订单管理、账户查询
- **`HyperliquidRequestDataSpot`** — SPOT 市场 REST feed；接口同上

#### WebSocket 类

- **`HyperliquidMarketWssDataSpot`** — 行情 WebSocket（行情、订单簿、成交）
- **`HyperliquidAccountWssDataSpot`** — 账户 WebSocket（订单、成交、持仓）

#### 容器类

- **`HyperliquidTickerData`** — 行情数据容器
- **`HyperliquidRequestOrderData`** — REST API 返回的订单数据
- **`HyperliquidSpotWssOrderData`** — WebSocket 推送的订单数据
- **`HyperliquidBalanceData`** — 余额 / clearinghouse 状态容器
- **`HyperliquidTradeData`** — 成交 / 订单数据容器

#### 交易所数据类

- **`HyperliquidExchangeData`** — 基础交易所元数据（REST/WSS URL、交易对映射、K 线周期）
- **`HyperliquidExchangeDataSpot`** — SPOT 专用元数据
- **`HyperliquidExchangeDataSwap`** — SWAP 专用元数据

### 在线文档

| 资源 | 链接 |
|------|------|
| 英文文档 | https://bt-api-hyperliquid.readthedocs.io/ |
| 中文文档 | https://bt-api-hyperliquid.readthedocs.io/zh/latest/ |
| GitHub 仓库 | https://github.com/cloudQuant/bt_api_hyperliquid |
| 问题反馈 | https://github.com/cloudQuant/bt_api_hyperliquid/issues |
| Hyperliquid API 文档 | https://hyperliquid.gitbook.io/hyperliquid-docs/ |

### 系统要求

- Python 3.9+
- bt_api_base >= 0.15, < 1.0
- `eth_account`（用于以太坊私钥签名）

### 许可证

MIT 许可证 — 详见 [LICENSE](LICENSE)。

### 技术支持

- 通过 [GitHub Issues](https://github.com/cloudQuant/bt_api_hyperliquid/issues) 反馈问题
- 邮箱: yunjinqi@gmail.com
