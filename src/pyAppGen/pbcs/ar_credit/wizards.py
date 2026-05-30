"""Package-local guided wizards for the standalone ar_credit workbench."""

from __future__ import annotations

from .forms import ar_credit_form_catalog


AR_CREDIT_WIZARDS = (
    {
        "wizard_id": "customer_activation",
        "title": "Customer activation",
        "goal": "Take a new customer from evidence review to an approved credit-ready account.",
        "steps": (
            {"step_id": "collect_credit_pack", "label": "Collect onboarding pack", "form_id": "customer_credit_onboarding", "operation": "command_ar_customers"},
            {"step_id": "review_credit_limit", "label": "Review recommended limit", "form_id": "customer_credit_onboarding", "operation": "review_credit_onboarding"},
        ),
    },
    {
        "wizard_id": "invoice_to_cash_cycle",
        "title": "Invoice to cash",
        "goal": "Issue a compliant invoice, apply cash, and inspect remaining exposure.",
        "steps": (
            {"step_id": "activate_customer", "label": "Activate customer", "form_id": "customer_credit_onboarding", "operation": "command_ar_customers"},
            {"step_id": "issue_invoice", "label": "Issue invoice", "form_id": "invoice_issuance", "operation": "command_ar_invoices"},
            {"step_id": "apply_receipt", "label": "Apply receipt", "form_id": "cash_receipt_application", "operation": "command_ar_cash_applications"},
            {"step_id": "inspect_follow_up", "label": "Inspect follow-up", "form_id": "collections_follow_up", "operation": "command_ar_collections"},
        ),
    },
    {
        "wizard_id": "collections_recovery",
        "title": "Collections recovery",
        "goal": "Drive aging, statement, dunning, and next-best collection action for a delinquent account.",
        "steps": (
            {"step_id": "review_customer_statement", "label": "Review statement", "form_id": "collections_follow_up", "operation": "build_collections_follow_up"},
            {"step_id": "prepare_dunning", "label": "Prepare dunning", "form_id": "collections_follow_up", "operation": "command_ar_collections"},
            {"step_id": "confirm_cash_resolution", "label": "Confirm cash resolution", "form_id": "cash_receipt_application", "operation": "command_ar_cash_applications"},
        ),
    },
    {
        "wizard_id": "release_readiness",
        "title": "Release readiness",
        "goal": "Confirm forms, controls, assistant previews, and runtime evidence are ready to ship.",
        "steps": (
            {"step_id": "check_forms", "label": "Check forms", "form_id": "customer_credit_onboarding", "operation": "ar_credit_form_catalog"},
            {"step_id": "check_workflows", "label": "Check workflows", "form_id": "collections_follow_up", "operation": "build_collections_follow_up"},
            {"step_id": "check_controls", "label": "Check controls", "form_id": "collections_follow_up", "operation": "ar_credit_control_center"},
        ),
    },
)


def ar_credit_wizard_catalog() -> dict:
    forms = ar_credit_form_catalog()
    form_ids = set(forms["form_ids"])
    missing_form_bindings = tuple(
        f"{wizard['wizard_id']}:{step['step_id']}"
        for wizard in AR_CREDIT_WIZARDS
        for step in wizard["steps"]
        if step["form_id"] not in form_ids
    )
    return {
        "ok": bool(AR_CREDIT_WIZARDS) and not missing_form_bindings,
        "pbc": "ar_credit",
        "wizards": AR_CREDIT_WIZARDS,
        "wizard_ids": tuple(item["wizard_id"] for item in AR_CREDIT_WIZARDS),
        "missing_form_bindings": missing_form_bindings,
        "side_effects": (),
    }


def ar_credit_plan_wizard(wizard_id: str, context: dict | None = None) -> dict:
    wizard = next((item for item in AR_CREDIT_WIZARDS if item["wizard_id"] == wizard_id), None)
    if wizard is None:
        return {"ok": False, "reason": "unknown_wizard", "wizard_id": wizard_id, "side_effects": ()}

    supplied = dict(context or {})
    planned_steps = []
    for position, step in enumerate(wizard["steps"], start=1):
        blocked_by = ()
        if wizard_id in {"invoice_to_cash_cycle", "collections_recovery"} and step["step_id"] != "activate_customer" and not supplied.get("customer_id"):
            blocked_by = ("customer_id",)
        if step["form_id"] == "collections_follow_up" and not supplied.get("as_of"):
            blocked_by = tuple(dict.fromkeys((*blocked_by, "as_of")))
        planned_steps.append({
            **step,
            "position": position,
            "ready": not blocked_by,
            "blocked_by": blocked_by,
        })
    return {
        "ok": True,
        "pbc": "ar_credit",
        "wizard_id": wizard_id,
        "goal": wizard["goal"],
        "steps": tuple(planned_steps),
        "side_effects": (),
    }


def smoke_test() -> dict:
    catalog = ar_credit_wizard_catalog()
    plan = ar_credit_plan_wizard(
        "invoice_to_cash_cycle",
        {"customer_id": "cust-demo", "as_of": "2026-06-30"},
    )
    return {
        "ok": catalog["ok"] and plan["ok"] and bool(plan["steps"]),
        "catalog": catalog,
        "plan": plan,
        "side_effects": (),
    }
