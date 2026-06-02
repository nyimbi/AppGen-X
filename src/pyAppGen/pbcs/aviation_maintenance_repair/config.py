"""Configuration, parameters, and rule evaluation for aviation maintenance repair."""
from __future__ import annotations

import hashlib

PBC_KEY = "aviation_maintenance_repair"

PARAMETERS = {
    "quality_score_floor": {"type": "number", "default": 0.95, "min": 0.5, "max": 1.0, "scope": "domain"},
    "materiality_threshold": {"type": "integer", "default": 1, "min": 1, "max": 10, "scope": "domain"},
    "approval_sla_hours": {"type": "integer", "default": 2, "min": 1, "max": 72, "scope": "domain"},
    "risk_threshold": {"type": "number", "default": 0.35, "min": 0.0, "max": 1.0, "scope": "domain"},
    "forecast_horizon_days": {"type": "integer", "default": 30, "min": 1, "max": 180, "scope": "domain"},
    "workbench_limit": {"type": "integer", "default": 25, "min": 5, "max": 200, "scope": "domain"},
}

RULES = {
    "certifier_required_for_release": {
        "rule_id": "certifier_required_for_release",
        "scope": "release",
        "description": "Release requires a certifier with release authorization.",
    },
    "critical_tasks_require_duplicate_inspection": {
        "rule_id": "critical_tasks_require_duplicate_inspection",
        "scope": "work_card",
        "description": "Critical work cards require a duplicate inspection before release.",
    },
    "quarantined_components_block_release": {
        "rule_id": "quarantined_components_block_release",
        "scope": "component",
        "description": "Quarantined or suspect components cannot be installed or released.",
    },
    "expired_deferred_defects_block_release": {
        "rule_id": "expired_deferred_defects_block_release",
        "scope": "defect",
        "description": "Expired deferred defects block release.",
    },
}


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "default_policy": "maintenance_release_governance",
        "side_effects": (),
    }


def validate_configuration(config=None):
    config = dict(config or {"database_backend": "postgresql"})
    backend_ok = config.get("database_backend", "postgresql") in configuration_manifest()["database_backends"]
    event_ok = config.get("event_topic", f"pbc.{PBC_KEY}.events") == f"pbc.{PBC_KEY}.events"
    violations = []
    for name, value in dict(config.get("parameter_overrides") or {}).items():
        result = set_parameter(name, value)
        if not result["ok"]:
            violations.append({"parameter": name, "reason": result["reason"]})
    return {
        "ok": backend_ok and event_ok and not violations,
        "configuration": config,
        "violations": tuple(violations),
        "side_effects": (),
    }


def parameter_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "parameters": tuple({"name": name, **definition} for name, definition in PARAMETERS.items()),
        "side_effects": (),
    }


def set_parameter(name, value):
    definition = PARAMETERS.get(name)
    if not definition:
        return {"ok": False, "name": name, "reason": "unknown_parameter", "side_effects": ()}
    if value < definition["min"] or value > definition["max"]:
        return {"ok": False, "name": name, "value": value, "reason": "out_of_bounds", "bounds": (definition["min"], definition["max"]), "side_effects": ()}
    return {"ok": True, "name": name, "value": value, "bounded": True, "definition": definition, "side_effects": ()}


def rule_manifest():
    return {"ok": True, "pbc": PBC_KEY, "rules": tuple(RULES.values()), "side_effects": ()}


def compile_rule(rule):
    rule_dict = RULES.get(str(rule)) if isinstance(rule, str) else dict(rule)
    if not rule_dict:
        return {"ok": False, "reason": "unknown_rule", "rule": rule, "side_effects": ()}
    return {"ok": True, "rule": rule_dict, "compiled_hash": _digest(rule_dict), "side_effects": ()}


def evaluate_rule(rule, payload=None):
    compiled = compile_rule(rule)
    if not compiled["ok"]:
        return compiled
    payload = dict(payload or {})
    rule_id = compiled["rule"]["rule_id"]
    if rule_id == "certifier_required_for_release":
        passed = bool(dict(payload.get("certifier") or {}).get("release_authorization"))
    elif rule_id == "critical_tasks_require_duplicate_inspection":
        passed = not payload.get("critical_task") or payload.get("duplicate_inspection_required")
    elif rule_id == "quarantined_components_block_release":
        passed = str(payload.get("quarantine_state", "")).lower() not in {"active", "hold", "suspect", "quarantined"}
    elif rule_id == "expired_deferred_defects_block_release":
        passed = not payload.get("expired")
    else:
        passed = True
    return {
        "ok": True,
        "passed": passed,
        "rule": compiled["rule"],
        "payload": payload,
        "side_effects": (),
    }


def governance_smoke_test():
    config = validate_configuration({"database_backend": "postgresql", "event_topic": f"pbc.{PBC_KEY}.events"})
    params = set_parameter("workbench_limit", 50)
    rule = compile_rule("certifier_required_for_release")
    evaluated = evaluate_rule("critical_tasks_require_duplicate_inspection", {"critical_task": True, "duplicate_inspection_required": True})
    return {
        "ok": config["ok"] and params["ok"] and rule["ok"] and evaluated["ok"] and evaluated["passed"],
        "side_effects": (),
    }


def smoke_test():
    return governance_smoke_test()
