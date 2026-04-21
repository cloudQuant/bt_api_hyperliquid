from __future__ import annotations

from typing import Any

import requests
from eth_account import Account

from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_base.feeds.capability import Capability
from bt_api_base.feeds.feed import Feed
from bt_api_base.logging_factory import get_logger
from bt_api_base.rate_limiter import RateLimiter, RateLimitRule, RateLimitScope, RateLimitType
from bt_api_hyperliquid.exchange_data.hyperliquid_exchange_data import (
    HyperliquidExchangeDataSpot,
    HyperliquidExchangeDataSwap,
)
from bt_api_hyperliquid.errors.hyperliquid_translator import HyperliquidErrorTranslator


class HyperliquidRequestData(Feed):
    """Base class for Hyperliquid API requests."""

    @classmethod
    def _capabilities(cls) -> set[Capability]:
        return {
            Capability.GET_TICK,
            Capability.GET_DEPTH,
            Capability.GET_KLINE,
            Capability.GET_EXCHANGE_INFO,
            Capability.MAKE_ORDER,
            Capability.CANCEL_ORDER,
            Capability.QUERY_ORDER,
            Capability.QUERY_OPEN_ORDERS,
            Capability.GET_BALANCE,
            Capability.GET_ACCOUNT,
            Capability.MARKET_STREAM,
            Capability.ACCOUNT_STREAM,
        }

    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)

        self.asset_type = kwargs.get("asset_type", "SPOT")
        self.logger_name = kwargs.get("logger_name", "hyperliquid_feed.log")
        params = kwargs.get("exchange_data")
        if params is None:
            params = (
                HyperliquidExchangeDataSpot()
                if self.asset_type == "SPOT"
                else HyperliquidExchangeDataSwap()
            )
        self._params = params

        self.request_logger = get_logger("hyperliquid_feed")
        self.async_logger = get_logger("hyperliquid_feed")

        self.rate_limiter = RateLimiter(
            rules=[
                RateLimitRule(
                    name="hyperliquid_general",
                    limit=1200,
                    interval=60,
                    type=RateLimitType.SLIDING_WINDOW,
                    scope=RateLimitScope.IP,
                    endpoint="/info",
                )
            ]
        )

        self.api_key = kwargs.get("public_key") or kwargs.get("api_key", "")
        self.private_key = (
            kwargs.get("private_key") or kwargs.get("api_secret") or kwargs.get("secret_key") or ""
        )
        self.address = None

        if self.private_key:
            try:
                self.account = Account.from_key(self.private_key)
                self.address = self.account.address
            except Exception as e:
                self.request_logger.error(f"Invalid private key: {e}")

        self.error_translator = HyperliquidErrorTranslator()

    def request(self, path, params=None, body=None, extra_data=None, timeout=10, is_sign=False):
        if extra_data is None:
            extra_data = {}
        if body is None:
            body = {}

        url = self._params.rest_url + path
        headers = {"Content-Type": "application/json", "User-Agent": "bt_api_hyperliquid/1.0"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key

        response = self.http_request("POST", url, headers, body, timeout)
        return RequestData(response, extra_data)

    async def async_request(
        self, path, params=None, body=None, extra_data=None, timeout=10, is_sign=False
    ):
        if extra_data is None:
            extra_data = {}
        if body is None:
            body = {}

        url = self._params.rest_url + path
        headers = {"Content-Type": "application/json", "User-Agent": "bt_api_hyperliquid/1.0"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key

        response = self.http_request("POST", url, headers, body, timeout)
        self.async_logger.info(f"Async Request: POST {url}")
        return RequestData(response, extra_data)

    def async_callback(self, future):
        try:
            result = future.result()
            self.data_queue.put(result)
        except Exception as e:
            self.async_logger.warning(f"async_callback::{e}")

    def _make_request(self, request_type, **kwargs):
        headers = {"Content-Type": "application/json", "User-Agent": "bt_api_hyperliquid/1.0"}

        if self.api_key:
            headers["X-API-Key"] = self.api_key

        url = self._params.rest_url + self._params.get_rest_path(request_type)

        try:
            response = requests.post(url, json=kwargs, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.request_logger.error(f"Request failed: {e}")
            return {"status": "error", "message": str(e)}

    def _get_request_data(self, data, extra_data):
        return RequestData(data, extra_data)

    def _get_tick(self, symbol, extra_data=None, **kwargs):
        if extra_data is None:
            extra_data = {}
        path = self._params.get_rest_path("get_all_mids")
        body = {"type": "allMids"}
        extra_data.update(
            {
                "exchange_name": self._params.exchange_name,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "request_type": "get_tick",
            }
        )
        return path, body, extra_data

    def get_tick(self, symbol, extra_data=None, **kwargs):
        path, body, extra_data = self._get_tick(symbol, extra_data, **kwargs)
        return self.request(path, body=body, extra_data=extra_data)

    def async_get_tick(self, symbol, extra_data=None, **kwargs):
        path, body, extra_data = self._get_tick(symbol, extra_data, **kwargs)
        self.submit(
            self.async_request(path, body=body, extra_data=extra_data),
            callback=self.async_callback,
        )

    def _get_depth(self, symbol, count=20, extra_data=None, **kwargs):
        if extra_data is None:
            extra_data = {}
        path = self._params.get_rest_path("get_l2_book")
        coin = self._params.get_symbol(symbol)
        body = {"type": "l2Book", "coin": coin}
        extra_data.update(
            {
                "exchange_name": self._params.exchange_name,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "request_type": "get_depth",
            }
        )
        return path, body, extra_data

    def get_depth(self, symbol, count=20, extra_data=None, **kwargs):
        path, body, extra_data = self._get_depth(symbol, count, extra_data, **kwargs)
        return self.request(path, body=body, extra_data=extra_data)

    def async_get_depth(self, symbol, count=20, extra_data=None, **kwargs):
        path, body, extra_data = self._get_depth(symbol, count, extra_data, **kwargs)
        self.submit(
            self.async_request(path, body=body, extra_data=extra_data),
            callback=self.async_callback,
        )

    def _get_kline(self, symbol, period, count=20, extra_data=None, **kwargs):
        if extra_data is None:
            extra_data = {}
        path = self._params.get_rest_path("get_candle_snapshot")
        coin = self._params.get_symbol(symbol)
        interval = self._params.kline_periods.get(period, period)
        req = {"coin": coin, "interval": interval}
        if "start_time" in kwargs and kwargs["start_time"]:
            req["startTime"] = kwargs["start_time"]
        if "end_time" in kwargs and kwargs["end_time"]:
            req["endTime"] = kwargs["end_time"]
        body = {"type": "candleSnapshot", "req": req}
        extra_data.update(
            {
                "exchange_name": self._params.exchange_name,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "request_type": "get_kline",
            }
        )
        return path, body, extra_data

    def get_kline(self, symbol, period, count=20, extra_data=None, **kwargs):
        path, body, extra_data = self._get_kline(symbol, period, count, extra_data, **kwargs)
        return self.request(path, body=body, extra_data=extra_data)

    def async_get_kline(self, symbol, period, count=20, extra_data=None, **kwargs):
        path, body, extra_data = self._get_kline(symbol, period, count, extra_data, **kwargs)
        self.submit(
            self.async_request(path, body=body, extra_data=extra_data),
            callback=self.async_callback,
        )

    def get_exchange_info(self, extra_data=None, **kwargs):
        if extra_data is None:
            extra_data = {}
        path = self._params.get_rest_path("get_meta")
        body = {"type": "meta"}
        extra_data.update(
            {
                "exchange_name": self._params.exchange_name,
                "symbol_name": "",
                "asset_type": self.asset_type,
                "request_type": "get_exchange_info",
            }
        )
        return self.request(path, body=body, extra_data=extra_data)

    def get_server_time(self, extra_data=None, **kwargs):
        if extra_data is None:
            extra_data = {}
        path = self._params.get_rest_path("get_all_mids")
        body = {"type": "allMids"}
        extra_data.update(
            {
                "exchange_name": self._params.exchange_name,
                "symbol_name": "",
                "asset_type": self.asset_type,
                "request_type": "get_server_time",
            }
        )
        return self.request(path, body=body, extra_data=extra_data)

    def get_all_mids(self):
        body = {"type": "allMids"}
        result = self._make_request("get_all_mids", **body)
        return self._get_request_data(
            result,
            {
                "exchange_name": self._params.exchange_name,
                "symbol_name": "",
                "asset_type": self.asset_type,
                "request_type": "get_all_mids",
            },
        )

    def get_meta(self):
        body = {"type": "meta"}
        result = self._make_request("get_meta", **body)
        return self._get_request_data(
            result,
            {
                "exchange_name": self._params.exchange_name,
                "symbol_name": "",
                "asset_type": self.asset_type,
                "request_type": "get_meta",
            },
        )

    def get_spot_meta(self):
        body = {"type": "spotMeta"}
        result = self._make_request("get_spot_meta", **body)
        return self._get_request_data(
            result,
            {
                "exchange_name": self._params.exchange_name,
                "symbol_name": "",
                "asset_type": self.asset_type,
                "request_type": "get_spot_meta",
            },
        )

    def get_l2_book(self, coin, depth=5):
        body = {"type": "l2Book", "coin": coin, "level": 2}
        result = self._make_request("get_l2_book", **body)
        return self._get_request_data(
            result,
            {
                "exchange_name": self._params.exchange_name,
                "symbol_name": coin,
                "asset_type": self.asset_type,
                "request_type": "get_l2_book",
            },
        )

    def get_candle_snapshot(self, coin, interval, start_time=None, end_time=None):
        req = {"coin": coin, "interval": interval}
        if start_time:
            req["startTime"] = start_time
        if end_time:
            req["endTime"] = end_time
        body = {"type": "candleSnapshot", "req": req}
        result = self._make_request("get_candle_snapshot", **body)
        return self._get_request_data(
            result,
            {
                "exchange_name": self._params.exchange_name,
                "symbol_name": coin,
                "asset_type": self.asset_type,
                "request_type": "get_candle_snapshot",
            },
        )

    def get_recent_trades(self, coin, limit=100):
        body = {"type": "recentTrades", "coin": coin, "limit": limit}
        result = self._make_request("get_recent_trades", **body)
        return self._get_request_data(
            result,
            {
                "exchange_name": self._params.exchange_name,
                "symbol_name": coin,
                "asset_type": self.asset_type,
                "request_type": "get_recent_trades",
            },
        )

    def get_exchange_status(self):
        body = {"type": "exchangeStatus"}
        result = self._make_request("get_exchange_status", **body)
        return self._get_request_data(
            result,
            {
                "exchange_name": self._params.exchange_name,
                "symbol_name": "",
                "asset_type": self.asset_type,
                "request_type": "get_exchange_status",
            },
        )

    def get_clearinghouse_state(self, user=None):
        user = user or self.address
        if not user:
            raise ValueError("User address required for clearinghouse state")
        body = {"type": "clearinghouseState", "user": user}
        result = self._make_request("get_clearinghouse_state", **body)
        return self._get_request_data(
            result,
            {
                "exchange_name": self._params.exchange_name,
                "symbol_name": "",
                "asset_type": self.asset_type,
                "request_type": "get_clearinghouse_state",
            },
        )

    def get_spot_clearinghouse_state(self, user=None):
        user = user or self.address
        if not user:
            raise ValueError("User address required for spot clearinghouse state")
        body = {"type": "spotClearinghouseState", "user": user}
        result = self._make_request("get_spot_clearinghouse_state", **body)
        return self._get_request_data(
            result,
            {
                "exchange_name": self._params.exchange_name,
                "symbol_name": "",
                "asset_type": self.asset_type,
                "request_type": "get_spot_clearinghouse_state",
            },
        )

    def get_order_status(self, user, oid):
        body = {"type": "orderStatus", "user": user, "oid": oid}
        result = self._make_request("get_order_status", **body)
        return self._get_request_data(
            result,
            {
                "exchange_name": self._params.exchange_name,
                "symbol_name": "",
                "asset_type": self.asset_type,
                "request_type": "get_order_status",
            },
        )

    def get_user_fills(self, user, limit=100):
        body = {"type": "userFills", "user": user, "limit": limit}
        result = self._make_request("get_user_fills", **body)
        return self._get_request_data(
            result,
            {
                "exchange_name": self._params.exchange_name,
                "symbol_name": "",
                "asset_type": self.asset_type,
                "request_type": "get_user_fills",
            },
        )

    def get_user_funding(self, user):
        body = {"type": "userFunding", "user": user}
        result = self._make_request("get_user_funding", **body)
        return self._get_request_data(
            result,
            {
                "exchange_name": self._params.exchange_name,
                "symbol_name": "",
                "asset_type": self.asset_type,
                "request_type": "get_user_funding",
            },
        )

    def _make_signed_request(self, request_type, **kwargs):
        if not self.account:
            raise ValueError("Private key required for signed requests")
        headers = {"Content-Type": "application/json", "User-Agent": "bt_api_hyperliquid/1.0"}
        url = self._params.rest_url + self._params.get_rest_path(request_type)
        try:
            response = requests.post(url, json=kwargs, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.request_logger.error(f"Signed request failed: {e}")
            return {"status": "error", "message": str(e)}
