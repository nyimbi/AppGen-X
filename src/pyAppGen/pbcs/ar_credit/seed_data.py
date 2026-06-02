"""Executable seed data for the standalone ar_credit PBC app."""

from __future__ import annotations

from .runtime import AR_CREDIT_REQUIRED_EVENT_TOPIC
from .runtime import ar_credit_configure_runtime
from .runtime import ar_credit_empty_state
from .runtime import ar_credit_set_parameter
from .runtime import ar_credit_register_rule
from .services import ArCreditService


DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": AR_CREDIT_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "default_currency": "USD",
    "default_timezone": "UTC",
    "allowed_collection_channels": ("portal", "api", "email"),
    "workbench_limit": 100,
}
DEFAULT_PARAMETERS = {
    "auto_cash_threshold": 0.95,
    "credit_limit_buffer": 0.1,
    "collection_risk_threshold": 0.45,
    "dunning_grace_days": 5,
    "write_off_approval_limit": 500.0,
    "workbench_limit": 100,
}
DEFAULT_RULE = {
    "rule_id": "ar_credit.release_readiness",
    "tenant": "tenant_demo",
    "scope": "cash_application",
    "status": "active",
    "auto_cash_threshold": 0.95,
    "requires_delivery_confirmation": False,
}
DEMO_CUSTOMER = {
    "customer_id": "cust-tenant_demo",
    "tenant": "tenant_demo",
    "name": "Northwind Retail",
    "parent": "northwind_group",
    "beneficial_owners": ("owner_nw_1", "owner_nw_2"),
    "requested_limit": 2500,
    "terms": {"net_days": 30, "discount_days": 10, "discount_rate": 0.01},
    "risk_signals": {"payment_latency": 0.04, "industry_stress": 0.08, "sanction_hits": 0},
    "identity": {"did": "did:appgen:northwind-retail", "issuer": "trusted_registry", "status": "active"},
}
DEMO_INVOICE = {
    "invoice_id": "inv-tenant_demo-1001",
    "tenant": "tenant_demo",
    "customer_id": "cust-tenant_demo",
    "currency": "USD",
    "invoice_date": "2026-05-01",
    "due_date": "2026-05-31",
    "tax": {"jurisdiction": "US-NY", "amount": 12.0, "rate": 0.08},
    "performance_obligations": ({"obligation": "monthly_service", "allocation": 150.0, "satisfied": True},),
    "lines": ({"sku": "svc-monthly", "quantity": 1, "unit_price": 150.0, "account": "revenue"},),
}
DEMO_RECEIPT = {
    "receipt_id": "rcpt-tenant_demo-9001",
    "tenant": "tenant_demo",
    "customer_id": "cust-tenant_demo",
    "amount": 162.0,
    "currency": "USD",
    "remittance_text": "PAY inv-tenant_demo-1001 amount 162 bank_ref BAI-9001",
}


def seed_plan(tenant: str = "tenant_demo") -> dict:
    customer = {**DEMO_CUSTOMER, "tenant": tenant, "customer_id": f"cust-{tenant}"}
    invoice = {**DEMO_INVOICE, "tenant": tenant, "customer_id": customer["customer_id"], "invoice_id": f"inv-{tenant}-1001"}
    receipt = {**DEMO_RECEIPT, "tenant": tenant, "customer_id": customer["customer_id"], "receipt_id": f"rcpt-{tenant}-9001", "remittance_text": f"PAY {invoice['invoice_id']} amount 162 bank_ref BAI-9001"}
    return {
        "ok": True,
        "pbc": "ar_credit",
        "tenant": tenant,
        "configuration": DEFAULT_CONFIGURATION,
        "parameters": DEFAULT_PARAMETERS,
        "rule": {**DEFAULT_RULE, "tenant": tenant},
        "actions": (
            {"operation": "command_ar_customers", "table": "ar_customer", "payload": customer},
            {"operation": "command_ar_invoices", "table": "ar_invoice", "payload": invoice},
            {"operation": "command_ar_cash_applications", "table": "ar_cash_receipt", "payload": receipt},
            {"operation": "command_ar_collections", "table": "ar_collection_action", "payload": {"customer_id": customer["customer_id"], "as_of": "2026-06-30"}},
        ),
        "tables": ("ar_customer", "ar_invoice", "ar_cash_receipt", "ar_collection_action"),
        "side_effects": (),
    }


def load_demo_state(tenant: str = "tenant_demo", *, include_transactions: bool = True) -> dict:
    state = ar_credit_empty_state()
    state = ar_credit_configure_runtime(state, DEFAULT_CONFIGURATION)["state"]
    for key, value in DEFAULT_PARAMETERS.items():
        state = ar_credit_set_parameter(state, key, value)["state"]
    state = ar_credit_register_rule(state, {**DEFAULT_RULE, "tenant": tenant})["state"]
    if include_transactions is not True:
        return {"ok": True, "tenant": tenant, "state": state, "side_effects": ()}

    plan = seed_plan(tenant)
    customer_payload = dict(plan["actions"][0]["payload"])
    invoice_payload = dict(plan["actions"][1]["payload"])
    receipt_payload = dict(plan["actions"][2]["payload"])
    service = ArCreditService(state=state)
    customer = service.command_ar_customers({"customer": customer_payload})
    invoice = service.command_ar_invoices({"invoice": invoice_payload})
    receipt = service.command_ar_cash_applications({"receipt": receipt_payload})
    follow_up = service.command_ar_collections({"customer_id": customer_payload["customer_id"], "as_of": "2026-06-30"})
    return {
        "ok": customer["ok"] and invoice["ok"] and receipt["ok"] and follow_up["ok"],
        "tenant": tenant,
        "state": service.state,
        "customer": customer["customer"],
        "invoice": invoice["invoice"],
        "receipt": receipt_payload,
        "follow_up": follow_up["follow_up"],
        "plan": plan,
        "side_effects": (),
    }


def validate_seed_data() -> dict:
    plan = seed_plan()
    invalid_tables = tuple(table for table in plan["tables"] if not table.startswith("ar_"))
    invalid_actions = tuple(
        action["operation"]
        for action in plan["actions"]
        if not action["payload"]
    )
    return {
        "ok": plan["ok"] and not invalid_tables and not invalid_actions,
        "pbc": "ar_credit",
        "plan": plan,
        "invalid_tables": invalid_tables,
        "invalid_actions": invalid_actions,
        "side_effects": (),
    }


def smoke_test() -> dict:
    seeded = load_demo_state()
    validation = validate_seed_data()
    return {
        "ok": seeded["ok"] and validation["ok"] and bool(seeded["state"]["outbox"]),
        "seeded": seeded,
        "validation": validation,
        "side_effects": (),
    }
