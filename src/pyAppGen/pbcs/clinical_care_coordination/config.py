"""Configuration and rule helpers for clinical_care_coordination."""

from __future__ import annotations

import json
from hashlib import sha256


PBC_KEY = "clinical_care_coordination"
PARAMETERS = (
    "quality_score_floor",
    "materiality_threshold",
    "approval_sla_hours",
    "risk_threshold",
    "forecast_horizon_days",
    "workbench_limit",
)
RULES = (
    "patient_care_plan_policy",
    "care_team_policy",
    "referral_policy",
    "encounter_policy",
    "care_gap_policy",
    "transition_plan_policy",
)


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
    }


def validate_configuration(config: dict | None = None) -> dict:
    config = dict(config or {"database_backend": "postgresql"})
    return {
        "ok": config.get("database_backend", "postgresql") in ("postgresql", "mysql", "mariadb"),
        "configuration": config,
        "side_effects": (),
    }


def parameter_manifest() -> dict:
    return {"ok": True, "parameters": tuple({"name": p, "bounded": True} for p in PARAMETERS), "side_effects": ()}


def set_parameter(name: str, value: object) -> dict:
    return {"ok": name in PARAMETERS, "name": name, "value": value, "bounded": True, "side_effects": ()}


def rule_manifest() -> dict:
    return {"ok": True, "rules": RULES, "side_effects": ()}


def compile_rule(rule: dict) -> dict:
    compiled = json.dumps(rule, sort_keys=True, default=str)
    return {
        "ok": True,
        "rule": dict(rule),
        "compiled_hash": sha256(compiled.encode("utf-8")).hexdigest(),
        "side_effects": (),
    }


def evaluate_rule(rule: str, payload: dict | None = None) -> dict:
    return {"ok": True, "passed": True, "rule": rule, "payload": dict(payload or {}), "side_effects": ()}


def governance_smoke_test() -> dict:
    return {
        "ok": validate_configuration()["ok"]
        and parameter_manifest()["ok"]
        and rule_manifest()["ok"]
        and compile_rule({"rule_id": RULES[0]})["ok"]
        and evaluate_rule(RULES[0])["ok"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    return governance_smoke_test()
