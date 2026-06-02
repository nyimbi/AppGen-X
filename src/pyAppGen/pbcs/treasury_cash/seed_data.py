"""Executable seed-data contract for the treasury_cash PBC."""

PBC_KEY = "treasury_cash"
SEED_DATA = (
    {
        "table": "treasury_cash_bank_account",
        "rows": (
            {
                "external_key": "acct_seed_operating_usd",
                "tenant": "seed_tenant",
                "status": "active",
                "code": "TREASURY-CASH-OPERATING-USD",
                "payload": {
                    "account_id": "acct_seed_operating_usd",
                    "tenant": "seed_tenant",
                    "legal_entity": "Seed Holdings LLC",
                    "bank_id": "bank_seed_alpha",
                    "currency": "USD",
                    "country": "US",
                    "purpose": "operating",
                },
            },
        ),
    },
    {
        "table": "treasury_cash_bank_account_signatory",
        "rows": (
            {
                "external_key": "acct_seed_operating_usd:treasurer",
                "tenant": "seed_tenant",
                "status": "active",
                "code": "TREASURY-CASH-SIGNATORY-TREASURER",
                "payload": {
                    "account_id": "acct_seed_operating_usd",
                    "principal": "treasurer",
                    "role": "primary_signer",
                    "approval_limit": "250000",
                },
            },
        ),
    },
    {
        "table": "treasury_cash_balance",
        "rows": (
            {
                "external_key": "bal_seed_opening_usd",
                "tenant": "seed_tenant",
                "status": "captured",
                "code": "TREASURY-CASH-BALANCE-OPENING",
                "payload": {
                    "balance_id": "bal_seed_opening_usd",
                    "tenant": "seed_tenant",
                    "account_id": "acct_seed_operating_usd",
                    "value_date": "2026-01-01",
                    "amount": 250000.0,
                    "currency": "USD",
                    "kind": "opening",
                },
            },
        ),
    },
    {
        "table": "treasury_cash_rule",
        "rows": (
            {
                "external_key": "rule_seed_liquidity_floor",
                "tenant": "seed_tenant",
                "status": "active",
                "code": "TREASURY-CASH-RULE-LIQUIDITY-FLOOR",
                "payload": {
                    "rule_id": "rule_seed_liquidity_floor",
                    "tenant": "seed_tenant",
                    "scope": "liquidity",
                    "minimum_liquidity_buffer": 100000.0,
                    "dual_approval_required": True,
                },
            },
        ),
    },
    {
        "table": "treasury_cash_parameter",
        "rows": (
            {
                "external_key": "parameter_seed_counterparty_threshold",
                "tenant": "seed_tenant",
                "status": "active",
                "code": "TREASURY-CASH-PARAM-COUNTERPARTY-RISK",
                "payload": {
                    "name": "counterparty_risk_threshold",
                    "value": 0.35,
                    "bounds": {"min": 0.0, "max": 1.0},
                },
            },
        ),
    },
)



def seed_plan():
    """Return deterministic seed rows without applying them."""
    tables = tuple(dict.fromkeys(item["table"] for item in SEED_DATA))
    return {
        "ok": bool(SEED_DATA),
        "pbc": PBC_KEY,
        "tables": tables,
        "rows": SEED_DATA,
        "side_effects": (),
    }



def validate_seed_data():
    """Validate seed ownership and minimum row shape."""
    invalid_tables = tuple(
        item["table"] for item in SEED_DATA if not item.get("table", "").startswith(f"{PBC_KEY}_")
    )
    invalid_rows = tuple(
        row
        for item in SEED_DATA
        for row in item.get("rows", ())
        if not row.get("external_key")
        or not row.get("status")
        or not row.get("code")
        or not isinstance(row.get("payload"), dict)
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
