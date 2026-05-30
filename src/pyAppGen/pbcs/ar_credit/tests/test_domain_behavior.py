"""Domain behavior tests for the ar_credit PBC."""

from __future__ import annotations

import pytest

from .. import agent
from .. import release_evidence
from .. import routes
from .. import runtime
from ..services import ArCreditService
from ..services import service_operation_manifest
from ..repository import ArCreditRepository
from ..standalone import ArCreditStandaloneApp
from ..standalone import workbench_smoke_test
from ..ui import ar_credit_render_workbench
from ..ui import ar_credit_ui_contract


CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.AR_CREDIT_REQUIRED_EVENT_TOPIC,
    "retry_limit": 2,
    "default_currency": "USD",
    "default_timezone": "UTC",
    "allowed_collection_channels": ("portal", "api", "email"),
    "workbench_limit": 100,
}


def configured_state() -> dict:
    state = runtime.ar_credit_empty_state()
    state = runtime.ar_credit_configure_runtime(state, CONFIGURATION)["state"]
    for key, value in (
        ("auto_cash_threshold", 0.95),
        ("credit_limit_buffer", 0.2),
        ("collection_risk_threshold", 0.65),
        ("dunning_grace_days", 5),
        ("write_off_approval_limit", 5000),
        ("workbench_limit", 100),
    ):
        state = runtime.ar_credit_set_parameter(state, key, value)["state"]
    state = runtime.ar_credit_register_rule(
        state,
        {
            "rule_id": "ar-cash-application",
            "tenant": "tenant_ar",
            "scope": "cash_application",
            "auto_cash_threshold": 0.95,
            "requires_delivery_confirmation": True,
            "status": "active",
        },
    )["state"]
    return state


def service_with_customer() -> ArCreditService:
    service = ArCreditService(configured_state())
    customer = service.command_ar_customers(
        {
            "customer": {
                "customer_id": "cust-ar-001",
                "tenant": "tenant_ar",
                "name": "Reliable Buyer Ltd",
                "parent": "buyer_group",
                "beneficial_owners": ("owner_a", "owner_b"),
                "requested_limit": 5000,
                "terms": {"net_days": 30, "discount_days": 10, "discount_rate": 0.01},
                "risk_signals": {"sanction_hits": 0, "payment_latency": 0.04, "industry_stress": 0.03},
                "identity": {"did": "did:appgen:cust-ar-001", "issuer": "trusted_registry", "status": "active"},
            }
        }
    )
    assert customer["ok"] is True
    assert customer["customer"]["credit_limit"] > 4000
    return service


def invoice_payload(invoice_id: str = "ar_inv_001", *, invoice_date: str = "2026-05-01", due_date: str = "2026-05-31", amount: float = 1000.0) -> dict:
    return {
        "invoice_id": invoice_id,
        "tenant": "tenant_ar",
        "customer_id": "cust-ar-001",
        "currency": "USD",
        "invoice_date": invoice_date,
        "due_date": due_date,
        "tax": {"jurisdiction": "US-NY", "amount": round(amount * 0.08, 2), "rate": 0.08},
        "performance_obligations": ({"obligation": f"deliver_{invoice_id}", "satisfied": True, "allocation": amount},),
        "lines": ({"sku": "service", "quantity": 1, "unit_price": amount, "account": "revenue"},),
    }


def issue_invoice(service: ArCreditService, invoice_id: str = "ar_inv_001", *, invoice_date: str = "2026-05-01", due_date: str = "2026-05-31", amount: float = 1000.0) -> dict:
    issued = service.command_ar_invoices({"invoice": invoice_payload(invoice_id, invoice_date=invoice_date, due_date=due_date, amount=amount)})
    assert issued["ok"] is True
    return issued


def test_ar_invoice_to_cash_lifecycle_executes_through_service_facade():
    service = service_with_customer()
    issued = issue_invoice(service)
    delivered = service.command_ar_deliveries(
        {
            "receipt": {
                "delivery_id": "deliv-ar-001",
                "tenant": "tenant_ar",
                "invoice_id": "ar_inv_001",
                "lines": ({"sku": "service", "quantity": 1},),
            }
        }
    )
    applied = service.command_ar_cash_applications(
        {
            "receipt": {
                "receipt_id": "rcpt-ar-001",
                "tenant": "tenant_ar",
                "customer_id": "cust-ar-001",
                "amount": 1080.0,
                "currency": "USD",
                "remittance_text": "PAY ar_inv_001 amount 1080 bank_ref BAI-001",
            }
        }
    )
    aging = service.query_ar_aging({"tenant": "tenant_ar", "as_of": "2026-06-30"})
    statement = service.query_ar_statements_customer_id({"customer_id": "cust-ar-001", "as_of": "2026-06-30"})
    workbench = service.query_ar_workbench({"tenant": "tenant_ar", "as_of": "2026-06-30", "customer_id": "cust-ar-001"})

    assert issued["invoice"]["total"] == 1080.0
    assert issued["readiness"]["ready"] is True
    assert delivered["ok"] is True
    assert delivered["delivery"]["status"] == "confirmed"
    assert applied["ok"] is True
    assert applied["decision"] == "auto_clear"
    assert applied["confidence"] >= 0.98
    assert applied["application"]["applied_amount"] == 1080.0
    assert service.state["invoices"]["ar_inv_001"]["status"] == "cleared"
    assert service.state["cash_pools"]["tenant_ar"]["received_cash"] == 1080.0
    assert aging["aging"]["buckets"] == {"current": 0.0, "1_30": 0.0, "31_60": 0.0, "61_90": 0.0, "90_plus": 0.0}
    assert statement["statement"]["statement"]["open_balance"] == 0.0
    assert workbench["ok"] is True
    assert workbench["workbench"]["open_balance"] == 0


def test_ar_handles_overpayment_unapplied_cash_and_revenue_schedule():
    service = service_with_customer()
    issue_invoice(service, "ar_inv_002", amount=500.0)
    overpayment = service.command_ar_cash_applications(
        {
            "receipt": {
                "receipt_id": "rcpt-ar-overpay",
                "tenant": "tenant_ar",
                "customer_id": "cust-ar-001",
                "amount": 600.0,
                "currency": "USD",
                "remittance_text": "PAY ar_inv_002 amount 600 bank_ref BAI-002",
            }
        }
    )
    schedule = service.query_ar_revenue_schedules_invoice_id({"invoice_id": "ar_inv_002", "build_if_missing": True})

    assert overpayment["ok"] is True
    assert overpayment["decision"] == "apply_and_record_excess"
    assert overpayment["applied"]["application"]["applied_amount"] == 540.0
    assert overpayment["excess_unapplied_cash"]["amount"] == 60.0
    assert service.state["invoices"]["ar_inv_002"]["status"] == "cleared"
    assert schedule["ok"] is True
    assert schedule["schedule"]["recognized_amount"] == 500.0
    assert schedule["schedule"]["deferred_amount"] == 0


def test_ar_adjustments_collections_and_ui_surfaces_are_executable():
    service = service_with_customer()
    issue_invoice(service, "ar_inv_003", invoice_date="2025-12-01", due_date="2026-01-01", amount=1000.0)
    memo = service.command_ar_credit_memos({"memo": {"invoice_id": "ar_inv_003", "tenant": "tenant_ar", "amount": 100.0, "reason": "service_credit"}})
    write_off = service.command_ar_write_offs(
        {
            "write_off": {
                "invoice_id": "ar_inv_003",
                "tenant": "tenant_ar",
                "amount": 980.0,
                "approved_by": "controller",
                "reason": "immaterial_balance_cleanup",
            }
        }
    )
    refund = service.command_ar_refunds({"refund": {"tenant": "tenant_ar", "customer_id": "cust-ar-001", "amount": 25.0, "currency": "USD", "reason": "overpayment"}})
    dispute = service.command_ar_disputes({"dispute": {"dispute_id": "disp-001", "invoice_id": "ar_inv_003", "amount": 50.0, "reason": "quality", "evidence_score": 0.9}})
    issue_invoice(service, "ar_inv_004", invoice_date="2025-12-01", due_date="2026-01-01", amount=250.0)
    follow_up = service.command_ar_collections({"customer_id": "cust-ar-001", "as_of": "2026-03-15"})
    action = service.command_ar_collections({"tenant": "tenant_ar", "customer_id": "cust-ar-001", "invoice_id": "ar_inv_004", "channel": "portal", "due_date": "2026-03-20"})
    ui_contract = ar_credit_ui_contract()
    rendered = ar_credit_render_workbench(
        service.state,
        tenant="tenant_ar",
        principal_permissions=tuple(set(ui_contract["action_permissions"].values())),
    )

    assert memo["ok"] is True
    assert memo["invoice"]["open_amount"] == 980.0
    assert write_off["ok"] is True
    assert write_off["invoice"]["status"] == "written_off"
    assert refund["ok"] is True
    assert refund["refund"]["status"] == "scheduled"
    assert dispute["dispute"]["decision"] == "credit_memo_suggested"
    assert follow_up["follow_up"]["recommended_action"] == "schedule_collections_call"
    assert action["ok"] is True
    assert action["action"]["status"] == "scheduled"
    assert rendered["ok"] is True
    assert "CashApplicationWorkbench" in rendered["fragments"]
    assert "invoice_to_cash_cycle" in tuple(wizard["wizard_id"] for wizard in rendered["wizards"])
    assert "cash_receipt_application" in tuple(form["form_id"] for form in rendered["forms"])
    assert rendered["cards"][2]["key"] == "open_balance"



def test_ar_agent_routes_repository_standalone_and_release_surfaces_are_executable():
    service = service_with_customer()
    issue_invoice(service, "ar_inv_route", amount=400.0)

    route_validation = routes.validate_api_route_contracts()
    route_dispatch = routes.dispatch_route(
        "POST",
        "/api/pbc/ar_credit/ar/invoices",
        {"invoice": invoice_payload("ar_inv_route_002", amount=250.0)},
        service=service,
    )
    skills = agent.agent_skill_manifest()
    document_plan = agent.document_instruction_plan(
        "Customer asks for credit review and remittance matching guidance.",
        "Review invoice readiness, apply cash, and build collections follow-up.",
    )
    crud_plan = agent.datastore_crud_plan(
        "create",
        table="ar_invoice",
        payload={"invoice_id": "ar_inv_agent", "customer_id": "cust-ar-001"},
    )
    blocked_crud = agent.datastore_crud_plan("delete", table="ap_automation_invoice", payload={"invoice_id": "bad"})
    invoice_preview = agent.invoice_readiness_preview({"state": service.state, "invoice": invoice_payload("ar_inv_preview", amount=50.0)})
    cash_preview = agent.cash_application_preview(
        {
            "state": service.state,
            "receipt": {
                "receipt_id": "rcpt-agent-preview",
                "tenant": "tenant_ar",
                "customer_id": "cust-ar-001",
                "amount": 270.0,
                "currency": "USD",
                "remittance_text": "PAY ar_inv_route_002 amount 270",
            },
        }
    )
    contribution = agent.composed_agent_contribution()

    repository = ArCreditRepository()
    try:
        applied = repository.apply_migrations()
        saved = repository.save_state("tenant_ar", service.state, captured_at="2026-05-30T00:00:00Z")
        loaded_state = repository.load_state("tenant_ar")
        run = repository.record_workflow_run(
            run_id="ar-credit-domain-proof",
            tenant="tenant_ar",
            workflow_name="domain_behavior",
            status="completed",
            summary={"invoice_count": len(service.state["invoices"])},
            created_at="2026-05-30T00:00:00Z",
        )
        runs = repository.list_workflow_runs(tenant="tenant_ar")
        manifest = repository.database_manifest()
    finally:
        repository.close()

    app = ArCreditStandaloneApp(tenant="tenant_demo")
    try:
        loaded = app.load_demo_workspace(tenant="tenant_demo")
        rendered = app.render_workbench(tenant="tenant_demo")
        controls = app.control_center(tenant="tenant_demo")
        release_snapshot = app.release_snapshot(tenant="tenant_demo")
        latest_release = app.repository.latest_release_snapshot(tenant="tenant_demo")
    finally:
        app.close()

    release_validation = release_evidence.validate_release_evidence()
    release_smoke = release_evidence.smoke_test()
    workbench_smoke = workbench_smoke_test()

    assert route_validation["ok"] is True
    assert all(contract["event_contract"] == "AppGen-X" for contract in route_validation["contracts"])
    assert all(contract["stream_engine_picker_visible"] is False for contract in route_validation["contracts"])
    assert all(contract["shared_table_access"] is False for contract in route_validation["contracts"])
    assert route_dispatch["ok"] is True
    assert route_dispatch["result"]["event_contract"] == "AppGen-X"
    assert route_dispatch["result"]["side_effects"] == ()
    assert skills["ok"] is True
    assert document_plan["ok"] is True
    assert {"execute_receipt_application", "build_collections_follow_up"} <= {item["operation"] for item in document_plan["workflow_suggestions"]}
    assert crud_plan["ok"] is True
    assert crud_plan["requires_confirmation"] is True
    assert crud_plan["event_contract"] == "AppGen-X"
    assert blocked_crud["ok"] is False
    assert invoice_preview["ok"] is True
    assert cash_preview["ok"] is True
    assert contribution["ok"] is True
    assert "ar_credit_workflow_previews" in contribution["dsl_tools"]
    assert applied == ("create_runtime_snapshot", "create_workflow_run", "create_release_snapshot")
    assert saved["ok"] is True
    assert loaded_state["invoices"]["ar_inv_route"]["customer_id"] == "cust-ar-001"
    assert run["ok"] is True
    assert runs[0]["workflow_name"] == "domain_behavior"
    assert manifest["ok"] is True
    assert manifest["shared_table_access"] is False
    assert loaded["ok"] is True
    assert rendered["ok"] is True
    assert controls["ok"] is True
    assert release_snapshot["ok"] is True
    assert latest_release is not None
    assert release_validation["ok"] is True
    assert release_smoke["ok"] is True
    assert workbench_smoke["ok"] is True


def test_ar_event_retry_dead_letter_contract_and_configuration_guards():
    service = service_with_customer()
    processed = service.state
    processed = runtime.ar_credit_receive_event(
        processed,
        {
            "event_id": "identity-evt-001",
            "event_type": "CustomerIdentityVerified",
            "payload": {"tenant": "tenant_ar", "customer_id": "cust-ar-001", "status": "verified"},
        },
    )
    duplicate = runtime.ar_credit_receive_event(
        processed["state"],
        {
            "event_id": "identity-evt-001",
            "event_type": "CustomerIdentityVerified",
            "payload": {"tenant": "tenant_ar", "customer_id": "cust-ar-001", "status": "verified"},
        },
    )
    retrying = runtime.ar_credit_receive_event(
        duplicate["state"],
        {"event_id": "bad-ar-event", "event_type": "UnknownInboundEvent", "payload": {"tenant": "tenant_ar"}},
    )
    dead_letter = runtime.ar_credit_receive_event(
        retrying["state"],
        {"event_id": "bad-ar-event", "event_type": "UnknownInboundEvent", "payload": {"tenant": "tenant_ar"}},
    )
    manifest = service_operation_manifest()

    assert processed["handler"]["status"] == "processed"
    assert duplicate["duplicate"] is True
    assert retrying["ok"] is False
    assert retrying["handler"]["status"] == "retrying"
    assert dead_letter["handler"]["status"] == "dead_letter"
    assert len(dead_letter["state"]["dead_letter"]) == 1
    assert manifest["event_contract"]["contract"] == "AppGen-X"
    assert {"command_ar_invoices", "command_ar_cash_applications", "query_ar_workbench"} <= set(manifest["operations"])

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        runtime.ar_credit_configure_runtime(runtime.ar_credit_empty_state(), {**CONFIGURATION, "database_backend": "sqlite"})
    with pytest.raises(ValueError, match="AppGen-X event contract"):
        runtime.ar_credit_configure_runtime(runtime.ar_credit_empty_state(), {**CONFIGURATION, "stream_engine_picker": "kafka"})
