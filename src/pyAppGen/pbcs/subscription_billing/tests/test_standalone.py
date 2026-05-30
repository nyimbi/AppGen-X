"""Standalone one-PBC subscription billing application tests."""
from .. import agent, controls, forms, release_evidence, routes, standalone, ui, wizards
from ..repository import SubscriptionBillingStandaloneRepository, standalone_repository_contract, standalone_repository_smoke_test
from ..services import SubscriptionBillingStandaloneService, standalone_service_operation_contracts


def test_forms_wizards_and_controls_are_executable():
    assert forms.smoke_test()["ok"] is True
    assert wizards.smoke_test()["ok"] is True
    assert controls.smoke_test()["ok"] is True
    assert "invoice" in forms.subscription_billing_form_catalog()["form_ids"]
    assert "usage_to_invoice" in wizards.subscription_billing_wizard_catalog()["wizard_ids"]


def test_repository_persists_seeded_subscription_workspace():
    repo=SubscriptionBillingStandaloneRepository()
    try:
        seeded=repo.seed_demo_workspace(tenant="tenant_demo")
        read_model=repo.read_model("tenant_demo")
        counts=repo.activity_counts("tenant_demo")
        assert seeded["ok"] is True
        assert read_model["ok"] is True
        assert read_model["subscription_count"] == 1
        assert read_model["invoice_count"] == 1
        assert read_model["paid_invoice_count"] == 1
        assert read_model["usage_count"] == 1
        assert read_model["credit_memo_count"] == 1
        assert read_model["payment_application_count"] >= 1
        assert read_model["entitlement_count"] == 1
        assert read_model["revenue_schedule_count"] == 2
        assert read_model["exception_count"] == 1
        assert counts["forms"] >= 10
        assert counts["workflows"] >= 8
        assert counts["controls"] == 1
        assert counts["agent_sessions"] == 1
    finally:
        repo.close()


def test_standalone_routes_ui_agent_and_release_evidence():
    repo=SubscriptionBillingStandaloneRepository(); service=SubscriptionBillingStandaloneService(repo)
    try:
        seed_route=routes.dispatch_standalone_route("POST","/app/subscription-billing/demo-workspace",{"tenant":"tenant_demo"},service=service)
        workbench_route=routes.dispatch_standalone_route("GET","/app/subscription-billing/workbench",{"tenant":"tenant_demo"},service=service)
        rendered=ui.subscription_billing_render_standalone_workbench(workbench_route["result"])
        workspace=agent.standalone_agent_workspace_contract()
        document_plan=agent.document_instruction_plan("generate invoice for sub_demo_100", "apply payment and recognize revenue")
        crud_plan=agent.datastore_crud_plan("read", "subscription_billing_workbench_read_model", {"tenant":"tenant_demo"})
        evidence=release_evidence.build_release_evidence()
        assert standalone_service_operation_contracts()["ok"] is True
        assert routes.standalone_route_contracts()["ok"] is True
        assert seed_route["ok"] is True
        assert workbench_route["ok"] is True
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
    assert standalone.subscription_billing_standalone_app_contract()["ok"] is True
    assert standalone.subscription_billing_standalone_app_smoke()["ok"] is True
    assert standalone.standalone_release_snapshot()["ok"] is True
