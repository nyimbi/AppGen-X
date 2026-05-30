"""Standalone and repository smoke tests for wms_core."""

from __future__ import annotations

from ..repository import WmsCoreRepository
from ..repository import wms_core_repository_contract
from ..standalone import WmsCoreStandaloneApp
from ..standalone import smoke_test
from ..ui import wms_core_standalone_app_contract


def test_standalone_manifest_repository_and_smoke():
    contract = wms_core_standalone_app_contract()
    repository_contract = wms_core_repository_contract()
    app_smoke = smoke_test()
    assert contract["ok"] is True
    assert repository_contract["ok"] is True
    assert app_smoke["ok"] is True
    assert contract["forms"]
    assert contract["wizards"]
    assert contract["controls"]
    assert repository_contract["form_bindings"]


def test_standalone_app_can_bootstrap_render_and_project_repository_views():
    app = WmsCoreStandaloneApp()
    app.load_demo_workspace(tenant="tenant_standalone")
    rendered = app.render_workbench(tenant="tenant_standalone")
    repository = WmsCoreRepository(app.state).read_model("tenant_standalone")
    binding = WmsCoreRepository(app.state).form_binding_plan("inbound_receipt_form")

    assert rendered["ok"] is True
    assert rendered["workbench"]["cards"][0]["value"] >= 1
    assert rendered["shell"]["app_id"] == "wms_core_one_pbc_app"
    assert repository["warehouse"]["warehouse_count"] == 1
    assert repository["inbound"]["receipt_count"] == 1
    assert repository["outbound"]["shipment_count"] == 1
    assert binding["ok"] is True
