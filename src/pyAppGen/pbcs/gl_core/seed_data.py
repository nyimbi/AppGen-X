"""Executable seed-data contract for the gl_core PBC."""

from __future__ import annotations

PBC_KEY = "gl_core"
SEED_DATA = (
    {
        "table": "gl_core_ledger_account",
        "rows": (
            {"tenant": "tenant_demo", "account_id": "cash_main", "account_code": "1000", "account_type": "asset", "normal_balance": 1, "parent_account_id": "root_assets"},
            {"tenant": "tenant_demo", "account_id": "accounts_receivable", "account_code": "1100", "account_type": "asset", "normal_balance": 1, "parent_account_id": "root_assets"},
            {"tenant": "tenant_demo", "account_id": "product_revenue", "account_code": "4000", "account_type": "revenue", "normal_balance": -1, "parent_account_id": "root_revenue"},
            {"tenant": "tenant_demo", "account_id": "tax_payable", "account_code": "2100", "account_type": "liability", "normal_balance": -1, "parent_account_id": "root_liabilities"},
        ),
    },
    {
        "table": "gl_core_accounting_period",
        "rows": (
            {"tenant": "tenant_demo", "period_id": "2026-05", "fiscal_year": "2026", "period_number": "05", "status": "open", "closed_at": ""},
        ),
    },
    {
        "table": "gl_core_policy_rule",
        "rows": (
            {
                "tenant": "tenant_demo",
                "rule_id": "gl_core.balance_and_materiality",
                "scope": "journal_posting",
                "status": "active",
                "predicate": {"requires_balance": True, "requires_approval_over": 1000},
                "decision_effect": "enforce",
            },
        ),
    },
    {
        "table": "gl_core_tenant_ledger_partition",
        "rows": (
            {
                "tenant": "tenant_demo",
                "partition_id": "tenant_demo-primary",
                "encryption_key_ref": "kms://tenant_demo/gl-primary",
                "residency_region": "us-east-1",
                "retention_policy": "7_year_finance_archive",
            },
        ),
    },
)
_IDENTITY_FIELDS = {
    "gl_core_ledger_account": "account_id",
    "gl_core_accounting_period": "period_id",
    "gl_core_policy_rule": "rule_id",
    "gl_core_tenant_ledger_partition": "partition_id",
}


def seed_plan():
    """Return deterministic seed rows without applying them."""
    tables = tuple(dict.fromkeys(item["table"] for item in SEED_DATA))
    row_count = sum(len(item.get("rows", ())) for item in SEED_DATA)
    return {
        "ok": bool(SEED_DATA) and row_count >= 4,
        "pbc": PBC_KEY,
        "tables": tables,
        "rows": SEED_DATA,
        "row_count": row_count,
        "side_effects": (),
    }


def validate_seed_data():
    """Validate seed ownership and minimum row shape."""
    invalid_tables = tuple(
        item["table"] for item in SEED_DATA if not item.get("table", "").startswith(f"{PBC_KEY}_")
    )
    invalid_rows = tuple(
        {"table": item["table"], "row": row}
        for item in SEED_DATA
        for row in item.get("rows", ())
        if not row.get("tenant") or not row.get(_IDENTITY_FIELDS.get(item["table"], "id"))
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


def smoke_test():
    """Exercise seed validation without writing rows."""
    return validate_seed_data()
