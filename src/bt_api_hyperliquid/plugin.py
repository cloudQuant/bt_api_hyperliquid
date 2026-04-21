from __future__ import annotations

from typing import Any

from bt_api_base.gateway.registrar import GatewayRuntimeRegistrar
from bt_api_base.plugins.protocol import PluginInfo
from bt_api_base.registry import ExchangeRegistry

from bt_api_hyperliquid import __version__
from bt_api_hyperliquid.registry_registration import register_hyperliquid


def register_plugin(
    registry: type[ExchangeRegistry], runtime_factory: type[GatewayRuntimeRegistrar]
) -> PluginInfo:
    register_hyperliquid(registry)

    return PluginInfo(
        name="bt_api_hyperliquid",
        version=__version__,
        core_requires=">=0.15,<1.0",
        supported_exchanges=("HYPERLIQUID___SPOT", "HYPERLIQUID___SWAP"),
        supported_asset_types=("SPOT", "SWAP"),
    )
