PBC_KEY = "hospitality_property_operations"


def seed_plan():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "records": (
            {
                "table": "hospitality_property_operations_room_inventory",
                "payload": {"room_id": "seed_room_101", "tenant": "seed", "room_number": "101", "room_class": "deluxe_king"},
            },
            {
                "table": "hospitality_property_operations_rate_plan",
                "payload": {"rate_plan_id": "seed_bar", "tenant": "seed", "plan_code": "BAR", "room_class": "deluxe_king"},
            },
            {
                "table": "hospitality_property_operations_hospitality_property_operations_runtime_parameter",
                "payload": {"parameter_id": "workbench_limit", "tenant": "seed", "parameter_name": "workbench_limit", "parameter_value": 50},
            },
        ),
        "side_effects": (),
    }


def validate_seed_data():
    seed = seed_plan()
    return {"ok": all(item["table"].startswith(f"{PBC_KEY}_") for item in seed["records"]), "pbc": PBC_KEY, "side_effects": ()}


def smoke_test():
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
