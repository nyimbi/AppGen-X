"""Configuration, rules, and bounded parameters for hospitality operations."""

from __future__ import annotations

from .domain_depth import DOMAIN_PARAMETERS, DOMAIN_RULES, assess_room_sellable_state, calculate_overbooking_risk

PBC_KEY = "hospitality_property_operations"
ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
EVENT_TOPIC = "pbc.hospitality_property_operations.events"
PARAMETER_SPECS = {
    "turn_time_minutes": {"minimum": 15, "maximum": 240, "default": 60, "unit": "minutes"},
    "inspection_delay_minutes": {"minimum": 0, "maximum": 120, "default": 20, "unit": "minutes"},
    "arrival_rush_threshold": {"minimum": 1, "maximum": 80, "default": 12, "unit": "arrivals"},
    "same_day_turn_limit": {"minimum": 0, "maximum": 100, "default": 20, "unit": "rooms"},
    "oversell_threshold": {"minimum": 0, "maximum": 10, "default": 2, "unit": "rooms"},
    "late_night_escalation_minutes": {"minimum": 5, "maximum": 180, "default": 30, "unit": "minutes"},
    "workbench_limit": {"minimum": 10, "maximum": 250, "default": 50, "unit": "rows"},
}
RULE_DESCRIPTIONS = {
    "room_sellable_state": "A room cannot be sold while dirty, failed inspection, occupied, or under maintenance hold.",
    "accessible_assignment_guard": "Accessible requests must be matched only to rooms with declared accessibility features.",
    "reservation_guarantee_cutoff": "Arrival-day reservations must be guaranteed before the cutoff to remain in the pickup queue.",
    "overbooking_limit": "Projected arrivals above ready inventory plus threshold trigger exception review.",
    "late_checkout_approval": "Late checkout cannot be approved if the same room has an arrival dependency without supervisor override.",
    "guest_request_sla": "Urgent or recovery requests escalate if the promise time exceeds the configured late-night window.",
}


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "event_topic": EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "required_fields": ("database_backend", "event_topic", "workbench_limit"),
        "side_effects": (),
    }


def validate_configuration(config: dict | None = None) -> dict:
    config = dict(config or {"database_backend": "postgresql", "event_topic": EVENT_TOPIC, "workbench_limit": 50})
    supported = config.get("database_backend") in ALLOWED_DATABASE_BACKENDS
    topic_ok = config.get("event_topic", EVENT_TOPIC) == EVENT_TOPIC
    workbench_limit = int(config.get("workbench_limit", PARAMETER_SPECS["workbench_limit"]["default"]))
    window = PARAMETER_SPECS["workbench_limit"]
    return {
        "ok": supported and topic_ok and window["minimum"] <= workbench_limit <= window["maximum"],
        "configuration": config,
        "side_effects": (),
    }


def parameter_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "parameters": tuple(
            {
                "name": name,
                "minimum": spec["minimum"],
                "maximum": spec["maximum"],
                "default": spec["default"],
                "bounded": True,
                "unit": spec["unit"],
            }
            for name, spec in PARAMETER_SPECS.items()
        ),
        "side_effects": (),
    }


def set_parameter(name: str, value: float | int) -> dict:
    spec = PARAMETER_SPECS.get(name)
    if not spec:
        return {"ok": False, "reason": "unknown_parameter", "name": name, "side_effects": ()}
    numeric = float(value)
    return {
        "ok": spec["minimum"] <= numeric <= spec["maximum"],
        "name": name,
        "value": numeric,
        "bounded": True,
        "side_effects": (),
    }


def rule_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "rules": tuple({"rule_id": rule, "description": RULE_DESCRIPTIONS[rule]} for rule in DOMAIN_RULES),
        "side_effects": (),
    }


def compile_rule(rule: dict) -> dict:
    rule_id = rule.get("rule_id")
    return {
        "ok": rule_id in RULE_DESCRIPTIONS,
        "rule": dict(rule),
        "compiled_hash": f"{PBC_KEY}:{rule_id}",
        "side_effects": (),
    }


def evaluate_rule(rule: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    if rule == "room_sellable_state":
        assessment = assess_room_sellable_state(payload)
        return {"ok": True, "passed": assessment["sellable"], "detail": assessment, "payload": payload, "side_effects": ()}
    if rule == "accessible_assignment_guard":
        required = bool(payload.get("accessible_required"))
        features = payload.get("accessibility_features", ())
        passed = (not required) or bool(features)
        return {"ok": True, "passed": passed, "payload": payload, "side_effects": ()}
    if rule == "reservation_guarantee_cutoff":
        passed = payload.get("guarantee_status", "guaranteed") in {"guaranteed", "deposit_received", "card_on_file"}
        return {"ok": True, "passed": passed, "payload": payload, "side_effects": ()}
    if rule == "overbooking_limit":
        risk = calculate_overbooking_risk(payload)
        threshold = float(payload.get("oversell_threshold", PARAMETER_SPECS["oversell_threshold"]["default"]))
        passed = risk["risk_score"] <= min(threshold / 10.0, 1.0)
        return {"ok": True, "passed": passed, "detail": risk, "payload": payload, "side_effects": ()}
    if rule == "late_checkout_approval":
        passed = not (payload.get("arrival_dependency") and payload.get("late_checkout_until"))
        return {"ok": True, "passed": passed, "payload": payload, "side_effects": ()}
    if rule == "guest_request_sla":
        promised_minutes = int(payload.get("promised_minutes", 0))
        threshold = PARAMETER_SPECS["late_night_escalation_minutes"]["default"]
        passed = promised_minutes <= threshold or payload.get("urgency") == "routine"
        return {"ok": True, "passed": passed, "payload": payload, "side_effects": ()}
    return {"ok": False, "reason": "unknown_rule", "rule": rule, "side_effects": ()}


def governance_smoke_test() -> dict:
    compiled = compile_rule({"rule_id": DOMAIN_RULES[0], "scope": "property"})
    evaluated = evaluate_rule(
        DOMAIN_RULES[0],
        {
            "operational_status": "vacant",
            "housekeeping_status": "clean",
            "inspection_status": "passed",
            "maintenance_status": "clear",
            "sellable_status": "sellable",
        },
    )
    param = set_parameter("workbench_limit", 75)
    return {
        "ok": validate_configuration()["ok"] and parameter_manifest()["ok"] and rule_manifest()["ok"] and compiled["ok"] and evaluated["passed"] and param["ok"],
        "compiled": compiled,
        "evaluated": evaluated,
        "parameter": param,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return governance_smoke_test()
