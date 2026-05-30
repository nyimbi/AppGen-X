from .operations_engine import seed_records

PBC_KEY = "water_wastewater_operations"


def seed_plan():
    return {"ok": True, "pbc": PBC_KEY, "records": seed_records(), "side_effects": ()}


def validate_seed_data():
    records = seed_plan()["records"]
    invalid = tuple(record for record in records if not record["table"].startswith(f"{PBC_KEY}_"))
    return {"ok": not invalid, "pbc": PBC_KEY, "invalid_records": invalid, "side_effects": ()}


def smoke_test():
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
