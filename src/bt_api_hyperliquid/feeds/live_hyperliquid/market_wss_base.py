from __future__ import annotations

import json
import threading
from typing import Any

import websocket

from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_base.feeds.feed import Feed
from bt_api_base.logging_factory import get_logger


class HyperliquidMarketWssData(Feed):
    """Base class for Hyperliquid market WebSocket data."""

    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self.asset_type = kwargs.get("asset_type", "SPOT")
        self.logger_name = kwargs.get("logger_name", "hyperliquid_market_wss.log")
        self._params = kwargs.get("exchange_data")
        self.request_logger = get_logger("hyperliquid_market_wss")
        self.async_logger = get_logger("hyperliquid_market_wss")

        self.ws_url = kwargs.get(
            "ws_url", self._params.wss_url if self._params else "wss://api.hyperliquid.xyz/ws"
        )
        self.subscriptions: list[dict[str, Any]] = []
        self.is_running = False
        self.ws_thread: threading.Thread | None = None

    def _get_request_data(self, data, extra_data):
        return RequestData(data, extra_data)

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            self.process_message(data)
        except Exception as e:
            self.request_logger.error(f"Error processing WebSocket message: {e}")

    def process_message(self, data):
        pass

    def on_open(self, ws):
        self.request_logger.info("WebSocket connection opened")
        for subscription in self.subscriptions:
            ws.send(json.dumps(subscription))

    def on_error(self, ws, error):
        self.request_logger.error(f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        self.request_logger.info("WebSocket connection closed")
        self.is_running = False

    def subscribe(self, subscription):
        self.subscriptions.append(subscription)

    def start(self):
        if self.is_running:
            return
        self.is_running = True
        self.ws_thread = threading.Thread(target=self._run_websocket)
        self.ws_thread.daemon = True
        self.ws_thread.start()

    def _run_websocket(self):
        ws = websocket.WebSocketApp(
            self.ws_url,
            on_message=self.on_message,
            on_open=self.on_open,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        ws.run_forever(ping_interval=30)

    def stop(self):
        self.is_running = False
        if self.ws_thread:
            self.ws_thread.join(timeout=5)
