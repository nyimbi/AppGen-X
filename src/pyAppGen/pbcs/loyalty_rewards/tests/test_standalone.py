"""Focused standalone tests for the loyalty_rewards PBC."""

from ..standalone import LoyaltyRewardsStandaloneApp
from ..standalone import smoke_test
from ..ui import loyalty_rewards_standalone_app_contract


def test_standalone_manifest_and_smoke():
    contract = loyalty_rewards_standalone_app_contract()
    result = smoke_test()

    assert contract["ok"] is True
    assert contract["forms"]
    assert contract["wizards"]
    assert contract["controls"]
    assert result["ok"] is True
    assert not result["side_effects"]


def test_standalone_app_can_render_and_dispatch():
    app = LoyaltyRewardsStandaloneApp()
    rendered = app.render_workbench(tenant="tenant_alpha")
    service_contract = app.dispatch("GET", "/loyalty-rewards/service-contract", {})

    assert rendered["ok"] is True
    assert rendered["workbench"]["cards"]
    assert service_contract["ok"] is True
    assert service_contract["result"]["result"]["pbc"] == "loyalty_rewards"
