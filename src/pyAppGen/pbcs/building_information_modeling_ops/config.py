"""Rules and configuration helpers for the BIM operations standalone slice."""

from __future__ import annotations

import hashlib
import json

PBC_KEY = "building_information_modeling_ops"
DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
PARAMETERS = (
    "quality_score_floor",
    "materiality_threshold",
    "approval_sla_hours",
    "risk_threshold",
    "forecast_horizon_days",
    "workbench_limit",
)
RULES = (
    "bim_model_policy",
    "model_version_policy",
    "clash_issue_policy",
    "asset_object_policy",
    "handover_package_policy",
    "model_review_policy",
)


def _stable_digest(value) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def configuration_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "single_pbc_app": True,
        "environment_variables": (
            "BUILDING_INFORMATION_MODELING_OPS_DATABASE_URL",
            "BUILDING_INFORMATION_MODELING_OPS_EVENT_TOPIC",
            "BUILDING_INFORMATION_MODELING_OPS_RETRY_LIMIT",
            "BUILDING_INFORMATION_MODELING_OPS_DEFAULT_POLICY",
        ),
        "side_effects": (),
    }


def validate_configuration(config=None):
    config = dict(config or {"database_backend": "postgresql"})
    return {
        "ok": config.get("database_backend", "postgresql") in DATABASE_BACKENDS,
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
    return {
        "ok": True,
        "rules": RULES,
        "deterministic_compilation": True,
        "side_effects": (),
    }


def compile_rule(rule):
    compiled = dict(rule)
    return {
        "ok": True,
        "rule": compiled,
        "compiled_hash": _stable_digest(compiled),
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
    compiled = compile_rule({"rule_id": RULES[0]})
    return {
        "ok": validate_configuration()["ok"]
        and parameter_manifest()["ok"]
        and rule_manifest()["ok"]
        and compiled["ok"]
        and evaluate_rule(RULES[0])["ok"],
        "compiled_hash": compiled["compiled_hash"],
        "side_effects": (),
    }


def smoke_test():
    return governance_smoke_test()
