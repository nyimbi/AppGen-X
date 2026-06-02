"""Standalone and repository smoke tests for transportation_management."""

from __future__ import annotations

from ..repository import TransportationManagementRepository
from ..repository import transportation_management_repository_contract
from ..standalone import TransportationManagementStandaloneApp
from ..standalone import smoke_test
from ..ui import transportation_management_standalone_app_contract


def test_standalone_manifest_repository_and_smoke():
    contract = transportation_management_standalone_app_contract()
    repository_contract = transportation_management_repository_contract()
    app_smoke = smoke_test()
    assert contract["ok"] is True
    assert repository_contract["ok"] is True
    assert app_smoke["ok"] is True
    assert contract["forms"]
    assert contract["wizards"]
    assert contract["controls"]
    assert repository_contract["form_bindings"]


def test_standalone_app_can_execute_shipment_to_delivery_flow():
    app = TransportationManagementStandaloneApp()
    loaded = app.load_demo_workspace(tenant="tenant_standalone")
    rendered = app.render_workbench(tenant="tenant_standalone")
    repository = TransportationManagementRepository(app.state).read_model("tenant_standalone")
    binding = TransportationManagementRepository(app.state).form_binding_plan("dispatch_tracking_form")

    assert loaded["ok"] is True
    assert rendered["ok"] is True
    assert rendered["workbench"]["cards"][0]["value"] == 1
    assert rendered["shell"]["app_id"] == "transportation_management_one_pbc_app"
    assert repository["shipment"]["shipment_count"] == 1
    assert repository["shipment"]["delivered_count"] == 1
    assert repository["carrier"]["carrier_count"] == 2
    assert repository["route"]["route_count"] == 1
    assert repository["tracking"]["tracking_event_count"] == 1
    assert binding["ok"] is True
    assert loaded["telematics_route"]["route"] == "appgen_outbox"
    assert loaded["delivery_proof"]["proof"].startswith("zk_delivery_")
