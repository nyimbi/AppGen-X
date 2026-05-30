"""Standalone one-PBC checkout application tests."""

from .. import agent, release_evidence, routes, standalone, ui
from ..repository import CheckoutProcessingStandaloneRepository, standalone_repository_contract, standalone_repository_smoke_test
from ..services import CheckoutProcessingStandaloneService, standalone_service_operation_contracts


def test_repository_persists_seeded_checkout_workspace():
    repo = CheckoutProcessingStandaloneRepository()
    try:
        seeded = repo.seed_demo_workspace(tenant="tenant_demo")
        read_model = repo.read_model("tenant_demo")
        counts = repo.activity_counts("tenant_demo")

        assert seeded["ok"] is True
        assert read_model["ok"] is True
        assert read_model["completed_checkout_count"] == 1
        assert read_model["confirmed_inventory_count"] == 1
        assert read_model["captured_payment_count"] == 1
        assert read_model["promotion_redemption_count"] == 1
        assert counts["forms"] >= 4
        assert counts["workflows"] >= 8
        assert counts["controls"] >= 2
        assert counts["agent_sessions"] == 1
    finally:
        repo.close()


def test_standalone_routes_ui_agent_and_release_evidence():
    repo = CheckoutProcessingStandaloneRepository()
    service = CheckoutProcessingStandaloneService(repo)
    try:
        service_contracts = standalone_service_operation_contracts()
        route_contracts = routes.standalone_route_contracts()
        seed_route = routes.dispatch_standalone_route(
            "POST",
            "/app/checkout-processing/demo-workspace",
            {"tenant": "tenant_demo"},
            service=service,
        )
        workbench_route = routes.dispatch_standalone_route(
            "GET",
            "/app/checkout-processing/workbench",
            {"tenant": "tenant_demo"},
            service=service,
        )
        proof_route = routes.dispatch_standalone_route(
            "POST",
            "/app/checkout-processing/proofs",
            {"tenant": "tenant_demo", "session_id": "chk_demo_100", "disclosure": ("session_id", "order_id", "status", "total")},
            service=service,
        )
        rendered = ui.checkout_processing_render_standalone_workbench(workbench_route["result"])
        workspace = agent.standalone_agent_workspace_contract()
        document_plan = agent.document_instruction_plan(
            "Checkout note for cart_demo_100 and card authorization.",
            "Create and complete the checkout session.",
            target_entity="checkout_session",
            requested_action="create",
        )
        crud_plan = agent.datastore_crud_plan("read", "checkout_processing_workbench_read_model", {"tenant": "tenant_demo"})
        evidence = release_evidence.build_release_evidence()

        assert service_contracts["ok"] is True
        assert route_contracts["ok"] is True
        assert seed_route["ok"] is True
        assert workbench_route["ok"] is True
        assert proof_route["ok"] is True
        assert rendered["ok"] is True
        assert workspace["ok"] is True
        assert document_plan["ok"] is True
        assert document_plan["wizard_candidates"]
        assert document_plan["standalone_routes"]
        assert crud_plan["ok"] is True
        assert evidence["standalone_app"]["ok"] is True
        assert evidence["standalone_repository"]["ok"] is True
        assert evidence["documentation"]["ok"] is True
    finally:
        service.close()


def test_standalone_contracts_and_smoke_are_executable():
    repo_contract = standalone_repository_contract()
    repo_smoke = standalone_repository_smoke_test()
    app_contract = standalone.checkout_processing_standalone_app_contract()
    app_smoke = standalone.checkout_processing_standalone_app_smoke()
    snapshot = standalone.standalone_release_snapshot()

    assert repo_contract["ok"] is True
    assert repo_smoke["ok"] is True
    assert app_contract["ok"] is True
    assert app_smoke["ok"] is True
    assert snapshot["ok"] is True
    assert not repo_contract["side_effects"]
    assert not app_contract["side_effects"]
