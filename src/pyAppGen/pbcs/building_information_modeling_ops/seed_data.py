PBC_KEY = "building_information_modeling_ops"


def seed_plan():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "records": (
            {
                "table": f"{PBC_KEY}_bim_model",
                "code": "SEED-BIM-MODEL",
                "discipline": "architectural",
            },
            {
                "table": f"{PBC_KEY}_building_information_modeling_ops_policy_rule",
                "code": "SEED-COORDINATE-TOLERANCE",
                "rule_scope": "federation-governance",
            },
        ),
        "side_effects": (),
    }


def validate_seed_data():
    records = seed_plan()["records"]
    invalid = tuple(item for item in records if not item["table"].startswith(f"{PBC_KEY}_"))
    return {"ok": not invalid, "pbc": PBC_KEY, "invalid_records": invalid, "side_effects": ()}


def smoke_test():
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
