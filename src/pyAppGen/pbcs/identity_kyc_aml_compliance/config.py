"""Configuration, rule, and parameter contracts for the identity KYC / AML slice."""

from __future__ import annotations

from .domain_depth import DOMAIN_PARAMETERS, DOMAIN_RULES
from .runtime import (
    DEFAULT_PARAMETER_VALUES,
    DEFAULT_RULES,
    IDENTITY_KYC_AML_COMPLIANCE_ALLOWED_DATABASE_BACKENDS,
    IDENTITY_KYC_AML_COMPLIANCE_REQUIRED_EVENT_TOPIC,
    _digest,
)

PBC_KEY = "identity_kyc_aml_compliance"
PARAMETERS = DOMAIN_PARAMETERS
RULES = DOMAIN_RULES


def configuration_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": IDENTITY_KYC_AML_COMPLIANCE_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "required_event_topic": IDENTITY_KYC_AML_COMPLIANCE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def validate_configuration(config=None):
    config = dict(config or {"database_backend": "postgresql", "event_topic": IDENTITY_KYC_AML_COMPLIANCE_REQUIRED_EVENT_TOPIC})
    return {
        "ok": config.get("database_backend", "postgresql") in IDENTITY_KYC_AML_COMPLIANCE_ALLOWED_DATABASE_BACKENDS and config.get("event_topic", IDENTITY_KYC_AML_COMPLIANCE_REQUIRED_EVENT_TOPIC) == IDENTITY_KYC_AML_COMPLIANCE_REQUIRED_EVENT_TOPIC,
        "configuration": config,
        "side_effects": (),
    }


def parameter_manifest():
    return {
        "ok": True,
        "parameters": tuple(
            {
                "name": name,
                "bounded": True,
                "default": DEFAULT_PARAMETER_VALUES[name],
            }
            for name in PARAMETERS
        ),
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
    return {"ok": True, "rules": tuple(DEFAULT_RULES.values()), "side_effects": ()}


def compile_rule(rule):
    materialized = dict(rule)
    materialized["compiled_hash"] = _digest(rule)
    return {"ok": bool(materialized.get("rule_id") or materialized.get("rule_name")), "rule": materialized, "compiled_hash": materialized["compiled_hash"], "side_effects": ()}


def evaluate_rule(rule, payload=None):
    payload = dict(payload or {})
    name = rule if isinstance(rule, str) else rule.get("rule_id") or rule.get("rule_name")
    if name == "customer_classification_required":
        passed = all(payload.get(field) for field in ("customer_type", "jurisdiction", "product_exposure", "channel", "expected_activity"))
    elif name == "document_completeness_required":
        passed = all(payload.get(field) for field in ("document_class", "jurisdiction", "issuing_authority", "identifier", "issue_date", "expiry_date", "capture_method"))
    elif name == "risk_score_challenge_policy":
        passed = bool(payload.get("challenge_note") and payload.get("supervisor"))
    else:
        passed = True
    return {"ok": True, "passed": passed, "rule": name, "payload": payload, "side_effects": ()}


def governance_smoke_test():
    return {
        "ok": validate_configuration()["ok"]
        and parameter_manifest()["ok"]
        and rule_manifest()["ok"]
        and compile_rule({"rule_id": RULES[0]})["ok"]
        and evaluate_rule(RULES[0], {"customer_type": "individual", "jurisdiction": "KE", "product_exposure": "checking", "channel": "remote", "expected_activity": "salary"})["passed"],
        "side_effects": (),
    }


def smoke_test():
    return governance_smoke_test()
