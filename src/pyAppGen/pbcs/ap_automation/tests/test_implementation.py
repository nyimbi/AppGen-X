"""Executable AP implementation tests kept with the PBC package."""

from .. import (
    AP_AUTOMATION_REQUIRED_EVENT_TOPIC,
    ap_automation_align_contract_terms,
    ap_automation_capture_invoice,
    ap_automation_configure_runtime,
    ap_automation_create_payment_batch,
    ap_automation_empty_state,
    ap_automation_execute_payment,
    ap_automation_generate_remittance_advice,
    ap_automation_issue_purchase_order,
    ap_automation_match_invoice,
    ap_automation_onboard_vendor,
    ap_automation_receive_event,
    ap_automation_reconcile_vendor_statement,
    ap_automation_record_goods_receipt,
    ap_automation_register_rule,
    ap_automation_register_vendor_tax_profile,
    ap_automation_schedule_payments,
    ap_automation_screen_vendor_network,
    ap_automation_set_parameter,
    ap_automation_validate_vendor_bank_account,
    release_evidence,
    services,
)
from ..agent import composed_agent_contribution


def test_vendor_readiness_and_duplicate_invoice_controls():
    state = _configured_state()
    vendor = ap_automation_onboard_vendor(
        state,
        {
            "vendor_id": "vendor_ready",
            "tenant": "tenant_ready",
            "name": "Ready Vendor Ltd",
            "beneficial_owners": ("owner_a",),
            "terms": {"net_days": 30},
            "risk_signals": {"sanction_hits": 0, "late_delivery_rate": 0.01, "financial_stress": 0.02},
            "activation_requirements": ("approval", "bank_validation", "tax_profile", "screening"),
            "identity": {"did": "did:appgen:vendor-ready", "issuer": "trusted_registry", "status": "active"},
        },
    )
    state = vendor["state"]
    assert vendor["vendor"]["payment_enabled"] is False

    state = ap_automation_receive_event(
        state,
        {
            "event_id": "evt_vendor_ready_approved",
            "event_type": "VendorApproved",
            "payload": {"tenant": "tenant_ready", "vendor_id": "vendor_ready", "approved_by": "controller_ready"},
        },
    )["state"]
    state = ap_automation_validate_vendor_bank_account(
        state,
        {
            "vendor_id": "vendor_ready",
            "bank_account_id": "bank_ready",
            "account_number": "123456789012",
            "rail": "ach",
            "verification_method": "independent_callback",
            "verification_reference": "cb-001",
            "verified_by": "analyst_a",
        },
    )["state"]
    state = ap_automation_register_vendor_tax_profile(
        state,
        {
            "vendor_id": "vendor_ready",
            "tax_profile_id": "tax_ready",
            "jurisdiction": "US-NY",
            "withholding_code": "NONE",
            "certificate_id": "cert-ready",
            "expiry_date": "2027-12-31",
        },
    )["state"]
    screening = ap_automation_screen_vendor_network(state, "vendor_ready", sanction_entities=())
    state = screening["state"]
    assert screening["payment_enabled"] is True

    state = _seed_po_receipt(state, tenant="tenant_ready", vendor_id="vendor_ready")
    state = ap_automation_capture_invoice(
        state,
        _invoice_payload("inv_primary", "tenant_ready", "vendor_ready", "ACME-1001", 500),
    )["state"]
    duplicate = ap_automation_capture_invoice(
        state,
        _invoice_payload("inv_duplicate", "tenant_ready", "vendor_ready", "ACME 1001", 500),
    )
    match = ap_automation_match_invoice(duplicate["state"], "inv_duplicate")
    assert duplicate["invoice"]["duplicate_review_required"] is True
    assert duplicate["invoice"]["duplicate_candidates"][0]["invoice_id"] == "inv_primary"
    assert match["decision"] == "route_exception"


def test_payment_batch_remittance_and_statement_reconciliation():
    state = _ready_vendor_state("tenant_payments", "vendor_payments")
    state = _seed_po_receipt(state, tenant="tenant_payments", vendor_id="vendor_payments")
    state = ap_automation_capture_invoice(
        state,
        _invoice_payload("inv_small", "tenant_payments", "vendor_payments", "SMALL-0800", 800),
    )["state"]
    state = ap_automation_capture_invoice(
        state,
        _invoice_payload("inv_large", "tenant_payments", "vendor_payments", "LARGE-9000", 6000),
    )["state"]

    schedule = ap_automation_schedule_payments(
        state,
        tenant="tenant_payments",
        liquidity_forecast=(9000, 8500, 8000),
        risk_limit=0.7,
    )
    state = schedule["state"]
    scheduled = {payment["invoice_id"]: payment for payment in schedule["payments"]}
    assert scheduled["inv_large"]["status"] == "blocked"
    assert "approval_required" in scheduled["inv_large"]["hold_reasons"]
    assert scheduled["inv_small"]["status"] == "scheduled"

    state = ap_automation_create_payment_batch(
        state,
        {"tenant": "tenant_payments", "payment_ids": ("pay_inv_small",), "batch_id": "batch_payments_1"},
    )["state"]
    executed = ap_automation_execute_payment(
        state,
        "pay_inv_small",
        rails=(
            {"rail": "instant_bank_api", "cost": 5, "latency": 2, "fx_rate": 1.0, "available": False},
            {"rail": "ach", "cost": 1, "latency": 24, "fx_rate": 1.0, "available": True},
        ),
    )
    state = executed["state"]
    advice = ap_automation_generate_remittance_advice(state, "pay_inv_small", delivery_channel="portal")
    statement = ap_automation_reconcile_vendor_statement(
        advice["state"],
        {
            "statement_id": "stmt_payments_1",
            "tenant": "tenant_payments",
            "vendor_id": "vendor_payments",
            "lines": (
                {"supplier_invoice_number": "SMALL-0800", "amount": 800.0, "status": "paid"},
                {"supplier_invoice_number": "UNKNOWN-404", "amount": 120.0, "status": "open"},
            ),
        },
    )
    assert executed["payment"]["batch_id"] == "batch_payments_1"
    assert advice["advice"]["invoices"][0]["supplier_invoice_number"] == "SMALL-0800"
    assert statement["statement"]["status"] == "action_required"
    assert statement["statement"]["exception_count"] == 2


def test_services_agent_and_release_evidence_expose_execution_slice():
    execution_manifest = services.execution_service_manifest()
    contribution = composed_agent_contribution()
    evidence = release_evidence.build_release_evidence()
    validation = release_evidence.validate_release_evidence()

    assert execution_manifest["ok"] is True
    assert {
        "validate_vendor_bank_account",
        "register_vendor_tax_profile",
        "create_payment_batch",
        "generate_remittance_advice",
        "reconcile_vendor_statement",
    } <= set(execution_manifest["operations"])
    assert contribution["ok"] is True
    assert set(execution_manifest["operations"]) <= set(contribution["execution_operations"])
    assert evidence["ok"] is True
    assert {"ui_contract_bound", "agent_contribution_bound", "execution_service_bound"} <= {
        check["id"] for check in evidence["checks"]
    }
    assert validation["ok"] is True


def _configured_state():
    state = ap_automation_empty_state()
    state = ap_automation_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": AP_AUTOMATION_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "default_timezone": "UTC",
            "allowed_payment_rails": ("ach", "wire", "instant_bank_api"),
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("auto_match_threshold", 0.95),
        ("payment_approval_limit", 5000),
        ("discount_capture_floor", 0.01),
        ("vendor_risk_threshold", 0.7),
        ("liquidity_buffer", 250),
        ("workbench_limit", 50),
    ):
        state = ap_automation_set_parameter(state, name, value)["state"]
    state = ap_automation_register_rule(
        state,
        {
            "rule_id": "rule_impl",
            "tenant": "tenant_impl",
            "scope": "invoice_match",
            "requires_three_way_match": True,
            "auto_match_threshold": 0.95,
            "status": "active",
        },
    )["state"]
    return state


def _ready_vendor_state(tenant, vendor_id):
    state = _configured_state()
    state = ap_automation_onboard_vendor(
        state,
        {
            "vendor_id": vendor_id,
            "tenant": tenant,
            "name": "Payables Vendor",
            "beneficial_owners": ("owner_pay",),
            "terms": {"net_days": 30},
            "risk_signals": {"sanction_hits": 0, "late_delivery_rate": 0.01, "financial_stress": 0.01},
            "identity": {"did": f"did:appgen:{vendor_id}", "issuer": "trusted_registry", "status": "active"},
        },
    )["state"]
    return ap_automation_receive_event(
        state,
        {
            "event_id": f"evt_{vendor_id}_approved",
            "event_type": "VendorApproved",
            "payload": {"tenant": tenant, "vendor_id": vendor_id, "approved_by": "controller_pay"},
        },
    )["state"]


def _seed_po_receipt(state, *, tenant, vendor_id):
    state = ap_automation_issue_purchase_order(
        state,
        {
            "po_id": "po_impl",
            "tenant": tenant,
            "vendor_id": vendor_id,
            "currency": "USD",
            "lines": ({"sku": "service", "quantity": 1, "unit_price": 500, "account": "expense"},),
        },
    )["state"]
    return ap_automation_record_goods_receipt(
        state,
        {
            "receipt_id": "gr_impl",
            "tenant": tenant,
            "po_id": "po_impl",
            "lines": ({"sku": "service", "quantity": 1},),
        },
    )["state"]


def _invoice_payload(invoice_id, tenant, vendor_id, supplier_invoice_number, amount):
    contract_terms = ap_automation_align_contract_terms(
        "net 30 with 2% discount if paid within 10 days; tax jurisdiction US-NY",
        {"vendor_id": vendor_id},
    )["terms"]
    return {
        "invoice_id": invoice_id,
        "tenant": tenant,
        "vendor_id": vendor_id,
        "po_id": "po_impl",
        "receipt_id": "gr_impl",
        "supplier_invoice_number": supplier_invoice_number,
        "invoice_date": "2026-05-28",
        "due_date": "2026-06-27",
        "currency": "USD",
        "tax": {"jurisdiction": "US-NY", "amount": round(float(amount) * 0.08, 2), "rate": 0.08},
        "contract_terms": contract_terms,
        "lines": ({"sku": "service", "quantity": 1, "unit_price": float(amount), "account": "expense"},),
        "artifact": {"source_document": f"{invoice_id}.pdf", "channel": "email"},
    }
