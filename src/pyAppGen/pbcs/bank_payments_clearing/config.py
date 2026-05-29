"""Configuration, parameter, and rule contracts for bank_payments_clearing."""

from __future__ import annotations

import hashlib
import json

from .runtime import (
    BANK_PAYMENTS_CLEARING_ALLOWED_DATABASE_BACKENDS,
    BANK_PAYMENTS_CLEARING_REQUIRED_EVENT_TOPIC,
)


PBC_KEY = "bank_payments_clearing"
PARAMETERS = (
    "quality_score_floor",
    "materiality_threshold",
    "approval_sla_hours",
    "risk_threshold",
    "forecast_horizon_days",
    "workbench_limit",
    "duplicate_similarity_threshold",
    "liquidity_buffer_amount",
)
RULES = (
    "payment_instruction_policy",
    "clearing_batch_policy",
    "settlement_file_policy",
    "return_item_policy",
    "exception_case_policy",
    "bank_reconciliation_policy",
    "maker_checker_policy",
)
_PARAMETER_DEFAULTS = {
    "quality_score_floor": 0.7,
    "materiality_threshold": 1000.0,
    "approval_sla_hours": 4,
    "risk_threshold": 0.85,
    "forecast_horizon_days": 3,
    "workbench_limit": 100,
    "duplicate_similarity_threshold": 0.95,
    "liquidity_buffer_amount": 250.0,
}


def _digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": BANK_PAYMENTS_CLEARING_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "event_topic": BANK_PAYMENTS_CLEARING_REQUIRED_EVENT_TOPIC,
        "default_configuration": {
            "database_backend": "postgresql",
            "event_topic": BANK_PAYMENTS_CLEARING_REQUIRED_EVENT_TOPIC,
            "retry_limit": 5,
            "default_policy": "balanced",
            "agent_confirmation_required": True,
            "stream_engine_picker_visible": False,
        },
        "side_effects": (),
    }


def validate_configuration(config: dict | None = None) -> dict:
    config = {
        **configuration_manifest()["default_configuration"],
        **dict(config or {}),
    }
    invalid = []
    if config["database_backend"] not in BANK_PAYMENTS_CLEARING_ALLOWED_DATABASE_BACKENDS:
        invalid.append("unsupported_database_backend")
    if config["event_topic"] != BANK_PAYMENTS_CLEARING_REQUIRED_EVENT_TOPIC:
        invalid.append("invalid_event_topic")
    if config.get("stream_engine_picker_visible") is not False:
        invalid.append("stream_engine_picker_must_be_hidden")
    return {
        "ok": not invalid,
        "configuration": config,
        "invalid": tuple(invalid),
        "side_effects": (),
    }


def parameter_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "parameters": tuple(
            {
                "name": name,
                "default": _PARAMETER_DEFAULTS[name],
                "bounded": True,
            }
            for name in PARAMETERS
        ),
        "side_effects": (),
    }


def set_parameter(name: str, value) -> dict:
    return {
        "ok": name in PARAMETERS,
        "name": name,
        "value": value,
        "bounded": name in PARAMETERS,
        "side_effects": (),
    }


def rule_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "rules": tuple(
            {
                "rule_id": rule,
                "scope": "bank_payments_clearing",
                "event_contract": "AppGen-X",
            }
            for rule in RULES
        ),
        "side_effects": (),
    }


def compile_rule(rule: dict) -> dict:
    return {
        "ok": rule.get("rule_id") in RULES,
        "rule": dict(rule),
        "compiled_hash": _digest(rule),
        "side_effects": (),
    }


def evaluate_rule(rule: str | dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    rule_id = rule["rule_id"] if isinstance(rule, dict) else str(rule)
    passed = True
    if rule_id == "maker_checker_policy":
        passed = payload.get("maker") != payload.get("checker")
    if rule_id == "payment_instruction_policy":
        passed = float(payload.get("amount", 1.0)) > 0
    return {
        "ok": rule_id in RULES,
        "passed": passed,
        "rule": rule_id,
        "payload": payload,
        "side_effects": (),
    }


def governance_smoke_test() -> dict:
    config_ok = validate_configuration()["ok"]
    parameter_ok = set_parameter("workbench_limit", 50)["ok"]
    compiled = compile_rule({"rule_id": "maker_checker_policy", "scope": "release"})
    evaluated = evaluate_rule(
        "maker_checker_policy",
        {"maker": "maker", "checker": "checker"},
    )
    return {
        "ok": config_ok and parameter_ok and compiled["ok"] and evaluated["ok"] and evaluated["passed"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    return governance_smoke_test()
