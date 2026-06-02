"""Controls and governed mutation previews for Subscription Billing."""

from .runtime import SUBSCRIPTION_BILLING_SCHEMA_TABLES

PBC_KEY = "subscription_billing"
CONTROL_DEFINITIONS = (
    {"control_id": "event_contract_locked", "description": "AppGen-X subscription event contract is enforced."},
    {"control_id": "invoice_payment_revenue_chain", "description": "Invoices, payments, entitlements, and revenue schedules stay reconciled."},
    {"control_id": "retry_dead_letter_evidence", "description": "Consumed event handlers produce retry and dead-letter evidence."},
    {"control_id": "owned_table_boundary", "description": "Mutations stay inside subscription_billing owned tables."},
    {"control_id": "assistant_mutation_preview", "description": "Assistant writes require preview and confirmation."},
)


def subscription_billing_control_catalog():
    return {"ok": True, "pbc": PBC_KEY, "controls": CONTROL_DEFINITIONS, "control_ids": tuple(item["control_id"] for item in CONTROL_DEFINITIONS), "side_effects": ()}


def subscription_billing_mutation_preview(action, table, payload=None):
    full_tables = tuple(table if table.startswith(PBC_KEY + "_") else PBC_KEY + "_" + table for table in SUBSCRIPTION_BILLING_SCHEMA_TABLES)
    allowed = table in full_tables and str(action).lower() in {"create", "read", "update", "delete"}
    return {"ok": allowed, "pbc": PBC_KEY, "action": str(action).lower(), "table": table, "payload_keys": tuple(sorted(dict(payload or {}))), "boundary": {"ok": table in full_tables, "owned_tables": full_tables}, "requires_confirmation": str(action).lower() != "read", "side_effects": ()}


def subscription_billing_control_center():
    catalog = subscription_billing_control_catalog()
    return {"ok": catalog["ok"], "pbc": PBC_KEY, "controls": catalog["controls"], "assistant_guardrails": {"preview_only": True, "boundary_ok": True}, "side_effects": ()}


def smoke_test():
    catalog = subscription_billing_control_catalog()
    preview = subscription_billing_mutation_preview("update", "subscription_billing_subscription", {"status": "active"})
    return {"ok": catalog["ok"] and preview["ok"], "catalog": catalog, "preview": preview, "side_effects": ()}
