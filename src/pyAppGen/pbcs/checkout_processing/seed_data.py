"""Executable seed-data contract for the checkout_processing PBC."""

from __future__ import annotations


PBC_KEY = "checkout_processing"
SEED_DATA = (
    {
        "table": "checkout_processing_checkout_configuration",
        "rows": (
            {
                "configuration_id": "cfg_default",
                "database_backend": "postgresql",
                "event_topic": "appgen.checkout.events",
                "default_currency": "USD",
                "default_country": "US",
            },
        ),
    },
    {
        "table": "checkout_processing_checkout_parameter",
        "rows": (
            {"parameter_id": "param_risk_threshold", "name": "risk_threshold", "value": "0.65", "tenant_scope": "default"},
            {"parameter_id": "param_retry_limit", "name": "max_retry_attempts", "value": "3", "tenant_scope": "default"},
        ),
    },
    {
        "table": "checkout_processing_checkout_rule",
        "rows": (
            {
                "rule_id": "rule_checkout_default",
                "tenant": "tenant_alpha",
                "scope": "checkout_guard",
                "status": "active",
            },
        ),
    },
)


def seed_plan() -> dict:
    """Return deterministic seed rows without applying them."""
    tables = tuple(dict.fromkeys(item["table"] for item in SEED_DATA))
    return {
        "ok": bool(SEED_DATA),
        "pbc": PBC_KEY,
        "tables": tables,
        "rows": SEED_DATA,
        "side_effects": (),
    }


def validate_seed_data() -> dict:
    """Validate seed ownership and minimum row shape."""
    invalid_tables = tuple(
        item["table"] for item in SEED_DATA if not item.get("table", "").startswith(f"{PBC_KEY}_")
    )
    invalid_rows = tuple(
        row
        for item in SEED_DATA
        for row in item.get("rows", ())
        if not any(key.endswith("_id") or key == "rule_id" for key in row)
    )
    plan = seed_plan()
    return {
        "ok": plan["ok"] and not invalid_tables and not invalid_rows,
        "pbc": PBC_KEY,
        "plan": plan,
        "invalid_tables": invalid_tables,
        "invalid_rows": invalid_rows,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise seed validation without writing rows."""
    return validate_seed_data()
