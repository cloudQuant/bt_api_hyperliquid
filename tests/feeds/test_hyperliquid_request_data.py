"""Module-level docstring."""
import pytest
from bt_api_hyperliquid.feeds.live_hyperliquid.request_base import HyperliquidRequestData
def test_hyperliquid_accepts_public_key_and_address() -> None:
    """vault/agent 模式：api_key 用作 X-API-Key，address 显式传入（无私钥签名死代码）。"""
    request_data = HyperliquidRequestData(
        public_key="public-key",
        address="0x0000000000000000000000000000000000000001",
    )

    assert request_data.api_key == "public-key"
    assert request_data.address == "0x0000000000000000000000000000000000000001"
    assert not hasattr(request_data, "private_key")


def _make_hyperliquid_request_data() -> HyperliquidRequestData:
    return HyperliquidRequestData(public_key="public-key")


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
