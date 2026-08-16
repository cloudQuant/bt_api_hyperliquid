# HYPERLIQUID Documentation

## English

### Overview

[Hyperliquid](https://hyperliquid.gitbook.io/hyperliquid-docs/) is a decentralized perpetual futures exchange built on its own Layer 1 blockchain. This plugin integrates Hyperliquid SPOT and SWAP markets into the bt_api framework.

### Exchange Codes

| Code | Description | Asset Type |
|------|-------------|------------|
| `HYPERLIQUID___SPOT` | Hyperliquid spot markets | SPOT |
| `HYPERLIQUID___SWAP` | Hyperliquid perpetual futures | SWAP |

### Quick Start

```bash
pip install bt_api_hyperliquid
```

```python
from bt_api import BtApi

api = BtApi(
    exchange_kwargs={
        "HYPERLIQUID___SPOT": {
            "private_key": "0xYourEthereumPrivateKey",
        },
        "HYPERLIQUID___SWAP": {
            "private_key": "0xYourEthereumPrivateKey",
        }
    }
)

# Market data
ticker = api.get_tick("HYPERLIQUID___SWAP", "BTC/USDC")
depth = api.get_depth("HYPERLIQUID___SWAP", "BTC/USDC")
bars = api.get_kline("HYPERLIQUID___SWAP", "BTC/USDC", "1h")

# WebSocket subscription
api.subscribe(
    "HYPERLIQUID___SWAP___BTC/USDC",
    [
        {"topic": "ticker", "symbol": "BTC/USDC"},
        {"topic": "l2Book", "symbol": "BTC/USDC"},
    ],
)
```

### API Reference

#### Feed Classes

| Class | Description |
|-------|-------------|
| `HyperliquidRequestData` | REST feed for SWAP markets |
| `HyperliquidRequestDataSpot` | REST feed for SPOT markets |
| `HyperliquidMarketWssDataSpot` | Market data WebSocket stream |
| `HyperliquidAccountWssDataSpot` | Account WebSocket stream |

#### Container Classes

| Class | Description |
|-------|-------------|
| `HyperliquidTickerData` | Ticker / price data |
| `HyperliquidRequestOrderData` | Order data from REST API |
| `HyperliquidSpotWssOrderData` | Order data from WebSocket |
| `HyperliquidBalanceData` | Balance / clearinghouse state |
| `HyperliquidTradeData` | Trade / fill data |

#### Exchange Data Classes

| Class | Description |
|-------|-------------|
| `HyperliquidExchangeData` | Base exchange metadata |
| `HyperliquidExchangeDataSpot` | SPOT metadata |
| `HyperliquidExchangeDataSwap` | SWAP metadata |

#### Key Methods

| Method | Description |
|--------|-------------|
| `get_tick(symbol)` | Get ticker data |
| `get_depth(symbol, count=20)` | Get order book depth |
| `get_kline(symbol, period, count=20)` | Get K-line / OHLCV data |
| `get_recent_trades(coin, limit=100)` | Get recent trades |
| `get_balance()` | Get account balance |
| `get_exchange_info()` | Get exchange / symbol info |
| `make_order(symbol, side, price, volume, order_type)` | Place order |
| `cancel_order(symbol, order_id)` | Cancel order |
| `get_user_fills(user, limit=100)` | Get user trade history |
| `get_user_funding(user)` | Get funding history |

#### WebSocket Topics

| Topic | Description |
|-------|-------------|
| `ticker` | Real-time ticker updates |
| `l2Book` | Order book depth updates |
| `trades` | Real-time trade stream |
| `account` | Account updates (orders, fills, positions) |
| `order` | Order update stream |

#### Kline Periods

`1m`, `3m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `8h`, `12h`, `1d`, `3d`, `1w`, `1M`

#### Authentication

Hyperliquid uses Ethereum-style private key authentication. Provide the private key via `private_key` (or aliases: `api_secret`, `secret_key`). The library uses `eth_account` to sign requests — no API key is required.

---

## 中文

### 概述

[Hyperliquid](https://hyperliquid.gitbook.io/hyperliquid-docs/) 是运行于自主 Layer 1 区块链上的去中心化永续期货交易所。本插件将 Hyperliquid 现货和永续合约市场接入 bt_api 框架。

### 交易所代码

| 代码 | 描述 | 资产类型 |
|------|------|----------|
| `HYPERLIQUID___SPOT` | Hyperliquid 现货市场 | SPOT |
| `HYPERLIQUID___SWAP` | Hyperliquid 永续期货 | SWAP |

### 快速开始

```bash
pip install bt_api_hyperliquid
```

```python
from bt_api import BtApi

api = BtApi(
    exchange_kwargs={
        "HYPERLIQUID___SPOT": {
            "private_key": "0x您的以太坊私钥",
        },
        "HYPERLIQUID___SWAP": {
            "private_key": "0x您的以太坊私钥",
        }
    }
)

# 行情数据
ticker = api.get_tick("HYPERLIQUID___SWAP", "BTC/USDC")
depth = api.get_depth("HYPERLIQUID___SWAP", "BTC/USDC")
bars = api.get_kline("HYPERLIQUID___SWAP", "BTC/USDC", "1h")

# WebSocket 订阅
api.subscribe(
    "HYPERLIQUID___SWAP___BTC/USDC",
    [
        {"topic": "ticker", "symbol": "BTC/USDC"},
        {"topic": "l2Book", "symbol": "BTC/USDC"},
    ],
)
```

### API 参考

#### Feed 类

| 类 | 描述 |
|----|------|
| `HyperliquidRequestData` | SWAP 市场 REST feed |
| `HyperliquidRequestDataSpot` | SPOT 市场 REST feed |
| `HyperliquidMarketWssDataSpot` | 行情 WebSocket 流 |
| `HyperliquidAccountWssDataSpot` | 账户 WebSocket 流 |

#### 容器类

| 类 | 描述 |
|----|------|
| `HyperliquidTickerData` | 行情 / 价格数据 |
| `HyperliquidRequestOrderData` | REST API 返回的订单数据 |
| `HyperliquidSpotWssOrderData` | WebSocket 推送的订单数据 |
| `HyperliquidBalanceData` | 余额 / clearinghouse 状态 |
| `HyperliquidTradeData` | 成交 / 订单数据 |

#### 交易所数据类

| 类 | 描述 |
|----|------|
| `HyperliquidExchangeData` | 基础交易所元数据 |
| `HyperliquidExchangeDataSpot` | SPOT 元数据 |
| `HyperliquidExchangeDataSwap` | SWAP 元数据 |

#### 核心方法

| 方法 | 描述 |
|------|------|
| `get_tick(symbol)` | 获取行情数据 |
| `get_depth(symbol, count=20)` | 获取订单簿深度 |
| `get_kline(symbol, period, count=20)` | 获取 K 线 / OHLCV 数据 |
| `get_recent_trades(coin, limit=100)` | 获取最新成交 |
| `get_balance()` | 获取账户余额 |
| `get_exchange_info()` | 获取交易所 / 交易对信息 |
| `make_order(symbol, side, price, volume, order_type)` | 下单 |
| `cancel_order(symbol, order_id)` | 撤单 |
| `get_user_fills(user, limit=100)` | 获取用户成交历史 |
| `get_user_funding(user)` | 获取资金费率历史 |

#### WebSocket Topic

| Topic | 描述 |
|-------|------|
| `ticker` | 实时行情推送 |
| `l2Book` | 订单簿深度推送 |
| `trades` | 实时成交推送 |
| `account` | 账户更新（订单、成交、持仓） |
| `order` | 订单更新推送 |

#### K 线周期

`1m`, `3m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `8h`, `12h`, `1d`, `3d`, `1w`, `1M`

#### 认证方式

Hyperliquid 使用以太坊私钥认证。通过 `private_key`（或别名 `api_secret`, `secret_key`）提供私钥。库内使用 `eth_account` 对请求签名——无需 API Key。
