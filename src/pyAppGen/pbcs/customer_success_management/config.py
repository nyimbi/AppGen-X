"""Configuration, rules, and parameters for the customer_success_management PBC."""
from __future__ import annotations

from .domain_depth import DOMAIN_PARAMETERS, DOMAIN_RULES
from .slice_app import ALLOWED_DATABASE_BACKENDS, APPGEN_X_TOPIC, PBC_KEY, build_standalone_app

DOMAIN_PARAMETER_SCHEMA = tuple(
    {"key": key, "scope": "domain", "default": default}
    for key, default in (
        ("churn_risk_threshold", 0.55),
        ("onboarding_sla_days", 30),
        ("health_warning_score", 0.65),
        ("renewal_notice_days", 120),
        ("playbook_task_sla_hours", 48),
        ("workbench_limit", 25),
    )
)
DOMAIN_RULE_SCHEMA = tuple(
    {
        "rule_id": rule_id,
        "scope": "tenant",
        "condition": rule_id,
    }
    for rule_id in DOMAIN_RULES
)


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": ALLOWED_DATABASE_BACKENDS[:-1],
        "event_contract": "AppGen-X",
        "event_topic": APPGEN_X_TOPIC,
        "stream_engine_picker_visible": False,
        "domain_parameter_schema": DOMAIN_PARAMETER_SCHEMA,
        "domain_rule_schema": DOMAIN_RULE_SCHEMA,
        "declared_parameters": DOMAIN_PARAMETERS,
        "side_effects": (),
    }


def parameter_manifest() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "parameters": DOMAIN_PARAMETER_SCHEMA, "side_effects": ()}


def rule_manifest() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "rules": DOMAIN_RULE_SCHEMA, "side_effects": ()}


def validate_configuration(config: dict | None = None) -> dict:
    config = dict(config or {"database_backend": "postgresql", "event_topic": APPGEN_X_TOPIC})
    ok = config.get("database_backend", "postgresql") in ALLOWED_DATABASE_BACKENDS and config.get(
        "event_topic", APPGEN_X_TOPIC
    ) == APPGEN_X_TOPIC
    return {"ok": ok, "config": config, "side_effects": ()}


def set_parameter(state: dict | None, key: str, value) -> dict:
    app = build_standalone_app()
    return app.set_parameter(key, value)


def compile_rule(rule: dict) -> dict:
    if "stream_engine" in str(rule) or "stream_engine_picker" in str(rule):
        return {"ok": False, "compiled": False, "reason": "stream_engine_picker_disallowed", "side_effects": ()}
    app = build_standalone_app()
    result = app.compile_success_rule(rule)
    return {"ok": result["ok"], "compiled": result["ok"], "rule": result["rule"], "side_effects": ()}


def evaluate_rule(compiled: dict, context: dict | None = None) -> dict:
    allowed = compiled.get("ok") is True or compiled.get("status") == "compiled"
    return {
        "ok": allowed,
        "allowed": allowed,
        "scope": compiled.get("scope") or compiled.get("rule", {}).get("payload", {}).get("scope"),
        "context": dict(context or {}),
        "side_effects": (),
    }


def governance_smoke_test() -> dict:
    compiled = compile_rule(DOMAIN_RULE_SCHEMA[0])
    evaluation = evaluate_rule(compiled)
    return {
        "ok": configuration_manifest()["ok"]
        and parameter_manifest()["ok"]
        and rule_manifest()["ok"]
        and evaluation["allowed"],
        "compiled": compiled,
        "evaluation": evaluation,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return governance_smoke_test()
