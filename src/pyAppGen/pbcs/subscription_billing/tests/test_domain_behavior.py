"""Executable domain behavior tests for the subscription_billing PBC."""

from __future__ import annotations

import pytest

from .. import agent
from .. import release_evidence
from .. import routes
from .. import runtime
from .. import standalone
from .. import ui
from ..repository import SubscriptionBillingStandaloneRepository
from ..repository import standalone_repository_contract
from ..repository import standalone_repository_smoke_test
from ..services import SubscriptionBillingService
from ..services import SubscriptionBillingStandaloneService
from ..services import service_operation_contracts
from ..services import service_operation_manifest
from ..services import standalone_service_operation_contracts


TENANT = "tenant_alpha"
SUBSCRIPTION_ID = "sub_alpha"

CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.SUBSCRIPTION_BILLING_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "default_currency": "USD",
    "supported_currencies": ("USD", "EUR"),
    "supported_regions": ("US", "EU"),
    "billing_calendars": ("monthly", "annual"),
    "default_timezone": "UTC",
    "invoice_approval_mode": "policy",
    "workbench_limit": 100,
}

PARAMETERS = {
    "renewal_confidence_threshold": 0.72,
    "churn_risk_threshold": 0.62,
    "dunning_risk_threshold": 0.58,
    "usage_rating_precision": 4,
    "proration_rounding_precision": 2,
    "retry_limit": 3,
    "carbon_batch_window_hours": 8,
    "discount_guardrail_percent": 35.0,
    "approval_amount_threshold": 5000.0,
    "workbench_limit": 100,
}


def _configured_state() -> dict:
    state = runtime.subscription_billing_empty_state()
    state = runtime.subscription_billing_configure_runtime(state, CONFIGURATION)["state"]
    for name, value in PARAMETERS.items():
        state = runtime.subscription_billing_set_parameter(state, name, value)["state"]
    state = runtime.subscription_billing_register_rule(
        state,
        {
            "rule_id": "rule_subscription",
            "tenant": TENANT,
            "rule_type": "renewal",
            "allowed_plan_families": ("growth",),
            "allowed_currencies": ("USD",),
            "allowed_regions": ("US",),
            "renewal_policy": "auto_renew_with_payment_confirmation",
            "invoice_policy": "approve_below_threshold",
            "status": "active",
        },
    )["state"]
    state = runtime.subscription_billing_register_schema_extension(
        state,
        "subscription",
        {"contract_terms": "jsonb"},
    )["state"]
    for plan in (
        {
            "plan_id": "plan_growth",
            "tenant": TENANT,
            "family": "growth",
            "name": "Growth",
            "currency": "USD",
            "region": "US",
            "billing_period": "monthly",
            "base_price": 100.0,
            "usage_rate": 2.5,
            "included_units": 10.0,
            "status": "active",
        },
        {
            "plan_id": "plan_scale",
            "tenant": TENANT,
            "family": "growth",
            "name": "Scale",
            "currency": "USD",
            "region": "US",
            "billing_period": "monthly",
            "base_price": 180.0,
            "usage_rate": 2.0,
            "included_units": 25.0,
            "status": "active",
        },
    ):
        state = runtime.subscription_billing_register_plan(state, plan)["state"]
    state = runtime.subscription_billing_start_trial(
        state,
        {
            "trial_id": "trial_alpha",
            "tenant": TENANT,
            "customer_id": "cust_alpha",
            "plan_id": "plan_growth",
            "start_date": "2025-12-15",
            "end_date": "2025-12-31",
            "region": "US",
            "currency": "USD",
        },
    )["state"]
    state = runtime.subscription_billing_receive_event(
        state,
        {
            "event_id": "price_growth",
            "event_type": "PriceOptimized",
            "payload": {
                "tenant": TENANT,
                "plan_id": "plan_growth",
                "optimized_rate": 2.25,
                "confidence": 0.91,
            },
        },
    )["state"]
    state = runtime.subscription_billing_create_subscription(
        state,
        {
            "subscription_id": SUBSCRIPTION_ID,
            "tenant": TENANT,
            "customer_id": "cust_alpha",
            "plan_id": "plan_growth",
            "start_date": "2026-01-01",
            "renewal_date": "2026-02-01",
            "region": "US",
            "currency": "USD",
            "seats": 5,
        },
    )["state"]
    return state


def _invoiced_state() -> dict:
    state = _configured_state()
    state = runtime.subscription_billing_add_subscription_addon(
        state,
        {
            "addon_id": "addon_support",
            "tenant": TENANT,
            "subscription_id": SUBSCRIPTION_ID,
            "name": "premium_support",
            "quantity": 1,
            "unit_price": 25.0,
            "effective_date": "2026-01-01",
        },
    )["state"]
    usage = runtime.subscription_billing_record_usage(
        state,
        {
            "usage_id": "usage_alpha",
            "tenant": TENANT,
            "subscription_id": SUBSCRIPTION_ID,
            "meter_name": "api_calls",
            "quantity": 44.0,
            "occurred_at": "2026-01-14T00:00:00Z",
        },
    )
    state = usage["state"]
    invoice = runtime.subscription_billing_generate_invoice(state, SUBSCRIPTION_ID, period="2026-01")
    state = invoice["state"]
    credit = runtime.subscription_billing_issue_credit_memo(
        state,
        invoice["invoice"]["invoice_id"],
        amount=5.0,
        reason="service_credit",
    )
    state = credit["state"]
    return {"state": state, "usage": usage, "invoice": invoice, "credit": credit}


def _settled_state() -> dict:
    bundle = _invoiced_state()
    state = bundle["state"]
    invoice_id = bundle["invoice"]["invoice"]["invoice_id"]
    payment = runtime.subscription_billing_apply_payment_to_invoice(
        state,
        invoice_id,
        payment_event_id="payment_alpha_direct",
        amount=bundle["invoice"]["invoice"]["amount"],
    )
    state = payment["state"]
    renewed = runtime.subscription_billing_renew_subscription(state, SUBSCRIPTION_ID)
    state = renewed["state"]
    changed = runtime.subscription_billing_change_subscription_plan(
        state,
        SUBSCRIPTION_ID,
        target_plan_id="plan_scale",
        effective_date="2026-02-15",
        reason="growth_upgrade",
    )
    state = changed["state"]
    entitlement = runtime.subscription_billing_grant_entitlement(
        state,
        SUBSCRIPTION_ID,
        entitlement_key="premium_support",
        scope=TENANT,
    )
    state = entitlement["state"]
    revenue = runtime.subscription_billing_recognize_revenue(state, invoice_id, period="2026-01")
    state = revenue["state"]
    exception = runtime.subscription_billing_open_billing_exception(
        state,
        SUBSCRIPTION_ID,
        exception_type="usage_spike",
        severity="medium",
        description="usage increased materially above baseline",
    )
    state = exception["state"]
    resolved = runtime.subscription_billing_resolve_billing_exception(
        state,
        exception["exception"]["exception_id"],
        resolution="usage reviewed and accepted",
    )
    state = resolved["state"]
    dunning = runtime.subscription_billing_create_dunning_notice(state, SUBSCRIPTION_ID, reason="payment_watch")
    state = dunning["state"]
    return {
        **bundle,
        "state": state,
        "payment": payment,
        "renewed": renewed,
        "changed": changed,
        "entitlement": entitlement,
        "revenue": revenue,
        "exception": exception,
        "resolved": resolved,
        "dunning": dunning,
    }


def test_subscription_repository_full_billing_flow_and_release_models_are_executable() -> None:
    repository = SubscriptionBillingStandaloneRepository()
    try:
        seeded = repository.seed_demo_workspace(tenant=TENANT)
        workbench = repository.build_workbench(TENANT)
        read_model = repository.read_model(TENANT)
        state = repository.load_state(TENANT)
        controls = repository.run_control_tests(TENANT)
        rendered = ui.subscription_billing_render_standalone_workbench(workbench)
        release = runtime.subscription_billing_build_release_evidence()

        assert seeded["ok"] is True
        assert workbench["ok"] is True
        assert workbench["subscription_count"] == 1
        assert workbench["invoice_count"] == 1
        assert workbench["paid_invoice_count"] == 1
        assert workbench["usage_count"] == 1
        assert workbench["credit_memo_count"] == 1
        assert workbench["payment_application_count"] >= 1
        assert workbench["entitlement_count"] == 1
        assert workbench["revenue_schedule_count"] >= 1
        assert workbench["exception_count"] == 1
        assert workbench["activity_counts"]["forms"] >= 9
        assert workbench["activity_counts"]["workflows"] >= 7
        assert workbench["activity_counts"]["controls"] >= 1
        assert workbench["activity_counts"]["agent_sessions"] >= 1
        assert read_model["ok"] is True
        assert state["subscriptions"]["sub_demo_100"]["status"] == "cancelled"
        assert next(iter(state["invoices"].values()))["status"] == "paid"
        assert any(exception["status"] == "resolved" for exception in state["billing_exceptions"].values())
        assert controls["ok"] is True and controls["summary"]["outbox_count"] > 0
        assert rendered["ok"] is True
        assert "subscription" in rendered["forms_visible"]
        assert "usage_to_invoice" in rendered["wizards_visible"]
        assert "event_contract_locked" in rendered["controls_visible"]
        assert release["ok"] is True and not release["blocking_gaps"]
    finally:
        repository.close()


def test_subscription_routes_agent_ui_standalone_and_service_surfaces_are_executable() -> None:
    state = _settled_state()["state"]
    permissions = tuple(set(ui.subscription_billing_ui_contract()["action_permissions"].values()))
    rendered = ui.subscription_billing_render_workbench(state, tenant=TENANT, principal_permissions=permissions)
    route_validation = routes.validate_api_route_contracts()
    command_dispatch = routes.dispatch_route("POST", "/api/pbc/subscription_billing/payment-applications", {"tenant": TENANT})
    query_dispatch = routes.dispatch_route("GET", "/api/pbc/subscription_billing/subscription-billing-workbench", {"tenant": TENANT})
    service = SubscriptionBillingService()
    service_result = service.command_payment_applications({"tenant": TENANT, "subscription_id": SUBSCRIPTION_ID})
    standalone_service = SubscriptionBillingStandaloneService()
    try:
        standalone_seed = standalone_service.seed_demo_workspace(tenant=TENANT)
        standalone_workbench = standalone_service.build_workbench(tenant=TENANT)
    finally:
        standalone_service.close()
    app_contract = standalone.subscription_billing_standalone_app_contract()
    app_smoke = standalone.subscription_billing_standalone_app_smoke()
    repository_contract = standalone_repository_contract()
    repository_smoke = standalone_repository_smoke_test()
    release_validation = release_evidence.validate_release_evidence()
    skills = agent.agent_skill_manifest()
    chatbot = agent.chatbot_interface_contract()
    document_plan = agent.document_instruction_plan(
        "Subscription packet: invoice sub_alpha, rate usage, issue credit, apply payment, and renew.",
        "Prepare a governed invoice and payment mutation preview.",
    )
    crud_plan = agent.datastore_crud_plan(
        "create",
        "subscription_billing_invoice",
        {"subscription_id": SUBSCRIPTION_ID},
    )
    blocked_plan = agent.datastore_crud_plan("update", "shared_subscription_table", {})
    contribution = agent.composed_agent_contribution()

    assert rendered["ok"] is True
    assert "SubscriptionBillingWorkbench" in rendered["fragments"]
    assert any(card["key"] == "revenue" and card["value"] >= 1 for card in rendered["cards"])
    assert rendered["binding_evidence"]["outbox_table"] == "subscription_billing_appgen_outbox_event"
    assert route_validation["ok"] is True
    assert all(contract["event_contract"] == "AppGen-X" for contract in route_validation["contracts"])
    assert all(contract["stream_engine_picker_visible"] is False for contract in route_validation["contracts"])
    assert command_dispatch["ok"] is True and command_dispatch["result"]["read_only"] is False
    assert query_dispatch["ok"] is True and query_dispatch["result"]["read_only"] is True
    assert service_operation_manifest()["ok"] is True
    assert service_operation_contracts()["ok"] is True
    assert standalone_service_operation_contracts()["ok"] is True
    assert service_result["ok"] is True and service_result["emits"] == ("PaymentApplied",)
    assert standalone_seed["ok"] is True
    assert standalone_workbench["ok"] is True
    assert app_contract["ok"] is True
    assert app_smoke["ok"] is True
    assert repository_contract["deployment_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert repository_smoke["ok"] is True
    assert release_validation["ok"] is True
    assert skills["ok"] is True
    assert chatbot["ok"] is True
    assert document_plan["ok"] is True and document_plan["requires_human_confirmation"] is True
    assert document_plan["candidate_table"] == "subscription_billing_invoice"
    assert document_plan["wizard_candidates"]
    assert crud_plan["ok"] is True and crud_plan["requires_confirmation"] is True
    assert blocked_plan["ok"] is False
    assert contribution["ok"] is True
    assert "subscription_billing_crud" in contribution["dsl_tools"]


def test_subscription_event_idempotency_dead_letter_boundary_and_advanced_runtime_are_executable() -> None:
    invoiced = _invoiced_state()
    state = invoiced["state"]
    invoice_id = invoiced["invoice"]["invoice"]["invoice_id"]
    payment_event = {
        "event_id": "payment_evt_100",
        "event_type": "PaymentCaptured",
        "payload": {
            "tenant": TENANT,
            "invoice_id": invoice_id,
            "amount": invoiced["invoice"]["invoice"]["amount"],
            "currency": "USD",
        },
    }
    first = runtime.subscription_billing_receive_event(state, payment_event)
    duplicate = runtime.subscription_billing_receive_event(first["state"], payment_event)
    failing_event = {
        "event_id": "payment_evt_fail",
        "event_type": "PaymentCaptured",
        "payload": {"tenant": TENANT, "invoice_id": invoice_id, "amount": 10.0, "currency": "USD"},
    }
    retry_one = runtime.subscription_billing_receive_event(duplicate["state"], failing_event, simulate_failure=True)
    retry_two = runtime.subscription_billing_receive_event(retry_one["state"], failing_event, simulate_failure=True)
    dead_letter = runtime.subscription_billing_receive_event(retry_two["state"], failing_event, simulate_failure=True)
    lifecycle = _settled_state()
    settled_state = lifecycle["state"]
    exposure = runtime.subscription_billing_score_revenue_exposure(settled_state, SUBSCRIPTION_ID)
    proration = runtime.subscription_billing_simulate_proration_quote(settled_state, SUBSCRIPTION_ID, target_seats=8, remaining_ratio=0.5)
    controls = runtime.subscription_billing_run_control_tests(dead_letter["state"])
    api = runtime.subscription_billing_build_api_contract()
    schema = runtime.subscription_billing_build_schema_contract()
    service = runtime.subscription_billing_build_service_contract()
    release = runtime.subscription_billing_build_release_evidence()
    permissions = runtime.subscription_billing_permissions_contract()
    ui_binding = runtime.subscription_billing_ui_binding_contract()
    boundary_ok = runtime.subscription_billing_verify_owned_table_boundary(("subscription", "payment_orchestration.PaymentCaptured", "payment_capture_projection"))
    boundary_bad = runtime.subscription_billing_verify_owned_table_boundary(("subscription", "foreign_billing_table"))
    cancelled = runtime.subscription_billing_cancel_subscription(
        settled_state,
        SUBSCRIPTION_ID,
        effective_date="2026-03-01",
        reason="customer_request",
    )
    smoke = runtime.subscription_billing_runtime_smoke()

    assert first["ok"] is True and first["handler"]["status"] == "handled"
    assert duplicate["ok"] is True and duplicate["handler"]["status"] == "duplicate"
    assert retry_one["ok"] is False and retry_one["handler"]["status"] == "retrying"
    assert retry_two["ok"] is False and retry_two["handler"]["status"] == "retrying"
    assert dead_letter["ok"] is False and dead_letter["handler"]["status"] == "dead_letter"
    assert dead_letter["state"]["dead_letter"][-1]["reason"] == "simulated_failure"
    assert lifecycle["usage"]["ok"] is True and lifecycle["usage"]["usage"]["rated_amount"] > 0
    assert lifecycle["invoice"]["ok"] is True and lifecycle["invoice"]["invoice"]["status"] == "approved"
    assert lifecycle["credit"]["ok"] is True and lifecycle["credit"]["invoice"]["net_amount"] > 0
    assert lifecycle["payment"]["ok"] is True and lifecycle["payment"]["invoice"]["status"] == "paid"
    assert lifecycle["renewed"]["ok"] is True and lifecycle["renewed"]["subscription"]["status"] == "renewed"
    assert lifecycle["changed"]["ok"] is True and lifecycle["changed"]["change_order"]["status"] == "applied"
    assert lifecycle["entitlement"]["ok"] is True and lifecycle["entitlement"]["entitlement"]["projection"] == "entitlement_projection"
    assert lifecycle["revenue"]["ok"] is True and lifecycle["revenue"]["revenue_schedules"]
    assert lifecycle["exception"]["ok"] is True and lifecycle["resolved"]["exception"]["status"] == "resolved"
    assert lifecycle["dunning"]["ok"] is True and lifecycle["dunning"]["notice"]["retry_policy"]["dead_letter"] == "subscription_billing_dead_letter_event"
    assert exposure["ok"] is True and exposure["exposure_score"] >= 0
    assert proration["ok"] is True and proration["target_seats"] == 8
    assert controls["ok"] is True and controls["summary"]["dead_letter_count"] == 1
    assert api["ok"] is True and api["event_contract"] == "AppGen-X"
    assert schema["ok"] is True and schema["datastore_backends"] == ("postgresql", "mysql", "mariadb")
    assert service["ok"] is True and "generate_invoice" in service["command_methods"]
    assert release["ok"] is True and not release["blocking_gaps"]
    assert permissions["action_permissions"]["generate_invoice"] == "subscription_billing.invoice"
    assert ui_binding["binding_evidence"]["dead_letter_table"] == "subscription_billing_dead_letter_event"
    assert boundary_ok["ok"] is True
    assert boundary_bad["ok"] is False and boundary_bad["violations"] == ("foreign_billing_table",)
    assert cancelled["ok"] is True and cancelled["subscription"]["status"] == "cancelled"
    assert smoke["ok"] is True

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        runtime.subscription_billing_configure_runtime(
            runtime.subscription_billing_empty_state(),
            {**CONFIGURATION, "database_backend": "sqlite"},
        )
    with pytest.raises(ValueError, match="AppGen-X subscription event contract"):
        runtime.subscription_billing_configure_runtime(
            runtime.subscription_billing_empty_state(),
            {**CONFIGURATION, "event_topic": "custom.subscription.events"},
        )
    with pytest.raises(ValueError, match="Unsupported Subscription Billing consumed event"):
        runtime.subscription_billing_receive_event(_configured_state(), {"event_id": "bad", "event_type": "UnknownEvent", "payload": {"tenant": TENANT}})
