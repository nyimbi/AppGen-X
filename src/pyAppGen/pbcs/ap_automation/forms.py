"""Database-backed forms for Accounts Payable Automation."""

from __future__ import annotations

from .repository import ApAutomationRepository
from .runtime import ap_automation_permissions_contract


FORM_DEFINITIONS = (
    {
        "form_id": "vendor_onboarding",
        "title": "Vendor Onboarding Evidence Pack",
        "permission": "ap_automation.vendor",
        "dataset": "vendor_readiness",
        "submit_action": "onboard_vendor",
        "fields": (
            {"name": "vendor_id", "type": "text", "required": True},
            {"name": "name", "type": "text", "required": True},
            {"name": "beneficial_owners", "type": "list", "required": True},
            {"name": "bank_account_id", "type": "text", "required": True},
            {"name": "tax_profile_id", "type": "text", "required": True},
        ),
    },
    {
        "form_id": "invoice_capture",
        "title": "Invoice Intake and Match Review",
        "permission": "ap_automation.invoice",
        "dataset": "invoice_capture_queue",
        "submit_action": "capture_invoice",
        "fields": (
            {"name": "invoice_id", "type": "text", "required": True},
            {"name": "supplier_invoice_number", "type": "text", "required": True},
            {"name": "po_id", "type": "lookup", "required": True},
            {"name": "receipt_id", "type": "lookup", "required": True},
            {"name": "artifact_channel", "type": "select", "options": ("email", "portal", "api")},
        ),
    },
    {
        "form_id": "payment_batch_release",
        "title": "Payment Batch Release",
        "permission": "ap_automation.payment",
        "dataset": "payment_release",
        "submit_action": "create_payment_batch",
        "fields": (
            {"name": "batch_id", "type": "text", "required": True},
            {"name": "payment_ids", "type": "multiselect", "required": True},
            {"name": "rail", "type": "select", "options": ("ach", "wire", "instant_bank_api")},
            {"name": "scheduled_date", "type": "date", "required": False},
        ),
    },
    {
        "form_id": "vendor_statement_reconciliation",
        "title": "Vendor Statement Reconciliation",
        "permission": "ap_automation.payment",
        "dataset": "statement_reconciliation",
        "submit_action": "reconcile_vendor_statement",
        "fields": (
            {"name": "statement_id", "type": "text", "required": True},
            {"name": "vendor_id", "type": "lookup", "required": True},
            {"name": "lines", "type": "grid", "required": True},
        ),
    },
)


def form_contract() -> dict:
    """Return the AP form catalog backed by owned-table repository datasets."""
    return {
        "format": "appgen.ap-automation-forms.v1",
        "ok": bool(FORM_DEFINITIONS),
        "pbc": "ap_automation",
        "forms": FORM_DEFINITIONS,
        "permission_model": ap_automation_permissions_contract(),
        "database_backed": True,
        "side_effects": (),
    }



def _invoice_capture_defaults(state: dict, tenant: str) -> dict:
    purchase_orders = tuple(
        po_id
        for po_id, purchase_order in state.get("purchase_orders", {}).items()
        if purchase_order["tenant"] == tenant
    )
    receipts = tuple(
        receipt_id
        for receipt_id, receipt in state.get("receipts", {}).items()
        if receipt["tenant"] == tenant
    )
    return {
        "artifact_channel": "email",
        "candidate_purchase_orders": purchase_orders,
        "candidate_receipts": receipts,
    }



def render_form(
    form_id: str,
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...] = (),
) -> dict:
    """Render a data-bound form using repository datasets only."""
    definition = next((form for form in FORM_DEFINITIONS if form["form_id"] == form_id), None)
    if definition is None:
        return {"ok": False, "reason": "unknown_form", "form_id": form_id, "side_effects": ()}
    repository = ApAutomationRepository()
    snapshot = repository.tenant_snapshot(state, tenant)
    dataset = snapshot["datasets"][definition["dataset"]]
    allowed = definition["permission"] in set(principal_permissions)
    if form_id == "vendor_onboarding":
        defaults = {
            "activation_requirements": ("approval", "bank_validation", "tax_profile", "screening"),
        }
    elif form_id == "invoice_capture":
        defaults = _invoice_capture_defaults(state, tenant)
    elif form_id == "payment_batch_release":
        defaults = {
            "payment_ids": tuple(
                row["payment_id"]
                for row in dataset
                if row.get("status") == "scheduled" and row.get("payment_id")
            ),
            "rail": "ach",
        }
    elif form_id == "vendor_statement_reconciliation":
        defaults = {
            "vendor_candidates": tuple(
                row["vendor_id"]
                for row in snapshot["datasets"]["vendor_readiness"]
                if row.get("vendor_id")
            ),
        }
    else:
        defaults = {}
    return {
        "ok": allowed,
        "form_id": form_id,
        "title": definition["title"],
        "permission": definition["permission"],
        "allowed": allowed,
        "dataset": definition["dataset"],
        "fields": definition["fields"],
        "defaults": defaults,
        "record_count": len(dataset),
        "repository_binding": repository.binding_for_form(form_id)["binding"],
        "side_effects": (),
    }



def smoke_test() -> dict:
    """Exercise all AP forms against repository-backed data bindings."""
    from .repository import build_demo_state

    permissions = tuple(ap_automation_permissions_contract()["permissions"])
    state = build_demo_state(include_release=False)
    rendered = tuple(
        render_form(form["form_id"], state, tenant="tenant_repo", principal_permissions=permissions)
        for form in FORM_DEFINITIONS
    )
    return {
        "ok": form_contract()["ok"] and all(item["ok"] for item in rendered),
        "contract": form_contract(),
        "rendered": rendered,
        "side_effects": (),
    }
