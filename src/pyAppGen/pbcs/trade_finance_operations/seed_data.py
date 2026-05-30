"""Seed data hooks for trade_finance_operations."""

from __future__ import annotations

PBC_KEY = "trade_finance_operations"


def seed_plan():
    records = (
        {"table": "trade_finance_operations_letter_of_credit", "code": "LC-SEED-001", "status": "draft"},
        {"table": "trade_finance_operations_bank_guarantee", "code": "BG-SEED-001", "status": "active"},
        {"table": "trade_finance_operations_documentary_collection", "code": "DC-SEED-001", "status": "awaiting_documents"},
    )
    return {"ok": True, "pbc": PBC_KEY, "records": records, "side_effects": ()}


def validate_seed_data():
    records = seed_plan()["records"]
    ok = all(record["table"].startswith(f"{PBC_KEY}_") and record["code"] for record in records)
    return {"ok": ok, "pbc": PBC_KEY, "side_effects": ()}


def smoke_test():
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
