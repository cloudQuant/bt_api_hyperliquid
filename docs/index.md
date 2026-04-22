# HYPERLIQUID Documentation

## English

Welcome to the HYPERLIQUID documentation for bt_api.

### Quick Start

```bash
pip install bt_api_hyperliquid
```

```python
from bt_api import BtApi

api = BtApi(
    exchange_kwargs={
        "HYPERLIQUID___SPOT": {
            "api_key": "your_api_key",
            "secret": "your_secret",
        }
    }
)
ticker = api.get_tick("HYPERLIQUID___SPOT", "BTCUSDT")
print(ticker)
```

## 中文

欢迎使用 bt_api 的 HYPERLIQUID 文档。

### 快速开始

```bash
pip install bt_api_hyperliquid
```

```python
from bt_api import BtApi

api = BtApi(
    exchange_kwargs={
        "HYPERLIQUID___SPOT": {
            "api_key": "your_api_key",
            "secret": "your_secret",
        }
    }
)
ticker = api.get_tick("HYPERLIQUID___SPOT", "BTCUSDT")
print(ticker)
```

## API Reference

See source code in `src/bt_api_hyperliquid/` for detailed API documentation.
