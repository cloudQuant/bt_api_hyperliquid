"""Module-level docstring."""
import pytest
from bt_api_hyperliquid.feeds.live_hyperliquid.request_base import HyperliquidRequestData
def test_hyperliquid_accepts_public_private_key_aliases() -> None:
    """test_hyperliquid_accepts_public_private_key_aliases function"""
    request_data = HyperliquidRequestData(
        public_key="public-key",
        private_key="0x59c6995e998f97a5a0044966f0945382d6f7d28e17f72c0f0f6f7d7f9d1c1b11",
    )

    assert request_data.api_key == "public-key"
    assert request_data.private_key.startswith("0x59c699")
    assert request_data.address is not None


def _make_hyperliquid_request_data() -> HyperliquidRequestData:
    return HyperliquidRequestData(
        public_key="public-key",
        private_key="0x59c6995e998f97a5a0044966f0945382d6f7d28e17f72c0f0f6f7d7f9d1c1b11",
    )


def test_hyperliquid_error_response_raises_invalid_signature() -> None:
    """API 错误(status == err)必须翻译为 UnifiedError 并抛出。"""
    from bt_api_base.error import UnifiedError

    request_data = _make_hyperliquid_request_data()
    with pytest.raises(UnifiedError):
        request_data._raise_if_error({"status": "err", "response": "Invalid signature"})


def test_hyperliquid_error_response_raises_insufficient_margin() -> None:
    from bt_api_base.error import UnifiedError

    request_data = _make_hyperliquid_request_data()
    with pytest.raises(UnifiedError):
        request_data._raise_if_error(
            {"status": "err", "response": "Insufficient margin"}
        )


def test_hyperliquid_error_response_raises_rate_limit() -> None:
    from bt_api_base.error import UnifiedError

    request_data = _make_hyperliquid_request_data()
    with pytest.raises(UnifiedError):
        request_data._raise_if_error(
            {"status": "err", "response": "Rate limit exceeded"}
        )


def test_hyperliquid_success_response_does_not_raise() -> None:
    """成功响应(无 status == err)不抛异常。"""
    request_data = _make_hyperliquid_request_data()
    request_data._raise_if_error({"mid": "64000.5"})
