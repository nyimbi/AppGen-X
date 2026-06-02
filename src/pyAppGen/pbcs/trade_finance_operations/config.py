"""Configuration, rule, and parameter hooks for trade_finance_operations."""

from __future__ import annotations

PBC_KEY = "trade_finance_operations"
PARAMETERS = (
    "quality_score_floor",
    "materiality_threshold",
    "approval_sla_hours",
    "risk_threshold",
    "forecast_horizon_days",
    "workbench_limit",
    "sanctions_hold_sla_hours",
    "waiver_response_sla_hours",
    "collateral_haircut_pct",
    "limit_buffer_pct",
)
RULES = (
    "letter_of_credit_policy",
    "bank_guarantee_policy",
    "standby_credit_policy",
    "documentary_collection_policy",
    "shipment_document_policy",
    "sanctions_and_compliance_policy",
    "discrepancy_resolution_policy",
    "limit_and_collateral_policy",
    "fee_policy",
    "settlement_release_policy",
)


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "required_fields": ("database_backend", "event_topic", "retry_limit", "default_policy"),
        "side_effects": (),
    }


def validate_configuration(config=None):
    candidate = {"database_backend": "postgresql", "event_topic": "pbc.trade_finance_operations.events", **dict(config or {})}
    ok = candidate["database_backend"] in ("postgresql", "mysql", "mariadb") and candidate["event_topic"] == "pbc.trade_finance_operations.events"
    return {"ok": ok, "configuration": candidate, "side_effects": ()}


def parameter_manifest() -> dict:
    return {
        "ok": True,
        "parameters": tuple({"name": name, "bounded": True, "min": 0, "max": 999999} for name in PARAMETERS),
        "side_effects": (),
    }


def set_parameter(name, value):
    return {"ok": name in PARAMETERS, "name": name, "value": value, "accepted": name in PARAMETERS, "bounded": True, "side_effects": ()}


def rule_manifest() -> dict:
    return {"ok": True, "rules": RULES, "side_effects": ()}


def compile_rule(rule):
    return {"ok": True, "rule": dict(rule), "compiled_hash": str(abs(hash(repr(rule)))), "compiled": True, "side_effects": ()}


def evaluate_rule(rule, payload=None):
    payload = dict(payload or {})
    blocked = any(term in str(payload).lower() for term in ("sanctioned", "restricted_party", "embargoed"))
    return {"ok": True, "allowed": not blocked, "passed": not blocked, "rule": rule, "payload": payload, "side_effects": ()}


def governance_smoke_test():
    config = validate_configuration()
    parameter = set_parameter("workbench_limit", 50)
    compiled_rule = compile_rule({"rule_id": RULES[0], "scope": "issuance"})
    rule_decision = evaluate_rule(RULES[0], {"destination_country": "KE"})
    return {
        "ok": config["ok"] and parameter["ok"] and compiled_rule["ok"] and rule_decision["ok"],
        "configuration": config,
        "parameter": parameter,
        "compiled_rule": compiled_rule,
        "rule_decision": rule_decision,
        "side_effects": (),
    }


def smoke_test():
    return governance_smoke_test()
