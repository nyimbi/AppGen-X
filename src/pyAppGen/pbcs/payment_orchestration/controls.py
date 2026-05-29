"""Controls and governed mutation previews for Payment Orchestration."""

from .runtime import PAYMENT_ORCHESTRATION_OWNED_TABLES

PBC_KEY = "payment_orchestration"
CONTROL_DEFINITIONS = (
    {"control_id": "event_contract_locked", "description": "AppGen-X event contract is enforced."},
    {"control_id": "payment_lifecycle_complete", "description": "Intents do not remain open after capture/void."},
    {"control_id": "owned_table_boundary", "description": "Mutations stay inside payment_orchestration owned tables."},
    {"control_id": "assistant_mutation_preview", "description": "Assistant writes require preview and confirmation."},
)


def payment_orchestration_control_catalog():
    return {"ok": True, "pbc": PBC_KEY, "controls": CONTROL_DEFINITIONS, "control_ids": tuple(item["control_id"] for item in CONTROL_DEFINITIONS), "side_effects": ()}


def payment_orchestration_mutation_preview(action, table, payload=None):
    full_tables = tuple(table if table.startswith(PBC_KEY + "_") else PBC_KEY + "_" + table for table in PAYMENT_ORCHESTRATION_OWNED_TABLES)
    allowed = table in full_tables and str(action).lower() in {"create", "read", "update", "delete"}
    return {"ok": allowed, "pbc": PBC_KEY, "action": str(action).lower(), "table": table, "payload_keys": tuple(sorted(dict(payload or {}))), "boundary": {"ok": table in full_tables, "owned_tables": full_tables}, "requires_confirmation": str(action).lower() != "read", "side_effects": ()}


def payment_orchestration_control_center():
    catalog = payment_orchestration_control_catalog()
    return {"ok": catalog["ok"], "pbc": PBC_KEY, "controls": catalog["controls"], "assistant_guardrails": {"preview_only": True, "boundary_ok": True}, "side_effects": ()}


def smoke_test():
    catalog = payment_orchestration_control_catalog()
    preview = payment_orchestration_mutation_preview("update", "payment_orchestration_payment_intent", {"status": "captured"})
    return {"ok": catalog["ok"] and preview["ok"], "catalog": catalog, "preview": preview, "side_effects": ()}
