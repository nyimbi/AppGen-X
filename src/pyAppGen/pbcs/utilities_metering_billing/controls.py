"""Controls for the Utilities Metering and Billing standalone PBC app."""
from .slice_app import CONTROL_DEFINITIONS, PBC_KEY

_CONTROL_IDS = tuple(item.get("id", item.get("key", "")) for item in CONTROL_DEFINITIONS)

def control_catalog(): return {"ok": True, "pbc": PBC_KEY, "controls": _CONTROL_IDS, "definitions": CONTROL_DEFINITIONS, "side_effects": ()}

def evaluate_control(control_id, facts):
    facts = dict(facts or {})
    definition = next((item for item in CONTROL_DEFINITIONS if item.get("id") == control_id or item.get("key") == control_id), None)
    if definition is None:
        return {"ok": False, "control_id": control_id, "missing": ("known_control",), "side_effects": ()}
    required = tuple(definition.get("required_fields", definition.get("fields", ())))
    missing = tuple(name for name in required if facts.get(name) in (None, "", (), [], {}))
    ok = not missing
    if control_id == "agent_mutation_confirmation":
        ok = facts.get("confirmed") is True
        missing = () if ok else ("confirmed",)
    if control_id == "disconnect_moratorium_guard" and ok:
        ok = facts.get("moratorium_enabled") is not True or facts.get("protected_customer") is not True
        missing = () if ok else ("moratorium_override_prohibited",)
    return {"ok": ok, "control_id": control_id, "missing": missing, "side_effects": ()}
