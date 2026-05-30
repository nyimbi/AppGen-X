"""Guided workflows for the standalone Returns Reverse Logistics PBC."""
from .forms import returns_reverse_logistics_form_catalog
PBC_KEY = "returns_reverse_logistics"
WIZARDS = (
    {"wizard_id": "return_authorization_to_label", "steps": ("returns_configuration", "return_rule", "return_authorization", "return_label")},
    {"wizard_id": "receipt_inspection_disposition", "steps": ("return_receipt", "inspection_grade", "credit_adjustment")},
    {"wizard_id": "refund_exchange_and_claim", "steps": ("refund_exchange_resolution", "carrier_claim")},
    {"wizard_id": "exception_resolution", "steps": ("exception_case",)},
    {"wizard_id": "assistant_document_to_return_action", "steps": ("document_instruction_intake", "return_authorization")},
)

def returns_reverse_logistics_wizard_catalog():
    form_ids = set(returns_reverse_logistics_form_catalog()["form_ids"])
    missing = tuple(step for wizard in WIZARDS for step in wizard["steps"] if step not in form_ids)
    return {"ok": not missing, "pbc": PBC_KEY, "wizards": WIZARDS, "wizard_ids": tuple(item["wizard_id"] for item in WIZARDS), "missing_form_bindings": missing, "side_effects": ()}

def returns_reverse_logistics_plan_wizard(wizard_id, context=None):
    supplied = dict(context or {})
    wizard = next((item for item in WIZARDS if item["wizard_id"] == wizard_id), None)
    if wizard is None:
        return {"ok": False, "pbc": PBC_KEY, "wizard_id": wizard_id, "steps": (), "side_effects": ()}
    steps = tuple({"step": step, "ready": bool(supplied) or index == 0, "blocked_by": () if (bool(supplied) or index == 0) else (wizard["steps"][index - 1],)} for index, step in enumerate(wizard["steps"]))
    return {"ok": bool(supplied) or all(step["ready"] for step in steps), "pbc": PBC_KEY, "wizard_id": wizard_id, "steps": steps, "side_effects": ()}

def smoke_test():
    catalog = returns_reverse_logistics_wizard_catalog()
    plan = returns_reverse_logistics_plan_wizard("receipt_inspection_disposition", {"return_id": "ret_demo"})
    return {"ok": catalog["ok"] and plan["ok"], "catalog": catalog, "plan": plan, "side_effects": ()}
