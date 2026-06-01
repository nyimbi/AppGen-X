from .slice_app import seed_plan as _seed_plan
from .slice_app import validate_seed_data as _validate_seed_data


def smoke_test():
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}


def seed_plan() -> dict:
    return _seed_plan()


def validate_seed_data() -> dict:
    return _validate_seed_data()
