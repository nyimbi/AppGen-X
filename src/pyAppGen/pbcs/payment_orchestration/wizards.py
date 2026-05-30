"""Guided workflows for the standalone Payment Orchestration PBC."""

from .forms import payment_orchestration_form_catalog

PBC_KEY = "payment_orchestration"
WIZARDS = (
    {"wizard_id": "payment_acceptance_setup", "steps": ("payment_configuration", "payment_gateway", "payment_token", "payment_intent")},
    {"wizard_id": "authorize_capture_settle", "steps": ("payment_intent", "payment_capture")},
    {"wizard_id": "refund_and_dispute_resolution", "steps": ("payment_refund", "payment_dispute")},
    {"wizard_id": "assistant_document_to_payment_action", "steps": ("document_instruction_intake", "payment_capture")},
)


def payment_orchestration_wizard_catalog():
    form_ids = set(payment_orchestration_form_catalog()["form_ids"])
    missing = tuple(step for wizard in WIZARDS for step in wizard["steps"] if step not in form_ids)
    return {"ok": not missing, "pbc": PBC_KEY, "wizards": WIZARDS, "wizard_ids": tuple(item["wizard_id"] for item in WIZARDS), "missing_form_bindings": missing, "side_effects": ()}


def payment_orchestration_plan_wizard(wizard_id, context=None):
    supplied = dict(context or {})
    wizard = next((item for item in WIZARDS if item["wizard_id"] == wizard_id), None)
    if wizard is None:
        return {"ok": False, "pbc": PBC_KEY, "wizard_id": wizard_id, "steps": (), "side_effects": ()}
    steps = tuple({"step": step, "ready": bool(supplied) or index == 0, "blocked_by": () if (bool(supplied) or index == 0) else (wizard["steps"][index - 1],)} for index, step in enumerate(wizard["steps"]))
    return {"ok": all(not step["blocked_by"] for step in steps) or bool(supplied), "pbc": PBC_KEY, "wizard_id": wizard_id, "steps": steps, "side_effects": ()}


def smoke_test():
    catalog = payment_orchestration_wizard_catalog()
    plan = payment_orchestration_plan_wizard("payment_acceptance_setup", {"tenant": "tenant_demo"})
    return {"ok": catalog["ok"] and plan["ok"], "catalog": catalog, "plan": plan, "side_effects": ()}
