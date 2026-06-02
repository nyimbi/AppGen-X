"""Configuration, rules, and parameters for the insurance_claims_policy PBC."""

from __future__ import annotations

from copy import deepcopy

PBC_KEY = "insurance_claims_policy"
REQUIRED_EVENT_TOPIC = f"pbc.{PBC_KEY}.events"
ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")

DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": REQUIRED_EVENT_TOPIC,
    "retry_limit": 5,
    "default_policy_form": "commercial_property",
    "default_jurisdiction": "US-NAIC",
    "tenant_isolation_mode": "strict",
    "agent_write_requires_confirmation": True,
    "workbench_limit": 100,
}

PARAMETER_SCHEMA = (
    {"key": "reserve_review_threshold", "type": "decimal", "default": 25000.0, "min": 0.0, "max": 1000000.0, "scope": "claims"},
    {"key": "settlement_authority_limit", "type": "decimal", "default": 100000.0, "min": 1000.0, "max": 1000000.0, "scope": "settlement"},
    {"key": "fraud_score_threshold", "type": "decimal", "default": 0.72, "min": 0.0, "max": 1.0, "scope": "fraud"},
    {"key": "premium_grace_days", "type": "integer", "default": 15, "min": 0, "max": 90, "scope": "billing"},
    {"key": "claim_sla_days", "type": "integer", "default": 30, "min": 1, "max": 365, "scope": "operations"},
    {"key": "workbench_limit", "type": "integer", "default": 100, "min": 1, "max": 500, "scope": "platform"},
)

RULE_SCHEMA = (
    {
        "rule_id": "coverage_policy",
        "scope": "coverage",
        "condition": "loss_date_within_policy_period and covered_peril and premium_current",
        "status": "active",
        "explainable": True,
    },
    {
        "rule_id": "reserve_authority_policy",
        "scope": "reserve",
        "condition": "approved_amount <= settlement_authority_limit",
        "status": "active",
        "explainable": True,
    },
    {
        "rule_id": "settlement_approval_policy",
        "scope": "settlement",
        "condition": "offer_amount <= settlement_authority_limit and adjudication_complete",
        "status": "active",
        "explainable": True,
    },
    {
        "rule_id": "fraud_escalation_policy",
        "scope": "fraud",
        "condition": "fraud_score >= fraud_score_threshold",
        "status": "active",
        "explainable": True,
    },
    {
        "rule_id": "premium_grace_policy",
        "scope": "billing",
        "condition": "days_past_due <= premium_grace_days",
        "status": "active",
        "explainable": True,
    },
    {
        "rule_id": "recovery_policy",
        "scope": "subrogation",
        "condition": "liability_third_party and evidence_complete",
        "status": "active",
        "explainable": True,
    },
)

_PARAMETER_INDEX = {item["key"]: item for item in PARAMETER_SCHEMA}
_RULE_INDEX = {item["rule_id"]: item for item in RULE_SCHEMA}


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "required_event_topic": REQUIRED_EVENT_TOPIC,
        "default_configuration": deepcopy(DEFAULT_CONFIGURATION),
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def parameter_manifest() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "parameters": PARAMETER_SCHEMA, "side_effects": ()}


def rule_manifest() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "rules": RULE_SCHEMA, "side_effects": ()}


def parameter_defaults() -> dict:
    return {item["key"]: item["default"] for item in PARAMETER_SCHEMA}


def rule_defaults() -> tuple[dict, ...]:
    return tuple(deepcopy(item) for item in RULE_SCHEMA)


def validate_configuration(config: dict | None = None) -> dict:
    candidate = {**DEFAULT_CONFIGURATION, **dict(config or {})}
    invalid = []
    if candidate["database_backend"] not in ALLOWED_DATABASE_BACKENDS:
        invalid.append("database_backend")
    if candidate.get("event_topic") != REQUIRED_EVENT_TOPIC:
        invalid.append("event_topic")
    if candidate.get("stream_engine_picker_visible"):
        invalid.append("stream_engine_picker_visible")
    return {
        "ok": not invalid,
        "config": candidate,
        "invalid": tuple(invalid),
        "side_effects": (),
    }


def set_parameter(state: dict | None, key: str, value) -> dict:
    schema = _PARAMETER_INDEX.get(key)
    if schema is None:
        schema = {"key": key, "type": "decimal" if isinstance(value, float) else "integer" if isinstance(value, int) else "string", "scope": "custom", "min": None, "max": None}
    if schema["type"] in {"integer", "decimal"} and schema.get("min") is not None and schema.get("max") is not None:
        if value < schema["min"] or value > schema["max"]:
            return {"ok": False, "reason": "parameter_out_of_bounds", "parameter": key, "bounds": (schema["min"], schema["max"]), "side_effects": ()}
    parameters = dict((state or {}).get("parameters", {}))
    parameters[key] = {
        "name": key,
        "value": value,
        "scope": schema["scope"],
        "type": schema["type"],
        "bounded": schema["scope"] != "custom",
    }
    return {"ok": True, "parameter": parameters[key], "parameters": parameters, "side_effects": ()}


def compile_rule(rule: dict) -> dict:
    supplied = dict(rule)
    if "stream_engine" in supplied or "stream_engine_picker" in supplied:
        return {"ok": False, "compiled": False, "reason": "stream_engine_picker_disallowed", "side_effects": ()}
    base = _RULE_INDEX.get(supplied.get("rule_id"), {})
    compiled = {
        **base,
        **supplied,
        "compiled": True,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
    }
    return {"ok": True, "compiled": True, "rule": compiled, "side_effects": ()}


def evaluate_rule(compiled: dict, context: dict | None = None) -> dict:
    context = dict(context or {})
    rule = compiled.get("rule", compiled)
    rule_id = rule.get("rule_id")
    if rule_id == "coverage_policy":
        allowed = bool(context.get("loss_date_within_policy_period", True) and context.get("covered_peril", True) and context.get("premium_current", True))
    elif rule_id == "reserve_authority_policy":
        allowed = float(context.get("approved_amount", 0.0)) <= float(context.get("settlement_authority_limit", parameter_defaults()["settlement_authority_limit"]))
    elif rule_id == "settlement_approval_policy":
        allowed = bool(context.get("adjudication_complete", False)) and float(context.get("offer_amount", 0.0)) <= float(context.get("settlement_authority_limit", parameter_defaults()["settlement_authority_limit"]))
    elif rule_id == "fraud_escalation_policy":
        allowed = float(context.get("fraud_score", 0.0)) < float(context.get("fraud_score_threshold", parameter_defaults()["fraud_score_threshold"]))
    elif rule_id == "premium_grace_policy":
        allowed = int(context.get("days_past_due", 0)) <= int(context.get("premium_grace_days", parameter_defaults()["premium_grace_days"]))
    elif rule_id == "recovery_policy":
        allowed = bool(context.get("liability_third_party", False) and context.get("evidence_complete", False))
    else:
        allowed = compiled.get("ok") is True
    return {
        "ok": compiled.get("ok", True),
        "allowed": allowed,
        "rule_id": rule_id,
        "scope": rule.get("scope"),
        "context": context,
        "side_effects": (),
    }


def governance_smoke_test() -> dict:
    configuration = validate_configuration()
    parameter = set_parameter({}, "reserve_review_threshold", 5000.0)
    compiled = compile_rule({"rule_id": "coverage_policy"})
    evaluation = evaluate_rule(compiled, {"loss_date_within_policy_period": True, "covered_peril": True, "premium_current": True})
    return {
        "ok": configuration["ok"] and parameter["ok"] and compiled["ok"] and evaluation["allowed"],
        "configuration": configuration,
        "parameter": parameter,
        "compiled": compiled,
        "evaluation": evaluation,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return governance_smoke_test()
