"""Standalone app smoke tests for insurance_claims_policy."""

from pyAppGen.pbcs.insurance_claims_policy.standalone import InsuranceClaimsPolicyStandaloneApp
from pyAppGen.pbcs.insurance_claims_policy.standalone import smoke_test
from pyAppGen.pbcs.insurance_claims_policy.ui import insurance_claims_policy_render_workbench
from pyAppGen.pbcs.insurance_claims_policy.ui import insurance_claims_policy_standalone_app_contract


def test_standalone_manifest_and_smoke():
    contract = insurance_claims_policy_standalone_app_contract()
    app_smoke = smoke_test()
    assert contract["ok"] is True
    assert app_smoke["ok"] is True
    assert contract["forms"]
    assert contract["wizards"]
    assert contract["controls"]


def test_standalone_app_can_bootstrap_and_render():
    app = InsuranceClaimsPolicyStandaloneApp()
    app.load_demo_workspace(tenant="tenant_standalone")
    rendered = insurance_claims_policy_render_workbench(app.state, tenant="tenant_standalone")
    assert rendered["ok"] is True
    assert rendered["workbench"]["cards"][0]["value"] >= 1
    assert rendered["shell"]["app_id"] == "insurance_claims_policy_one_pbc_app"
