from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base._compat import Self
from bt_api_base.containers.tickers.ticker import TickerData
from bt_api_base.functions.utils import from_dict_get_float
from bt_api_base.logging_factory import get_logger

logger = get_logger('container')


class HyperliquidTickerData(TickerData):
    """Hyperliquid ticker data."""

    def __init__(self, ticker_info, symbol_name, asset_type, has_been_json_encoded=False) -> None:
        super().__init__(ticker_info, has_been_json_encoded)
        self.exchange_name = 'HYPERLIQUID'
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.ticker_data: dict[str, Any] | None = ticker_info if has_been_json_encoded else None
        self.ticker_symbol_name: str | None = None
        self.server_time: float | None = None
        self.bid_price: float | None = None
        self.ask_price: float | None = None
        self.bid_volume: float | None = None
        self.ask_volume: float | None = None
        self.last_price: float | None = None
        self.last_volume: float | None = None
        self.all_data: dict[str, Any] | None = None
        self.has_been_init_data = False

    def init_data(self) -> Self:
        if self.has_been_init_data:
            return self

        try:
            if not self.has_been_json_encoded:
                self.ticker_data = json.loads(self.ticker_info)

            td = self.ticker_data or {}
            if self.asset_type == 'SWAP':
                self.ticker_symbol_name = self.symbol_name
                self.last_price = from_dict_get_float(td, self.symbol_name)
                self.bid_price = self.last_price
                self.ask_price = self.last_price
                self.last_volume = 0.0
            elif self.asset_type == 'SPOT':
                self.ticker_symbol_name = self.symbol_name
                if isinstance(self.ticker_data, dict):
                    td = self.ticker_data
                    self.last_price = from_dict_get_float(td, 'last')
                    self.bid_price = from_dict_get_float(td, 'bid')
                    self.ask_price = from_dict_get_float(td, 'ask')
                    self.last_volume = from_dict_get_float(td, 'volume')
                    self.server_time = from_dict_get_float(td, 'time')
                else:
                    self.last_price = self.ticker_data
                    self.bid_price = self.ticker_data
                    self.ask_price = self.ticker_data

            self.has_been_init_data = True

        except Exception as e:
            logger.error(f'Error initializing Hyperliquid ticker data: {e}', exc_info=True)

        return self

    def get_all_data(self) -> dict[str, Any]:
        if self.all_data is None:
            self.all_data = {
                'exchange_name': self.exchange_name,
                'symbol_name': self.symbol_name,
                'asset_type': self.asset_type,
                'local_update_time': self.local_update_time,
                'ticker_symbol_name': self.ticker_symbol_name,
                'server_time': self.server_time,
                'bid_price': self.bid_price,
                'ask_price': self.ask_price,
                'bid_volume': self.bid_volume,
                'ask_volume': self.ask_volume,
                'last_price': self.last_price,
                'last_volume': self.last_volume,
            }
        return self.all_data or {}

    def get_exchange_name(self) -> str:
        return str(self.exchange_name)

    def get_local_update_time(self) -> float:
        return float(self.local_update_time)

    def get_symbol_name(self) -> str:
        return str(self.symbol_name)

    def get_ticker_symbol_name(self) -> str | None:
        val = self.ticker_symbol_name
        return None if val is None else str(val)

    def get_asset_type(self) -> str:
        return str(self.asset_type)

    def get_server_time(self) -> float | None:
        return self.server_time

    def get_bid_price(self) -> float | None:
        return self.bid_price

    def get_ask_price(self) -> float | None:
        return self.ask_price

    def get_bid_volume(self) -> float | None:
        return self.bid_volume

    def get_ask_volume(self) -> float | None:
        return self.ask_volume

    def get_last_price(self) -> float | None:
        return self.last_price

    def get_last_volume(self) -> float | None:
        return self.last_volume

    def __str__(self) -> str:
        return (
            f'HyperliquidTickerData(symbol={self.symbol_name}, '
            f'last_price={self.last_price}, bid={self.bid_price}, '
            f'ask={self.ask_price})'
        )
