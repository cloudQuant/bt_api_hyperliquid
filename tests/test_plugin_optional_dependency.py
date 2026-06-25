from __future__ import annotations

import pytest

from bt_api_base.gateway.registrar import GatewayRuntimeRegistrar
from bt_api_base.plugins.errors import PluginOptionalDependencyError
from bt_api_base.plugins.loader import PluginLoader
from bt_api_base.registry import ExchangeRegistry


class _EntryPoint:
    name = "hyperliquid"
    module = "bt_api_hyperliquid.plugin"

    @staticmethod
    def load():
        from bt_api_hyperliquid.plugin import register_plugin

        return register_plugin


def setup_function() -> None:
    ExchangeRegistry.clear()
    GatewayRuntimeRegistrar.clear()


def teardown_function() -> None:
    ExchangeRegistry.clear()
    GatewayRuntimeRegistrar.clear()


def test_entry_point_load_does_not_import_optional_dependencies() -> None:
    assert callable(_EntryPoint.load())


def test_loader_records_missing_eth_account_as_optional_skip(monkeypatch) -> None:
    try:
        import eth_account  # noqa: F401
    except ModuleNotFoundError:
        pass
    else:
        pytest.skip("eth_account is installed")

    loader = PluginLoader(ExchangeRegistry, GatewayRuntimeRegistrar)
    monkeypatch.setattr(loader, "_discover_entry_points", lambda group: [_EntryPoint()])

    loader.load_all()

    assert loader.failed == {}
    assert "hyperliquid" in loader.skipped
    assert isinstance(loader.skipped["hyperliquid"], PluginOptionalDependencyError)
