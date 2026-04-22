"""
Hyperliquid error translator.
"""

from __future__ import annotations

from bt_api_base.error import ErrorTranslator, UnifiedErrorCode


class HyperliquidErrorTranslator(ErrorTranslator):
    """Translate Hyperliquid API errors to unified error codes."""

    @staticmethod
    def translate_error(error_msg: str) -> tuple[str, int]:
        """Translate Hyperliquid error to unified error code."""
        error_msg_lower = error_msg.lower()

        if 'invalid signature' in error_msg_lower:
            return ('INVALID_SIGNATURE', UnifiedErrorCode.INVALID_SIGNATURE.value)
        elif 'insufficient margin' in error_msg_lower:
            return ('INSUFFICIENT_MARGIN', UnifiedErrorCode.INSUFFICIENT_MARGIN.value)
        elif 'order not found' in error_msg_lower:
            return ('ORDER_NOT_FOUND', UnifiedErrorCode.ORDER_NOT_FOUND.value)
        elif 'rate limit' in error_msg_lower or 'too many requests' in error_msg_lower:
            return ('RATE_LIMIT_EXCEEDED', UnifiedErrorCode.RATE_LIMIT_EXCEEDED.value)
        elif 'price slippage' in error_msg_lower:
            return ('PRICE_SLIPPAGE', UnifiedErrorCode.PRICE_SLIPPAGE.value)
        elif 'min trade size' in error_msg_lower:
            return ('MIN_NOTIONAL', UnifiedErrorCode.MIN_NOTIONAL.value)
        elif 'invalid api key' in error_msg_lower:
            return ('INVALID_API_KEY', UnifiedErrorCode.INVALID_API_KEY.value)
        elif 'permission denied' in error_msg_lower:
            return ('PERMISSION_DENIED', UnifiedErrorCode.PERMISSION_DENIED.value)
        else:
            return ('UNKNOWN_ERROR', UnifiedErrorCode.UNKNOWN_ERROR.value)
