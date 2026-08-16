"""Module-level docstring."""
from __future__ import annotations

from typing import Any

__version__ = "0.15.0"

_EXPORTS: dict[str, tuple[str, str]] = {
    "HyperliquidExchangeData": (
        "bt_api_hyperliquid.exchange_data.hyperliquid_exchange_data",
        "HyperliquidExchangeData",
    ),
    "HyperliquidExchangeDataSpot": (
        "bt_api_hyperliquid.exchange_data.hyperliquid_exchange_data",
        "HyperliquidExchangeDataSpot",
    ),
    "HyperliquidExchangeDataSwap": (
        "bt_api_hyperliquid.exchange_data.hyperliquid_exchange_data",
        "HyperliquidExchangeDataSwap",
    ),
    "HyperliquidErrorTranslator": (
        "bt_api_hyperliquid.errors.hyperliquid_translator",
        "HyperliquidErrorTranslator",
    ),
    "HyperliquidRequestData": (
        "bt_api_hyperliquid.feeds.live_hyperliquid",
        "HyperliquidRequestData",
    ),
    "HyperliquidRequestDataSpot": (
        "bt_api_hyperliquid.feeds.live_hyperliquid",
        "HyperliquidRequestDataSpot",
    ),
    "HyperliquidMarketWssDataSpot": (
        "bt_api_hyperliquid.feeds.live_hyperliquid",
        "HyperliquidMarketWssDataSpot",
    ),
    "HyperliquidAccountWssDataSpot": (
        "bt_api_hyperliquid.feeds.live_hyperliquid",
        "HyperliquidAccountWssDataSpot",
    ),
    "register_hyperliquid": (
        "bt_api_hyperliquid.registry_registration",
        "register_hyperliquid",
    ),
}

__all__ = [*_EXPORTS]


def __getattr__(name: str) -> Any:
    try:
        module_name, attr_name = _EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(name) from exc

    from importlib import import_module

    value = getattr(import_module(module_name), attr_name)
    globals()[name] = value
    return value
