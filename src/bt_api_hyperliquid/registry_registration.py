from __future__ import annotations

from typing import Any

from bt_api_base.balance_utils import simple_balance_handler as _hyperliquid_balance_handler
from bt_api_base.registry import ExchangeRegistry

from bt_api_hyperliquid.exchange_data.hyperliquid_exchange_data import (
    HyperliquidExchangeDataSpot,
    HyperliquidExchangeDataSwap,
)
from bt_api_hyperliquid.feeds.live_hyperliquid import (
    HyperliquidAccountWssDataSpot,
    HyperliquidMarketWssDataSpot,
    HyperliquidRequestData,
    HyperliquidRequestDataSpot,
)


def _hyperliquid_swap_subscribe_handler(data_queue: Any, exchange_params: Any, topics: Any, bt_api: Any) -> None:
    exchange_data = HyperliquidExchangeDataSwap()
    kwargs = dict(exchange_params.items())
    kwargs['wss_name'] = 'hyperliquid_market_data'
    kwargs['wss_url'] = 'wss://api.hyperliquid.xyz/ws'
    kwargs['exchange_data'] = exchange_data
    kwargs['topics'] = topics
    HyperliquidMarketWssDataSpot(data_queue, **kwargs).start()
    if not bt_api._subscription_flags.get('HYPERLIQUID___SWAP_account', False):
        account_kwargs = dict(kwargs.items())
        account_kwargs['topics'] = [
            {'topic': 'account'},
            {'topic': 'order'},
            {'topic': 'trade'},
        ]
        HyperliquidAccountWssDataSpot(data_queue, **account_kwargs).start()
        bt_api._subscription_flags['HYPERLIQUID___SWAP_account'] = True


def _hyperliquid_spot_subscribe_handler(data_queue: Any, exchange_params: Any, topics: Any, bt_api: Any) -> None:
    exchange_data = HyperliquidExchangeDataSpot()
    kwargs = dict(exchange_params.items())
    kwargs['wss_name'] = 'hyperliquid_market_data'
    kwargs['wss_url'] = 'wss://api.hyperliquid.xyz/ws'
    kwargs['exchange_data'] = exchange_data
    kwargs['topics'] = topics
    HyperliquidMarketWssDataSpot(data_queue, **kwargs).start()
    if not bt_api._subscription_flags.get('HYPERLIQUID___SPOT_account', False):
        account_kwargs = dict(kwargs.items())
        account_kwargs['topics'] = [
            {'topic': 'account'},
            {'topic': 'order'},
            {'topic': 'trade'},
        ]
        HyperliquidAccountWssDataSpot(data_queue, **account_kwargs).start()
        bt_api._subscription_flags['HYPERLIQUID___SPOT_account'] = True


def register_hyperliquid(registry: type[ExchangeRegistry]) -> None:
    registry.register_feed('HYPERLIQUID___SWAP', HyperliquidRequestData)
    registry.register_exchange_data('HYPERLIQUID___SWAP', HyperliquidExchangeDataSwap)
    registry.register_balance_handler('HYPERLIQUID___SWAP', _hyperliquid_balance_handler)
    registry.register_stream('HYPERLIQUID___SWAP', 'subscribe', _hyperliquid_swap_subscribe_handler)

    registry.register_feed('HYPERLIQUID___SPOT', HyperliquidRequestDataSpot)
    registry.register_exchange_data('HYPERLIQUID___SPOT', HyperliquidExchangeDataSpot)
    registry.register_balance_handler('HYPERLIQUID___SPOT', _hyperliquid_balance_handler)
    registry.register_stream('HYPERLIQUID___SPOT', 'subscribe', _hyperliquid_spot_subscribe_handler)
