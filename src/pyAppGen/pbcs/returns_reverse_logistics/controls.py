"""Controls and governed mutation previews for Returns Reverse Logistics."""
from .runtime import RETURNS_REVERSE_LOGISTICS_OWNED_TABLES
PBC_KEY = "returns_reverse_logistics"
CONTROL_DEFINITIONS = (
    {"control_id": "event_contract_locked", "description": "AppGen-X return event contract is enforced."},
    {"control_id": "rma_to_credit_chain", "description": "Authorization, label, receipt, inspection, disposition, credit, and status are connected."},
    {"control_id": "retry_dead_letter_evidence", "description": "Inbox handlers produce retry and dead-letter evidence."},
    {"control_id": "owned_table_boundary", "description": "Mutations stay inside returns_reverse_logistics owned tables."},
    {"control_id": "assistant_mutation_preview", "description": "Assistant writes require preview and confirmation."},
)

def returns_reverse_logistics_control_catalog():
    return {"ok": True, "pbc": PBC_KEY, "controls": CONTROL_DEFINITIONS, "control_ids": tuple(item["control_id"] for item in CONTROL_DEFINITIONS), "side_effects": ()}

def returns_reverse_logistics_mutation_preview(action, table, payload=None):
    full_tables = tuple(table if table.startswith(PBC_KEY + "_") else PBC_KEY + "_" + table for table in RETURNS_REVERSE_LOGISTICS_OWNED_TABLES)
    allowed = table in full_tables and str(action).lower() in {"create", "read", "update", "delete"}
    return {"ok": allowed, "pbc": PBC_KEY, "action": str(action).lower(), "table": table, "payload_keys": tuple(sorted(dict(payload or {}))), "boundary": {"ok": table in full_tables, "owned_tables": full_tables}, "requires_confirmation": str(action).lower() != "read", "side_effects": ()}

def returns_reverse_logistics_control_center():
    catalog = returns_reverse_logistics_control_catalog()
    return {"ok": catalog["ok"], "pbc": PBC_KEY, "controls": catalog["controls"], "assistant_guardrails": {"preview_only": True, "boundary_ok": True}, "side_effects": ()}

def smoke_test():
    catalog = returns_reverse_logistics_control_catalog()
    preview = returns_reverse_logistics_mutation_preview("update", "returns_reverse_logistics_return_authorization", {"status": "authorized"})
    return {"ok": catalog["ok"] and preview["ok"], "catalog": catalog, "preview": preview, "side_effects": ()}
