"""Guided workflows for the standalone Subscription Billing PBC."""

from .forms import subscription_billing_form_catalog

PBC_KEY = "subscription_billing"
WIZARDS = (
    {"wizard_id": "subscription_launch", "steps": ("billing_configuration", "plan_catalog", "trial_period", "subscription")},
    {"wizard_id": "usage_to_invoice", "steps": ("usage_meter", "invoice", "payment_application")},
    {"wizard_id": "credit_and_dunning", "steps": ("credit_memo", "dunning_notice")},
    {"wizard_id": "subscription_change", "steps": ("subscription_change", "invoice")},
    {"wizard_id": "assistant_document_to_billing_action", "steps": ("document_instruction_intake", "invoice")},
)


def subscription_billing_wizard_catalog():
    form_ids = set(subscription_billing_form_catalog()["form_ids"])
    missing = tuple(step for wizard in WIZARDS for step in wizard["steps"] if step not in form_ids)
    return {"ok": not missing, "pbc": PBC_KEY, "wizards": WIZARDS, "wizard_ids": tuple(item["wizard_id"] for item in WIZARDS), "missing_form_bindings": missing, "side_effects": ()}


def subscription_billing_plan_wizard(wizard_id, context=None):
    supplied = dict(context or {})
    wizard = next((item for item in WIZARDS if item["wizard_id"] == wizard_id), None)
    if wizard is None:
        return {"ok": False, "pbc": PBC_KEY, "wizard_id": wizard_id, "steps": (), "side_effects": ()}
    steps = tuple({"step": step, "ready": bool(supplied) or index == 0, "blocked_by": () if (bool(supplied) or index == 0) else (wizard["steps"][index - 1],)} for index, step in enumerate(wizard["steps"]))
    return {"ok": bool(supplied) or all(step["ready"] for step in steps), "pbc": PBC_KEY, "wizard_id": wizard_id, "steps": steps, "side_effects": ()}


def smoke_test():
    catalog = subscription_billing_wizard_catalog()
    plan = subscription_billing_plan_wizard("subscription_launch", {"tenant": "tenant_demo"})
    return {"ok": catalog["ok"] and plan["ok"], "catalog": catalog, "plan": plan, "side_effects": ()}
