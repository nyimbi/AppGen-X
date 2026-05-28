PBC_KEY = "capital_projects_delivery"


def seed_plan():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "records": (
            {
                "table": "capital_projects_delivery_capital_project",
                "code": "SEED-CAPITAL-PROJECT",
                "name": "Seed Capital Project",
                "lifecycle_stage": "idea",
            },
        ),
        "side_effects": (),
    }


def validate_seed_data():
    plan = seed_plan()
    return {
        "ok": plan["ok"] and all(record["table"].startswith(f"{PBC_KEY}_") for record in plan["records"]),
        "pbc": PBC_KEY,
        "side_effects": (),
    }


def smoke_test():
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
