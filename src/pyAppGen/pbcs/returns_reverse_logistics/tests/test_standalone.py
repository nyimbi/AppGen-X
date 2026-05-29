"""Standalone one-PBC returns reverse logistics application tests."""
from .. import agent, controls, forms, release_evidence, routes, standalone, ui, wizards
from ..repository import ReturnsReverseLogisticsStandaloneRepository, standalone_repository_contract, standalone_repository_smoke_test
from ..services import ReturnsReverseLogisticsStandaloneService, standalone_service_operation_contracts


def test_forms_wizards_and_controls_are_executable():
    assert forms.smoke_test()["ok"] is True
    assert wizards.smoke_test()["ok"] is True
    assert controls.smoke_test()["ok"] is True
    assert "return_authorization" in forms.returns_reverse_logistics_form_catalog()["form_ids"]
    assert "receipt_inspection_disposition" in wizards.returns_reverse_logistics_wizard_catalog()["wizard_ids"]


def test_repository_persists_seeded_returns_workspace():
    repo=ReturnsReverseLogisticsStandaloneRepository()
    try:
        seeded=repo.seed_demo_workspace(tenant="tenant_demo")
        read_model=repo.read_model("tenant_demo")
        counts=repo.activity_counts("tenant_demo")
        assert seeded["ok"] is True
        assert read_model["ok"] is True
        assert read_model["return_count"] == 1
        assert read_model["label_count"] == 1
        assert read_model["receipt_count"] == 1
        assert read_model["inspection_count"] == 1
        assert read_model["credit_count"] == 1
        assert read_model["customer_status_count"] == 1
        assert read_model["exception_count"] == 1
        assert read_model["dead_letter_count"] == 1
        assert counts["forms"] >= 9
        assert counts["workflows"] >= 4
        assert counts["controls"] >= 2
        assert counts["agent_sessions"] == 1
    finally:
        repo.close()


def test_standalone_routes_ui_agent_and_release_evidence():
    repo=ReturnsReverseLogisticsStandaloneRepository(); service=ReturnsReverseLogisticsStandaloneService(repo)
    try:
        seed_route=routes.dispatch_standalone_route("POST","/app/returns-reverse-logistics/demo-workspace",{"tenant":"tenant_demo"},service=service)
        workbench_route=routes.dispatch_standalone_route("GET","/app/returns-reverse-logistics/workbench",{"tenant":"tenant_demo"},service=service)
        proof_route=routes.dispatch_standalone_route("POST","/app/returns-reverse-logistics/proofs",{"tenant":"tenant_demo","return_id":"ret_demo_100","disclosure":("return_id","order_id","status")},service=service)
        rendered=ui.returns_reverse_logistics_render_standalone_workbench(workbench_route["result"])
        workspace=agent.standalone_agent_workspace_contract()
        document_plan=agent.document_instruction_plan("RMA return ret_demo_100 order order_demo_100", "inspect return and issue credit refund")
        crud_plan=agent.datastore_crud_plan("read", "returns_reverse_logistics_workbench_read_model", {"tenant":"tenant_demo"})
        evidence=release_evidence.build_release_evidence()
        assert standalone_service_operation_contracts()["ok"] is True
        assert routes.standalone_route_contracts()["ok"] is True
        assert seed_route["ok"] is True
        assert workbench_route["ok"] is True
        assert proof_route["ok"] is True
        assert rendered["ok"] is True
        assert workspace["ok"] is True
        assert document_plan["ok"] is True and document_plan["wizard_candidates"] and document_plan["standalone_routes"]
        assert crud_plan["ok"] is True
        assert evidence["standalone_app"]["ok"] is True
        assert evidence["documentation"]["ok"] is True
    finally:
        service.close()


def test_standalone_contracts_and_smoke_are_executable():
    assert standalone_repository_contract()["ok"] is True
    assert standalone_repository_smoke_test()["ok"] is True
    assert standalone.returns_reverse_logistics_standalone_app_contract()["ok"] is True
    assert standalone.returns_reverse_logistics_standalone_app_smoke()["ok"] is True
    assert standalone.standalone_release_snapshot()["ok"] is True
