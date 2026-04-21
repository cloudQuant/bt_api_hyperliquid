from __future__ import annotations

import json
import time

from bt_api_base.containers.balances.balance import BalanceData
from bt_api_base.functions.utils import from_dict_get_float
from bt_api_base.logging_factory import get_logger

logger = get_logger("container")


class HyperliquidSwapRequestBalanceData(BalanceData):
    """Hyperliquid perpetual swap balance data."""

    def __init__(self, balance_info, symbol_name, asset_type, has_been_json_encoded=False):
        super().__init__(balance_info, has_been_json_encoded)
        self.exchange_name = "HYPERLIQUID"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.balance_data = balance_info if has_been_json_encoded else None
        self.coin = None
        self.total = None
        self.available = None
        self.hold = None
        self.initial_margin = None
        self.margin_used = None
        self.unrealized_pnl = None
        self.unrealized_pnl_ratio = None
        self.leverage = None
        self.account_value = None
        self.all_data = None
        self.has_been_init_data = False

    def init_data(self):
        if self.has_been_init_data:
            return self

        try:
            if not self.has_been_json_encoded:
                self.balance_data = json.loads(self.balance_info)

            if isinstance(self.balance_data, dict):
                if "assetPositions" in self.balance_data:
                    for position in self.balance_data["assetPositions"]:
                        if position.get("coin") == self.symbol_name:
                            pos = position.get("position", {})
                            self.coin = pos.get("coin")
                            self.total = from_dict_get_float(pos, "sz")
                            self.available = from_dict_get_float(pos, "free collateral")
                            self.hold = from_dict_get_float(pos, "margin held")
                            self.unrealized_pnl = from_dict_get_float(pos, "unrealizedPnl")

                            if "leverage" in pos and isinstance(pos["leverage"], dict):
                                self.leverage = from_dict_get_float(pos["leverage"], "value")

                if "marginSummary" in self.balance_data:
                    margin_summary = self.balance_data["marginSummary"]
                    self.account_value = from_dict_get_float(margin_summary, "accountValue")
                    self.margin_used = from_dict_get_float(margin_summary, "totalMarginUsed")
                    self.initial_margin = from_dict_get_float(margin_summary, "initialMargin")

            self.has_been_init_data = True

        except Exception as e:
            logger.error(f"Error initializing Hyperliquid balance data: {e}", exc_info=True)

        return self

    def get_all_data(self):
        if self.all_data is None:
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "asset_type": self.asset_type,
                "local_update_time": self.local_update_time,
                "coin": self.coin,
                "total": self.total,
                "available": self.available,
                "hold": self.hold,
                "initial_margin": self.initial_margin,
                "margin_used": self.margin_used,
                "unrealized_pnl": self.unrealized_pnl,
                "unrealized_pnl_ratio": self.unrealized_pnl_ratio,
                "leverage": self.leverage,
                "account_value": self.account_value,
            }
        return self.all_data

    def get_exchange_name(self):
        return self.exchange_name

    def get_local_update_time(self):
        return self.local_update_time

    def get_symbol_name(self):
        return self.symbol_name

    def get_asset_type(self):
        return self.asset_type

    def get_coin(self):
        return self.coin

    def get_total(self):
        return self.total

    def get_available(self):
        return self.available

    def get_hold(self):
        return self.hold

    def get_initial_margin(self):
        return self.initial_margin

    def get_margin_used(self):
        return self.margin_used

    def get_unrealized_pnl(self):
        return self.unrealized_pnl

    def get_unrealized_pnl_ratio(self):
        return self.unrealized_pnl_ratio

    def get_leverage(self):
        return self.leverage

    def get_account_value(self):
        return self.account_value

    def __str__(self):
        return f"HyperliquidSwapRequestBalanceData(coin={self.coin}, total={self.total}, available={self.available}, pnl={self.unrealized_pnl})"


class HyperliquidSpotRequestBalanceData(BalanceData):
    """Hyperliquid spot balance data."""

    def __init__(self, balance_info, symbol_name, asset_type, has_been_json_encoded=False):
        super().__init__(balance_info, has_been_json_encoded)
        self.exchange_name = "HYPERLIQUID"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.balance_data = balance_info if has_been_json_encoded else None
        self.coin = None
        self.total = None
        self.available = None
        self.hold = None
        self.all_data = None
        self.has_been_init_data = False

    def init_data(self):
        if self.has_been_init_data:
            return self

        try:
            if not self.has_been_json_encoded:
                self.balance_data = json.loads(self.balance_info)

            if isinstance(self.balance_data, dict) and "balances" in self.balance_data:
                for balance in self.balance_data["balances"]:
                    if balance.get("coin") == self.symbol_name:
                        self.coin = balance.get("coin")
                        self.total = from_dict_get_float(balance, "total")
                        self.available = from_dict_get_float(balance, "free")
                        self.hold = from_dict_get_float(balance, "hold")

            self.has_been_init_data = True

        except Exception as e:
            logger.error(f"Error initializing Hyperliquid spot balance data: {e}", exc_info=True)

        return self

    def get_all_data(self):
        if self.all_data is None:
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "asset_type": self.asset_type,
                "local_update_time": self.local_update_time,
                "coin": self.coin,
                "total": self.total,
                "available": self.available,
                "hold": self.hold,
            }
        return self.all_data

    def get_exchange_name(self):
        return self.exchange_name

    def get_local_update_time(self):
        return self.local_update_time

    def get_symbol_name(self):
        return self.symbol_name

    def get_asset_type(self):
        return self.asset_type

    def get_coin(self):
        return self.coin

    def get_total(self):
        return self.total

    def get_available(self):
        return self.available

    def get_hold(self):
        return self.hold

    def __str__(self):
        return f"HyperliquidSpotRequestBalanceData(coin={self.coin}, total={self.total}, available={self.available})"
