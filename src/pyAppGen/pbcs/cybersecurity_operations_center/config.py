"""Configuration and policy governance for the cybersecurity_operations_center PBC."""

from __future__ import annotations

from typing import Any

from .models import PARAMETER_BOUNDS, RULE_NAMES, default_policy_bundle

PBC_KEY = "cybersecurity_operations_center"
PARAMETERS = tuple(PARAMETER_BOUNDS)
RULES = RULE_NAMES


def configuration_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "environment_variables": (
            "CYBERSECURITY_OPERATIONS_CENTER_DATABASE_URL",
            "CYBERSECURITY_OPERATIONS_CENTER_EVENT_TOPIC",
            "CYBERSECURITY_OPERATIONS_CENTER_RETRY_LIMIT",
            "CYBERSECURITY_OPERATIONS_CENTER_DEFAULT_POLICY",
        ),
        "side_effects": (),
    }


def validate_configuration(config: dict[str, Any] | None = None) -> dict[str, Any]:
    config = dict(config or {"database_backend": "postgresql", "event_topic": f"pbc.{PBC_KEY}.events"})
    ok = config.get("database_backend") in ("postgresql", "mysql", "mariadb") and config.get("event_topic") == f"pbc.{PBC_KEY}.events"
    return {"ok": ok, "configuration": config, "side_effects": ()}


def parameter_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "parameters": tuple(
            {"name": name, "bounded": True, "minimum": bounds[0], "maximum": bounds[1]}
            for name, bounds in PARAMETER_BOUNDS.items()
        ),
        "defaults": default_policy_bundle(),
        "side_effects": (),
    }


def set_parameter(name: str, value: Any) -> dict[str, Any]:
    if name not in PARAMETER_BOUNDS:
        return {"ok": False, "reason": "unknown_parameter", "name": name, "side_effects": ()}
    minimum, maximum = PARAMETER_BOUNDS[name]
    ok = minimum <= value <= maximum
    return {
        "ok": ok,
        "name": name,
        "value": value,
        "bounded": True,
        "minimum": minimum,
        "maximum": maximum,
        "side_effects": (),
    }


def rule_manifest() -> dict[str, Any]:
    return {"ok": True, "rules": RULES, "default_policy": default_policy_bundle(), "side_effects": ()}


def compile_rule(rule: dict[str, Any]) -> dict[str, Any]:
    rule_name = rule.get("rule_name") or rule.get("rule_id")
    if rule_name not in RULES:
        return {"ok": False, "reason": "unknown_rule", "rule": dict(rule), "side_effects": ()}
    compiled = {
        "rule_name": rule_name,
        "policy": dict(rule.get("policy", {})),
        "compiled_hash": abs(hash(repr(rule))),
        "simulation_preview": {
            "dedup_window_hours": rule.get("policy", {}).get("dedup_window_hours", default_policy_bundle()["dedup_window_hours"]),
            "promotion_cluster_threshold": rule.get("policy", {}).get("promotion_cluster_threshold", default_policy_bundle()["promotion_cluster_threshold"]),
        },
    }
    return {"ok": True, "rule": compiled, "side_effects": ()}


def evaluate_rule(rule: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    if rule not in RULES:
        return {"ok": False, "reason": "unknown_rule", "payload": payload, "side_effects": ()}
    if rule == "containment_action_policy":
        passed = payload.get("approval_path", "no_approval") == "no_approval" or bool(payload.get("approved_by"))
    else:
        passed = True
    return {"ok": True, "passed": passed, "rule": rule, "payload": payload, "side_effects": ()}


def governance_smoke_test() -> dict[str, Any]:
    return {
        "ok": validate_configuration()["ok"]
        and parameter_manifest()["ok"]
        and rule_manifest()["ok"]
        and compile_rule({"rule_name": RULES[0]})["ok"]
        and evaluate_rule("containment_action_policy", {"approval_path": "supervisor_approval", "approved_by": "lead"})["passed"],
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    return governance_smoke_test()
