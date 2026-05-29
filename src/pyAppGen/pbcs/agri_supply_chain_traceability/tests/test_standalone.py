"""Standalone app smoke tests for agri_supply_chain_traceability."""

from __future__ import annotations

from ..standalone import AgriSupplyChainTraceabilityStandaloneApp
from ..standalone import smoke_test
from ..ui import agri_supply_chain_traceability_standalone_app_contract


def test_standalone_manifest_and_smoke():
    contract = agri_supply_chain_traceability_standalone_app_contract()
    app_smoke = smoke_test()
    assert contract['ok'] is True
    assert app_smoke['ok'] is True
    assert contract['forms']
    assert contract['wizards']
    assert contract['controls']


def test_standalone_app_can_bootstrap_and_render():
    app = AgriSupplyChainTraceabilityStandaloneApp()
    loaded = app.load_demo_workspace(tenant='tenant_standalone')
    rendered = app.render_workbench(tenant='tenant_standalone')
    assert loaded['ok'] is True
    assert rendered['ok'] is True
    assert any(card['key'] == 'farm_lots' and card['value'] >= 1 for card in rendered['workbench']['cards'])
    assert any(card['key'] == 'release_decisions' and card['value'] >= 1 for card in rendered['workbench']['cards'])
    assert rendered['shell']['app_id'] == 'agri_supply_chain_traceability_one_pbc_app'
    assert rendered['release_gate_panel']['release_status'] == 'approved'
