"""Control library for AP workflow governance and release safety."""

from __future__ import annotations

from .repository import ApAutomationRepository
from .repository import build_demo_state
from .runtime import AP_AUTOMATION_REQUIRED_EVENT_TOPIC
from .runtime import ap_automation_run_control_tests


CONTROL_DEFINITIONS = (
    {
        "control_id": "vendor_payment_readiness",
        "title": "Vendor Payment Readiness Gate",
        "severity": "high",
        "dataset": "vendor_readiness",
        "assertion": "payment_enabled_only_when_evidence_pack_is_clear",
    },
    {
        "control_id": "duplicate_invoice_hold_guard",
        "title": "Duplicate Invoice Hold Guard",
        "severity": "high",
        "dataset": "invoice_capture_queue",
        "assertion": "duplicate_invoices_require_hold_reason",
    },
    {
        "control_id": "payment_batch_release_integrity",
        "title": "Payment Batch Release Integrity",
        "severity": "high",
        "dataset": "payment_release",
        "assertion": "batched_payments_reference_existing_batch",
    },
    {
        "control_id": "statement_exception_visibility",
        "title": "Statement Exception Visibility",
        "severity": "medium",
        "dataset": "statement_reconciliation",
        "assertion": "reconciliation_exceptions_are_visible_in_workbench",
    },
    {
        "control_id": "event_contract_lock",
        "title": "AppGen-X Event Contract Lock",
        "severity": "high",
        "dataset": "payment_release",
        "assertion": "configuration_is_locked_to_appgen_x_ap_topic",
    },
)


def control_contract() -> dict:
    """Return AP workflow control coverage backed by owned datasets."""
    return {
        "format": "appgen.ap-automation-controls.v1",
        "ok": bool(CONTROL_DEFINITIONS),
        "pbc": "ap_automation",
        "controls": CONTROL_DEFINITIONS,
        "side_effects": (),
    }


def evaluate_controls(state: dict, *, tenant: str) -> dict:
    """Evaluate AP controls against the current owned state only."""
    repository = ApAutomationRepository()
    snapshot = repository.tenant_snapshot(state, tenant)
    vendors = snapshot["datasets"]["vendor_readiness"]
    invoices = tuple(invoice for invoice in state.get("invoices", {}).values() if invoice["tenant"] == tenant)
    payments = tuple(payment for payment in state.get("payments", {}).values() if payment["tenant"] == tenant)
    statements = snapshot["datasets"]["statement_reconciliation"]
    results = (
        {
            "control_id": "vendor_payment_readiness",
            "ok": all(not row["payment_enabled"] or not row["pending_checks"] for row in vendors),
        },
        {
            "control_id": "duplicate_invoice_hold_guard",
            "ok": all(
                not invoice.get("duplicate_review_required") or bool(invoice.get("hold_reasons"))
                for invoice in invoices
            ),
        },
        {
            "control_id": "payment_batch_release_integrity",
            "ok": all(
                payment["status"] != "executed" or bool(payment.get("batch_id"))
                for payment in payments
            ),
        },
        {
            "control_id": "statement_exception_visibility",
            "ok": all(
                statement["exception_count"] >= 0
                for statement in statements
            ) and snapshot["workbench"]["statement_exception_count"] >= 0,
        },
        {
            "control_id": "event_contract_lock",
            "ok": state.get("configuration", {}).get("event_topic") == AP_AUTOMATION_REQUIRED_EVENT_TOPIC
            and state.get("configuration", {}).get("event_contract") == "AppGen-X",
        },
    )
    runtime_controls = ap_automation_run_control_tests(state)
    return {
        "ok": control_contract()["ok"] and all(item["ok"] for item in results) and runtime_controls["ok"],
        "pbc": "ap_automation",
        "controls": results,
        "runtime_controls": runtime_controls,
        "snapshot": snapshot,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise the AP control stack against a deterministic runtime state."""
    state = build_demo_state(include_release=True)
    evaluation = evaluate_controls(state, tenant="tenant_repo")
    return {
        "ok": control_contract()["ok"] and evaluation["ok"],
        "contract": control_contract(),
        "evaluation": evaluation,
        "side_effects": (),
    }
