import pytest
from bt_api_hyperliquid.feeds.live_hyperliquid.request_base import HyperliquidRequestData
def test_hyperliquid_accepts_public_private_key_aliases() -> None:
    request_data = HyperliquidRequestData(
        public_key="public-key",
        private_key="0x59c6995e998f97a5a0044966f0945382d6f7d28e17f72c0f0f6f7d7f9d1c1b11",
    )

    assert request_data.api_key == "public-key"
    assert request_data.private_key.startswith("0x59c699")
    assert request_data.address is not None
