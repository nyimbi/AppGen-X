from .standalone import build_seed_plan, seed_state

PBC_KEY = "environment_health_safety"


def seed_plan():
    return build_seed_plan()


def validate_seed_data():
    state = seed_state()
    return {"ok": bool(state["records"]["incidents"]) and bool(state["records"]["hazards"]) and bool(state["records"]["permits"]), "pbc": PBC_KEY, "side_effects": ()}


def smoke_test():
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
