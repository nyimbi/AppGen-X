"""Seed data for the customer_success_management PBC."""
from __future__ import annotations

from .slice_app import PBC_KEY, build_seed_plan

SEED_ROWS = tuple(build_seed_plan()["rows"])


def seed_plan() -> dict:
    return build_seed_plan()


def validate_seed_data() -> dict:
    return {
        "ok": all(row["table"].startswith(f"{PBC_KEY}_") for row in SEED_ROWS),
        "rows": SEED_ROWS,
        "side_effects": (),
    }


def smoke_test() -> dict:
    plan = seed_plan()
    validation = validate_seed_data()
    return {"ok": plan["ok"] and validation["ok"], "side_effects": ()}
