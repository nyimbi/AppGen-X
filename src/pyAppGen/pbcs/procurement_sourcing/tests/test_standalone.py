"""Standalone and repository smoke tests for procurement_sourcing."""

from __future__ import annotations

from ..repository import ProcurementSourcingRepository
from ..repository import procurement_sourcing_repository_contract
from ..standalone import ProcurementSourcingStandaloneApp
from ..standalone import smoke_test
from ..ui import procurement_sourcing_standalone_app_contract


def test_standalone_manifest_repository_and_smoke():
    contract = procurement_sourcing_standalone_app_contract()
    repository_contract = procurement_sourcing_repository_contract()
    app_smoke = smoke_test()
    assert contract["ok"] is True
    assert repository_contract["ok"] is True
    assert app_smoke["ok"] is True
    assert contract["forms"]
    assert contract["wizards"]
    assert contract["controls"]
    assert repository_contract["form_bindings"]


def test_standalone_app_can_bootstrap_render_and_project_repository_views():
    app = ProcurementSourcingStandaloneApp()
    loaded = app.load_demo_workspace(tenant="tenant_standalone")
    rendered = app.render_workbench(tenant="tenant_standalone")
    repository = ProcurementSourcingRepository(app.state).read_model("tenant_standalone")
    binding = ProcurementSourcingRepository(app.state).form_binding_plan("supplier_bid_form")

    assert loaded["ok"] is True
    assert rendered["ok"] is True
    assert rendered["workbench"]["cards"][0]["value"] == 1
    assert rendered["shell"]["app_id"] == "procurement_sourcing_one_pbc_app"
    assert repository["requisition"]["requisition_count"] == 1
    assert repository["sourcing"]["rfq_count"] == 1
    assert repository["sourcing"]["bid_count"] == 3
    assert repository["award"]["award_count"] == 1
    assert repository["contracting"]["purchase_order_count"] == 1
    assert binding["ok"] is True
    assert loaded["route"]["route"] == "appgen_outbox"
    assert loaded["supplier_compliance_proof"]["proof"].startswith("zk_supplier_")
