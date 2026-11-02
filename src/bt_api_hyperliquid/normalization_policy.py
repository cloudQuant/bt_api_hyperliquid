"""HYPERLIQUID legacy normalization policy exposed through the SDK."""

from types import MappingProxyType

from bt_api_base.normalization_policy import LegacyOrderProvenancePolicy
from bt_api_base.order_provenance_fields import (
    NEUTRAL_ORDER_SOURCE_FIELDS,
    PROVIDER_SCOPED_ORDER_PROVENANCE_SCHEMAS,
)
from bt_api_base.provider_order_source_aliases import build_provider_order_source_aliases


class ProviderNormalizationPolicy(LegacyOrderProvenancePolicy):
    trade_id_fields = ("trade_id", "fill_id", "deal_id", "tid")
    tick_trading_day_fields = ("trading_day",)
    tick_action_day_fields = ("action_day",)
    order_status_fields = ("status", "order_status", "state")
    order_provenance_schemas = PROVIDER_SCOPED_ORDER_PROVENANCE_SCHEMAS
    order_provenance_source_fields = NEUTRAL_ORDER_SOURCE_FIELDS | frozenset({
        "filledSz", "limit_px", "oid", "orderOid", "px", "sz", "tid",
    })
    risk_order_native_aliases = {
        "provider_order_id": ("oid",), "filled_quantity": ("filledSz",),
        "quantity": ("sz",), "price": ("limit_px",),
    }
    group_order_native_aliases = {
        "order_id": ("oid",), "filled": ("filledSz",),
        "quantity": ("sz",), "price": ("limit_px",),
    }
    group_fill_native_aliases = {
        "trade_id": ("tid",), "order_id": ("orderOid",),
        "quantity": ("sz",), "price": ("px",),
    }
    (
        risk_order_source_aliases,
        group_order_source_aliases,
        group_fill_source_aliases,
    ) = build_provider_order_source_aliases(
        order_provenance_source_fields,
        risk_order_native_aliases=risk_order_native_aliases,
        group_order_native_aliases=group_order_native_aliases,
        group_fill_native_aliases=group_fill_native_aliases,
    )
    # Preserve the former shared response alias pending venue-specific review.
    response_error_item_fields = ("sCode",)
    # Preserve the legacy symbols container pending provider-specific review.
    result_collection_fields = ("data", "symbols")
    # Other legacy field choices stay inherited until separately assigned.
    base_symbol_fields = (
        "symbol", "symbol_name", "instrument", "instrument_id", "data_name",
        "trade_symbol",
    )
    balance_fields = MappingProxyType({
        **LegacyOrderProvenancePolicy.balance_fields,
        "margin_used": ("margin_used", "used_margin", "initialMargin"),
    })


def normalization_policy(exchange_name):
    """Return this provider's policy for its explicitly registered routes."""
    return ProviderNormalizationPolicy()


__all__ = ("ProviderNormalizationPolicy", "normalization_policy")
