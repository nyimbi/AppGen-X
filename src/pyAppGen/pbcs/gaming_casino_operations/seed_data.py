"""Seed-data hooks for gaming_casino_operations."""

from __future__ import annotations

from typing import Any

from .models import PLAYER_PROFILE_TABLE, POLICY_RULE_TABLE, RUNTIME_PARAMETER_TABLE, SLOT_MACHINE_TABLE, TABLE_GAME_TABLE


PBC_KEY = "gaming_casino_operations"


def seed_plan() -> dict[str, Any]:
    records = (
        {
            "table": PLAYER_PROFILE_TABLE,
            "code": "PLAYER-SEED-001",
            "tenant": "tenant_seed",
            "legal_name": "Seed Patron",
        },
        {
            "table": TABLE_GAME_TABLE,
            "code": "TABLE-SEED-001",
            "tenant": "tenant_seed",
            "table_number": "BJ-01",
        },
        {
            "table": SLOT_MACHINE_TABLE,
            "code": "SLOT-SEED-001",
            "tenant": "tenant_seed",
            "asset_code": "SL-01",
        },
        {
            "table": POLICY_RULE_TABLE,
            "code": "RULE-SEED-001",
            "tenant": "tenant_seed",
            "rule_id": "player_profile_policy",
        },
        {
            "table": RUNTIME_PARAMETER_TABLE,
            "code": "PARAM-SEED-001",
            "tenant": "tenant_seed",
            "parameter_name": "workbench_limit",
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "records": records, "side_effects": ()}


def validate_seed_data() -> dict[str, Any]:
    plan = seed_plan()
    invalid = tuple(record for record in plan["records"] if not record["table"].startswith(f"{PBC_KEY}_"))
    return {"ok": not invalid, "pbc": PBC_KEY, "invalid": invalid, "side_effects": ()}


def smoke_test() -> dict[str, Any]:
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
