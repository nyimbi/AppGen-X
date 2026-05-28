"""Configuration, rules, and parameter contracts for construction project controls."""
from __future__ import annotations

from .runtime import DEFAULT_CONFIGURATION, DEFAULT_PARAMETERS, DEFAULT_RULES

PBC_KEY = "construction_project_controls"
PARAMETERS = tuple(DEFAULT_PARAMETERS)
RULES = tuple(DEFAULT_RULES)
CONFIGURATION_KEYS = (
    "CONSTRUCTION_PROJECT_CONTROLS_DATABASE_URL",
    "CONSTRUCTION_PROJECT_CONTROLS_EVENT_TOPIC",
    "CONSTRUCTION_PROJECT_CONTROLS_RETRY_LIMIT",
    "CONSTRUCTION_PROJECT_CONTROLS_DEFAULT_POLICY",
)


def configuration_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "configuration_keys": CONFIGURATION_KEYS,
        "defaults": DEFAULT_CONFIGURATION,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
    }


def validate_configuration(config=None):
    config = dict(config or {"database_backend": "postgresql"})
    ok = (
        config.get("database_backend", "postgresql") in ("postgresql", "mysql", "mariadb")
        and config.get("event_topic", DEFAULT_CONFIGURATION["event_topic"])
        == DEFAULT_CONFIGURATION["event_topic"]
    )
    return {"ok": ok, "configuration": config, "side_effects": ()}


def parameter_manifest():
    return {
        "ok": True,
        "parameters": tuple(
            {"name": name, "bounded": True, "default": value}
            for name, value in DEFAULT_PARAMETERS.items()
        ),
        "side_effects": (),
    }


def set_parameter(name, value):
    if name not in DEFAULT_PARAMETERS:
        return {"ok": False, "name": name, "reason": "unknown_parameter", "side_effects": ()}
    if name in ("float_near_critical_days", "float_critical_days", "workbench_limit") and float(value) < 0:
        return {"ok": False, "name": name, "reason": "out_of_range", "side_effects": ()}
    return {"ok": True, "name": name, "value": value, "bounded": True, "side_effects": ()}


def rule_manifest():
    return {"ok": True, "rules": tuple(DEFAULT_RULES.values()), "side_effects": ()}


def compile_rule(rule):
    rule_id = rule.get("rule_id")
    if rule_id not in DEFAULT_RULES:
        return {"ok": False, "reason": "unknown_rule", "rule": dict(rule), "side_effects": ()}
    compiled = {**DEFAULT_RULES[rule_id], **dict(rule), "compiled_hash": str(abs(hash(repr(rule))))}
    return {"ok": True, "rule": compiled, "side_effects": ()}


def evaluate_rule(rule, payload=None):
    payload = dict(payload or {})
    if rule == "progress_evidence_policy":
        passed = bool(payload.get("evidence_bundle"))
    elif rule == "baseline_freeze_policy":
        passed = all(payload.get(field) for field in DEFAULT_RULES[rule]["required_fields"])
    elif rule == "float_threshold_policy":
        passed = float(payload.get("current_float_days", 1)) > float(payload.get("critical_threshold", 0))
    else:
        passed = True
    return {"ok": True, "passed": passed, "rule": rule, "payload": payload, "side_effects": ()}


def governance_smoke_test():
    return {
        "ok": validate_configuration()["ok"]
        and parameter_manifest()["ok"]
        and rule_manifest()["ok"]
        and compile_rule({"rule_id": "baseline_freeze_policy"})["ok"]
        and evaluate_rule(
            "baseline_freeze_policy",
            {"approved_by": "lead", "approved_at": "2026-05-29", "freeze_reason": "Issued for construction"},
        )["passed"],
        "side_effects": (),
    }


def smoke_test():
    return governance_smoke_test()
