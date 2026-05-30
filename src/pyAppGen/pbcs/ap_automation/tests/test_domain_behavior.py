"""Domain behavior tests for the ap_automation PBC."""

from __future__ import annotations

import pytest

from .. import runtime
from ..services import ApAutomationExecutionService
from ..services import execution_service_manifest
from ..ui import ap_automation_render_workbench
from ..ui import ap_automation_ui_contract


CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.AP_AUTOMATION_REQUIRED_EVENT_TOPIC,
    "retry_limit": 2,
    "default_currency": "USD",
    "default_timezone": "UTC",
    "allowed_payment_rails": ("ach", "wire", "instant_bank_api"),
    "workbench_limit": 100,
}


def service_with_controls() -> ApAutomationExecutionService:
    service = ApAutomationExecutionService()
    assert service.execute("configure_runtime", CONFIGURATION)["ok"] is True
    for key, value in (
        ("auto_match_threshold", 0.95),
        ("payment_approval_limit", 5000),
        ("discount_capture_floor", 0.01),
        ("vendor_risk_threshold", 0.75),
        ("liquidity_buffer", 250),
        ("workbench_limit", 100),
    ):
        assert service.execute("set_parameter", {"key": key, "value": value})["ok"] is True
    assert service.execute(
        "register_rule",
        {
            "rule_id": "ap-three-way-match",
            "tenant": "tenant_ap",
            "scope": "invoice_match",
            "status": "active",
            "requires_three_way_match": True,
        },
    )["ok"] is True
    return service


def vendor_payload(**overrides) -> dict:
    payload = {
        "vendor_id": "vendor_ap",
        "tenant": "tenant_ap",
        "name": "Precision Parts Ltd",
        "beneficial_owners": ("owner_a", "owner_b"),
        "activation_requirements": ("approval", "bank_validation", "tax_profile", "screening"),
        "terms": {"net_days": 30, "discount_days": 10, "discount_rate": 0.02},
        "risk_signals": {"sanction_hits": 0, "late_delivery_rate": 0.02, "financial_stress": 0.04},
        "identity": {"did": "did:appgen:vendor-ap", "issuer": "trusted_registry", "status": "active"},
    }
    payload.update(overrides)
    return payload


def invoice_lines(quantity: int = 10, price: float = 100.0) -> tuple[dict, ...]:
    return ({"sku": "bearing", "quantity": quantity, "unit_price": price, "account": "inventory"},)


def prepare_matched_invoice(service: ApAutomationExecutionService, invoice_id: str = "inv-ap-001") -> dict:
    assert service.execute("onboard_vendor", vendor_payload())["ok"] is True
    assert service.execute(
        "receive_event",
        {
            "event_id": "vendor-approved-001",
            "event_type": "VendorApproved",
            "payload": {"tenant": "tenant_ap", "vendor_id": "vendor_ap", "approved_by": "controller"},
        },
    )["ok"] is True
    assert service.execute(
        "validate_vendor_bank_account",
        {
            "bank_account_id": "bank-001",
            "tenant": "tenant_ap",
            "vendor_id": "vendor_ap",
            "rail": "ach",
            "account_number": "1234567890",
            "verification_method": "bank_api",
            "verified_by": "treasury_user",
            "created_by": "ap_user",
            "verification_reference": "bank-ref-001",
        },
    )["ok"] is True
    assert service.execute(
        "register_vendor_tax_profile",
        {
            "tax_profile_id": "tax-001",
            "tenant": "tenant_ap",
            "vendor_id": "vendor_ap",
            "jurisdiction": "US-NY",
            "certificate_id": "cert-001",
            "withholding_code": "standard",
        },
    )["ok"] is True
    screening = runtime.ap_automation_screen_vendor_network(service.state, "vendor_ap", sanction_entities=("blocked",))
    assert screening["ok"] is True
    service.state = screening["state"]

    assert service.state["vendors"]["vendor_ap"]["payment_enabled"] is True
    assert service.execute(
        "issue_purchase_order",
        {
            "po_id": "po-ap-001",
            "tenant": "tenant_ap",
            "vendor_id": "vendor_ap",
            "currency": "USD",
            "lines": invoice_lines(),
        },
    )["ok"] is True
    assert service.execute(
        "record_goods_receipt",
        {"receipt_id": "gr-ap-001", "tenant": "tenant_ap", "po_id": "po-ap-001", "lines": ({"sku": "bearing", "quantity": 10},)},
    )["ok"] is True
    capture = service.execute(
        "capture_invoice",
        {
            "invoice_id": invoice_id,
            "tenant": "tenant_ap",
            "vendor_id": "vendor_ap",
            "po_id": "po-ap-001",
            "receipt_id": "gr-ap-001",
            "supplier_invoice_number": "SUP-1001",
            "invoice_date": "2026-05-01",
            "due_date": "2026-05-31",
            "currency": "USD",
            "tax": {"jurisdiction": "US-NY", "amount": 80, "rate": 0.08},
            "contract_terms": {"net_days": 30, "discount_days": 10, "discount_rate": 0.02},
            "artifact": {"artifact_id": "artifact-001", "channel": "pdf", "confidence": 0.99, "source_document": "invoice.pdf"},
            "lines": invoice_lines(),
        },
    )
    assert capture["ok"] is True
    return capture


def test_ap_execution_service_runs_vendor_to_payment_lifecycle():
    service = service_with_controls()
    capture = prepare_matched_invoice(service)

    match = service.execute("match_invoice", {"invoice_id": "inv-ap-001"})
    schedule = service.execute(
        "schedule_payments",
        {"tenant": "tenant_ap", "liquidity_forecast": (2000.0, 1800.0, 1700.0), "risk_limit": 0.75},
    )
    batch = service.execute(
        "create_payment_batch",
        {"batch_id": "batch-001", "tenant": "tenant_ap", "payment_ids": ("pay_inv-ap-001",), "rail": "ach"},
    )
    execute = service.execute(
        "execute_payment",
        {
            "payment_id": "pay_inv-ap-001",
            "rails": (
                {"rail": "instant_bank_api", "cost": 4, "latency": 2, "fx_rate": 1.0, "available": False},
                {"rail": "ach", "cost": 1, "latency": 24, "fx_rate": 1.0, "available": True},
            ),
        },
    )
    remittance = service.execute("generate_remittance_advice", {"payment_id": "pay_inv-ap-001", "delivery_channel": "portal"})
    workbench = service.execute("build_workbench_view", {"tenant": "tenant_ap"})

    assert capture["result"]["invoice"]["total"] == 1080.0
    assert capture["result"]["invoice"]["capture_artifact_id"] == "artifact-001"
    assert match["result"] == {"ok": True, "invoice_id": "inv-ap-001", "confidence": 0.99, "decision": "auto_approve"}
    assert schedule["result"]["payments"][0]["scheduled_date"] == "discount_window"
    assert schedule["result"]["payments"][0]["hold_reasons"] == ()
    assert batch["result"]["batch"]["total_amount"] == 1080.0
    assert execute["ok"] is True
    assert execute["result"]["payment"]["status"] == "executed"
    assert execute["result"]["payment"]["rail"] == "ach"
    assert execute["result"]["failover_used"] is True
    assert execute["result"]["idempotency_key"].startswith("ap_automation:PaymentExecuted:")
    assert remittance["result"]["advice"]["amount"] == 1080.0
    assert workbench["result"]["executed_payment_count"] == 1
    assert workbench["result"]["open_invoice_total"] == 0
    assert service.state["invoices"]["inv-ap-001"]["status"] == "paid"


def test_ap_duplicate_invoice_and_blocked_payment_controls_are_executable():
    service = service_with_controls()
    prepare_matched_invoice(service)
    duplicate_capture = service.execute(
        "capture_invoice",
        {
            "invoice_id": "inv-ap-duplicate",
            "tenant": "tenant_ap",
            "vendor_id": "vendor_ap",
            "po_id": "po-ap-001",
            "receipt_id": "gr-ap-001",
            "supplier_invoice_number": "SUP 1001",
            "invoice_date": "2026-05-02",
            "due_date": "2026-06-01",
            "currency": "USD",
            "tax": {"jurisdiction": "US-NY", "amount": 80, "rate": 0.08},
            "contract_terms": {"net_days": 30, "discount_days": 10, "discount_rate": 0.02},
            "lines": invoice_lines(),
        },
    )
    duplicate_match = service.execute("match_invoice", {"invoice_id": "inv-ap-duplicate"})
    blocked_schedule = service.execute(
        "schedule_payments",
        {"tenant": "tenant_ap", "liquidity_forecast": (2500.0, 2000.0), "risk_limit": 0.75},
    )

    duplicate_invoice = duplicate_capture["result"]["invoice"]
    blocked = {payment["invoice_id"]: payment for payment in blocked_schedule["result"]["payments"]}
    assert duplicate_invoice["duplicate_review_required"] is True
    assert duplicate_invoice["duplicate_candidates"][0]["invoice_id"] == "inv-ap-001"
    assert duplicate_match["result"]["decision"] == "route_exception"
    assert duplicate_match["result"]["reason"] == "suspected_duplicate_invoice"
    assert blocked["inv-ap-duplicate"]["status"] == "blocked"
    assert "suspected_duplicate_invoice" in blocked["inv-ap-duplicate"]["hold_reasons"]
    assert any(task["reason"] == "suspected_duplicate_invoice" for task in service.state["approval_tasks"].values())


def test_ap_event_retry_dead_letter_statement_reconciliation_and_ui_surfaces():
    service = service_with_controls()
    prepare_matched_invoice(service)
    service.execute(
        "schedule_payments",
        {"tenant": "tenant_ap", "liquidity_forecast": (2000.0, 1800.0), "risk_limit": 0.75},
    )
    service.execute(
        "execute_payment",
        {
            "payment_id": "pay_inv-ap-001",
            "rails": ({"rail": "ach", "cost": 1, "latency": 24, "fx_rate": 1.0, "available": True},),
        },
    )
    retrying = service.execute(
        "receive_event",
        {"event_id": "bad-event-1", "event_type": "UnknownInboundEvent", "payload": {"tenant": "tenant_ap"}, "attempts": 1},
    )
    dead_letter = service.execute(
        "receive_event",
        {"event_id": "bad-event-2", "event_type": "UnknownInboundEvent", "payload": {"tenant": "tenant_ap"}, "attempts": 2},
    )
    statement = service.execute(
        "reconcile_vendor_statement",
        {
            "statement_id": "stmt-001",
            "tenant": "tenant_ap",
            "vendor_id": "vendor_ap",
            "lines": (
                {"supplier_invoice_number": "SUP-1001", "amount": 1080.0, "status": "paid"},
                {"supplier_invoice_number": "MISSING", "amount": 25.0, "status": "open"},
            ),
        },
    )
    ui_contract = ap_automation_ui_contract()
    rendered = ap_automation_render_workbench(
        service.state,
        tenant="tenant_ap",
        principal_permissions=tuple(set(ui_contract["action_permissions"].values())),
    )
    manifest = execution_service_manifest()

    assert retrying["ok"] is False
    assert retrying["result"]["handler"]["status"] == "retrying"
    assert dead_letter["ok"] is False
    assert dead_letter["result"]["dead_lettered"] is True
    assert len(service.state["dead_letter"]) == 1
    assert statement["result"]["statement"]["status"] == "action_required"
    assert statement["result"]["statement"]["exception_count"] == 1
    assert rendered["ok"] is True
    assert "ApFormsHub" in rendered["fragments"]
    assert "invoice_capture" in rendered["data_entry_forms"]
    assert "payment_release_wizard" in rendered["guided_flows"]
    assert {"capture_invoice", "execute_payment", "receive_event"} <= set(manifest["operations"])


def test_ap_configuration_rejects_forbidden_eventing_and_non_ordinary_backends():
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        runtime.ap_automation_configure_runtime(
            runtime.ap_automation_empty_state(),
            {**CONFIGURATION, "database_backend": "sqlite"},
        )
    with pytest.raises(ValueError, match="stream-engine"):
        runtime.ap_automation_configure_runtime(
            runtime.ap_automation_empty_state(),
            {**CONFIGURATION, "stream_engine_picker": "kafka"},
        )
