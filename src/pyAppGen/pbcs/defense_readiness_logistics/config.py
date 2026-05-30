"""Configuration, rules, and parameter helpers for defense_readiness_logistics."""

from __future__ import annotations

from hashlib import sha256

PBC_KEY = "defense_readiness_logistics"
ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
REQUIRED_EVENT_TOPIC = f"pbc.{PBC_KEY}.events"

PARAMETER_SPECS = (
    {"name": "quality_score_floor", "type": "float", "default": 0.8, "minimum": 0.0, "maximum": 1.0},
    {"name": "materiality_threshold", "type": "float", "default": 0.2, "minimum": 0.0, "maximum": 1.0},
    {"name": "approval_sla_hours", "type": "int", "default": 12, "minimum": 1, "maximum": 72},
    {"name": "risk_threshold", "type": "float", "default": 0.35, "minimum": 0.0, "maximum": 1.0},
    {"name": "forecast_horizon_days", "type": "int", "default": 14, "minimum": 1, "maximum": 180},
    {"name": "workbench_limit", "type": "int", "default": 50, "minimum": 10, "maximum": 250},
)
RULE_SPECS = (
    {"name": "unit_readiness_policy", "scope": "readiness"},
    {"name": "mission_asset_policy", "scope": "asset"},
    {"name": "supply_request_policy", "scope": "supply"},
    {"name": "maintenance_status_policy", "scope": "maintenance"},
    {"name": "deployment_plan_policy", "scope": "deployment"},
    {"name": "readiness_inspection_policy", "scope": "inspection"},
)


def _hash(value: object) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "required_event_topic": REQUIRED_EVENT_TOPIC,
        "default_policy": "mission_safe_defaults",
        "assistant_mutations_require_confirmation": True,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def validate_configuration(config: dict | None = None) -> dict:
    config = dict(config or {"database_backend": "postgresql", "event_topic": REQUIRED_EVENT_TOPIC})
    ok = config.get("database_backend") in ALLOWED_DATABASE_BACKENDS and config.get("event_topic", REQUIRED_EVENT_TOPIC) == REQUIRED_EVENT_TOPIC
    return {"ok": ok, "configuration": config, "side_effects": ()}


def parameter_manifest() -> dict:
    return {"ok": True, "parameters": tuple({**spec, "bounded": True} for spec in PARAMETER_SPECS), "side_effects": ()}


def set_parameter(name: str, value) -> dict:
    spec = next((item for item in PARAMETER_SPECS if item["name"] == name), None)
    if not spec:
        return {"ok": False, "reason": "unknown_parameter", "name": name, "side_effects": ()}
    if value < spec["minimum"] or value > spec["maximum"]:
        return {"ok": False, "reason": "out_of_bounds", "name": name, "value": value, "side_effects": ()}
    return {"ok": True, "name": name, "value": value, "bounded": True, "side_effects": ()}


def rule_manifest() -> dict:
    return {"ok": True, "rules": tuple(RULE_SPECS), "side_effects": ()}


def compile_rule(rule: dict) -> dict:
    compiled = {**dict(rule), "compiled_hash": _hash(rule), "event_contract": "AppGen-X"}
    return {"ok": True, "rule": compiled, "side_effects": ()}


def evaluate_rule(rule, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    if isinstance(rule, dict):
        rule_name = rule.get("rule_id") or rule.get("name") or "rule"
    else:
        rule_name = str(rule)
    passed = payload.get("risk_score", 0.0) <= next((spec["default"] for spec in PARAMETER_SPECS if spec["name"] == "risk_threshold"), 0.35)
    return {"ok": True, "passed": passed, "rule": rule_name, "payload": payload, "side_effects": ()}


def governance_smoke_test() -> dict:
    config = validate_configuration()
    parameter = set_parameter("workbench_limit", 50)
    rule = compile_rule({"rule_id": "unit_readiness_policy", "scope": "readiness"})
    evaluation = evaluate_rule(rule["rule"], {"risk_score": 0.2})
    return {
        "ok": config["ok"] and parameter["ok"] and rule["ok"] and evaluation["ok"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    return governance_smoke_test()
