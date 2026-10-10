from __future__ import annotations

from .runtime import seed_plan as _seed_plan
from .runtime import validate_seed_data as _validate_seed_data


def seed_plan():
    return _seed_plan()


def validate_seed_data():
    return _validate_seed_data()


def smoke_test():
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
