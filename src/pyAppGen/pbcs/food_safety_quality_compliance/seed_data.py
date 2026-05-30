from .slice_app import seed_plan
from .slice_app import validate_seed_data


def smoke_test():
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
