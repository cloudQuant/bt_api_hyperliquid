"""Tests for HyperliquidExchangeData container."""

from __future__ import annotations

from bt_api_hyperliquid.exchange_data import HyperliquidExchangeDataSpot


class TestHyperliquidExchangeData:
    """Tests for HyperliquidExchangeData."""

    def test_init(self):
        """Test initialization."""
        exchange = HyperliquidExchangeDataSpot()

        assert exchange.exchange_name == "hyperliquid_spot"
