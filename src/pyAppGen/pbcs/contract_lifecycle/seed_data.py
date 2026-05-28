"""Seed data for the contract_lifecycle PBC."""

from .application import PBC_KEY, seed_rows

SEED_ROWS = seed_rows()


def seed_plan():
    return {"ok": True, "pbc": PBC_KEY, "rows": SEED_ROWS}


def validate_seed_data():
    invalid = tuple(row for row in SEED_ROWS if not row["table"].startswith(f"{PBC_KEY}_"))
    return {"ok": not invalid, "rows": SEED_ROWS, "invalid": invalid}


def smoke_test():
    validation = validate_seed_data()
    return {"ok": seed_plan()["ok"] and validation["ok"], "validation": validation}
