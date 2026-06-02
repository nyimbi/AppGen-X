"""Standalone one-PBC payment orchestration application tests."""
from .. import agent, controls, forms, release_evidence, routes, standalone, ui, wizards
from ..repository import PaymentOrchestrationStandaloneRepository, standalone_repository_contract, standalone_repository_smoke_test
from ..services import PaymentOrchestrationStandaloneService, standalone_service_operation_contracts


def test_forms_wizards_and_controls_are_executable():
    assert forms.smoke_test()["ok"] is True
    assert wizards.smoke_test()["ok"] is True
    assert controls.smoke_test()["ok"] is True
    assert "payment_capture" in forms.payment_orchestration_form_catalog()["form_ids"]
    assert "authorize_capture_settle" in wizards.payment_orchestration_wizard_catalog()["wizard_ids"]


def test_repository_persists_seeded_payment_workspace():
    repo=PaymentOrchestrationStandaloneRepository()
    try:
        seeded=repo.seed_demo_workspace(tenant="tenant_demo")
        read_model=repo.read_model("tenant_demo")
        counts=repo.activity_counts("tenant_demo")
        assert seeded["ok"] is True
        assert read_model["ok"] is True
        assert read_model["intent_count"] == 1
        assert read_model["captured_count"] == 1
        assert read_model["settlement_count"] == 1
        assert read_model["payout_count"] == 1
        assert read_model["refund_count"] == 1
        assert read_model["dispute_count"] == 1
        assert counts["forms"] >= 7
        assert counts["workflows"] >= 7
        assert counts["controls"] >= 2
        assert counts["agent_sessions"] == 1
    finally:
        repo.close()


def test_standalone_routes_ui_agent_and_release_evidence():
    repo=PaymentOrchestrationStandaloneRepository(); service=PaymentOrchestrationStandaloneService(repo)
    try:
        seed_route=routes.dispatch_standalone_route("POST","/app/payment-orchestration/demo-workspace",{"tenant":"tenant_demo"},service=service)
        workbench_route=routes.dispatch_standalone_route("GET","/app/payment-orchestration/workbench",{"tenant":"tenant_demo"},service=service)
        proof_route=routes.dispatch_standalone_route("POST","/app/payment-orchestration/proofs",{"tenant":"tenant_demo","intent_id":"pi_demo_100","disclosure":("intent_id","amount","currency","status")},service=service)
        rendered=ui.payment_orchestration_render_standalone_workbench(workbench_route["result"])
        workspace=agent.standalone_agent_workspace_contract()
        document_plan=agent.document_instruction_plan("capture payment pi_demo_100 amount 125.5", "settle and payout the payment")
        crud_plan=agent.datastore_crud_plan("read", "payment_orchestration_workbench_read_model", {"tenant":"tenant_demo"})
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
    assert standalone.payment_orchestration_standalone_app_contract()["ok"] is True
    assert standalone.payment_orchestration_standalone_app_smoke()["ok"] is True
    assert standalone.standalone_release_snapshot()["ok"] is True
