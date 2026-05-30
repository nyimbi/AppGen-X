"""Package-local seed data for agriculture_farm_operations."""

PBC_KEY = "agriculture_farm_operations"


def seed_plan() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "records": (
            {"table": "agriculture_farm_operations_field", "code": "FIELD-SEED-001"},
            {"table": "agriculture_farm_operations_crop_plan", "code": "PLAN-SEED-001"},
        ),
        "side_effects": (),
    }


def validate_seed_data() -> dict:
    seed = seed_plan()
    invalid = tuple(item for item in seed["records"] if not item["table"].startswith(f"{PBC_KEY}_"))
    return {"ok": not invalid, "pbc": PBC_KEY, "invalid": invalid, "side_effects": ()}


def smoke_test() -> dict:
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
