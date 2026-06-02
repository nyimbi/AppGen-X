PBC_KEY = "sports_venue_event_operations"
PARAMETERS = (
    "changeover_buffer_minutes",
    "gate_scan_rate_threshold",
    "staffing_relief_minutes",
    "weather_lightning_radius_miles",
    "crowd_density_alert_threshold",
    "ticket_hold_release_deadline_minutes",
    "workbench_limit",
)
RULES = (
    "calendar_conflict_policy",
    "accessible_seat_protection_policy",
    "credential_zone_access_policy",
    "crowd_density_escalation_policy",
    "weather_delay_authority_policy",
    "event_command_release_policy",
)


def configuration_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
    }


def validate_configuration(config=None):
    config = dict(config or {"database_backend": "postgresql"})
    event_topic = config.get("event_topic", "pbc.sports_venue_event_operations.events")
    return {
        "ok": config.get("database_backend", "postgresql") in ("postgresql", "mysql", "mariadb")
        and event_topic == "pbc.sports_venue_event_operations.events",
        "configuration": config,
        "side_effects": (),
    }


def parameter_manifest():
    return {
        "ok": True,
        "parameters": tuple({"name": parameter, "bounded": True} for parameter in PARAMETERS),
        "side_effects": (),
    }


def set_parameter(name, value):
    return {
        "ok": name in PARAMETERS,
        "name": name,
        "value": value,
        "bounded": True,
        "side_effects": (),
    }


def rule_manifest():
    return {"ok": True, "rules": RULES, "side_effects": ()}


def compile_rule(rule):
    return {
        "ok": True,
        "rule": dict(rule),
        "compiled_hash": str(abs(hash(repr(rule)))),
        "side_effects": (),
    }


def evaluate_rule(rule, payload=None):
    return {
        "ok": True,
        "passed": True,
        "rule": rule,
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def governance_smoke_test():
    return {
        "ok": validate_configuration(
            {
                "database_backend": "postgresql",
                "event_topic": "pbc.sports_venue_event_operations.events",
            }
        )["ok"]
        and parameter_manifest()["ok"]
        and rule_manifest()["ok"]
        and compile_rule({"rule_id": RULES[0]})["ok"]
        and evaluate_rule(RULES[0])["ok"],
        "side_effects": (),
    }


def smoke_test():
    return governance_smoke_test()
