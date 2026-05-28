from typing import Any

PBC_KEY = "banking_core_accounts"
SEED_TABLE = "banking_core_accounts_deposit_account"


def seed_plan() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "records": (
            {
                "table": SEED_TABLE,
                "account_id": "SEED-001",
                "account_number": "SEED0001",
                "customer_id": "CUSTOMER-SEED",
                "product_code": "SAVINGS",
                "currency": "KES",
                "lifecycle_state": "pending",
            },
        ),
        "side_effects": (),
    }


def validate_seed_data() -> dict[str, Any]:
    plan = seed_plan()
    return {
        "ok": plan["ok"] and all(record["table"].startswith(f"{PBC_KEY}_") for record in plan["records"]),
        "pbc": PBC_KEY,
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
