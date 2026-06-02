"""Configuration, rules, and parameters for the enterprise_risk_controls PBC."""

from __future__ import annotations

import hashlib

PBC_KEY = "enterprise_risk_controls"
ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
REQUIRED_EVENT_TOPIC = "pbc.enterprise_risk_controls.events"
DOMAIN_PARAMETER_SCHEMA = (
    {"key": "high_risk_threshold", "scope": "risk_appetite", "default": 15, "bounded": True},
    {"key": "appetite_breach_margin", "scope": "risk_appetite", "default": 2, "bounded": True},
    {"key": "kri_staleness_hours", "scope": "indicator_quality", "default": 24, "bounded": True},
    {"key": "attestation_window_days", "scope": "attestation", "default": 14, "bounded": True},
    {"key": "critical_remediation_sla_days", "scope": "remediation", "default": 30, "bounded": True},
    {"key": "evidence_retention_days", "scope": "evidence", "default": 365, "bounded": True},
    {"key": "workbench_limit", "scope": "ui", "default": 50, "bounded": True},
)
DOMAIN_RULE_SCHEMA = (
    {
        "rule_id": "risk_registration_readiness_rule",
        "scope": "risk_intake",
        "condition": "risk_statement_and_owner_required",
    },
    {
        "rule_id": "appetite_breach_gate",
        "scope": "risk_appetite",
        "condition": "residual_score_must_be_within_margin_or_escalated",
    },
    {
        "rule_id": "indicator_quality_rule",
        "scope": "indicator_quality",
        "condition": "observations_must_be_fresh_and_complete",
    },
    {
        "rule_id": "evidence_sufficiency_rule",
        "scope": "evidence",
        "condition": "control_tests_need_traceable_supporting_evidence",
    },
    {
        "rule_id": "assurance_independence_rule",
        "scope": "attestation",
        "condition": "tester_and_attestor_must_be_independent",
    },
    {
        "rule_id": "release_gate_rule",
        "scope": "release_gate",
        "condition": "all_package_sections_and_docs_must_be_present",
    },
)


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": REQUIRED_EVENT_TOPIC,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "required_fields": (
            "database_backend",
            "event_topic",
            "default_appetite_model",
            "default_heatmap_view",
            "default_attestation_window_days",
            "evidence_hash_algorithm",
        ),
        "domain_parameter_schema": DOMAIN_PARAMETER_SCHEMA,
        "domain_rule_schema": DOMAIN_RULE_SCHEMA,
        "side_effects": (),
    }


def parameter_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "parameters": DOMAIN_PARAMETER_SCHEMA,
        "side_effects": (),
    }


def rule_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "rules": DOMAIN_RULE_SCHEMA,
        "side_effects": (),
    }


def validate_configuration(config=None):
    config = {
        "database_backend": "postgresql",
        "event_topic": REQUIRED_EVENT_TOPIC,
        "default_appetite_model": "residual_priority",
        "default_heatmap_view": "appetite_overlay",
        "default_attestation_window_days": 14,
        "evidence_hash_algorithm": "sha256",
        **dict(config or {}),
    }
    required = configuration_manifest()["required_fields"]
    missing = tuple(field for field in required if config.get(field) in {None, ""})
    ok = (
        config.get("database_backend") in ALLOWED_DATABASE_BACKENDS
        and config.get("event_topic") == REQUIRED_EVENT_TOPIC
        and not missing
    )
    return {"ok": ok, "config": config, "missing": missing, "side_effects": ()}


def set_parameter(state, key, value):
    schema = next((item for item in DOMAIN_PARAMETER_SCHEMA if item["key"] == key), None)
    return {
        "ok": schema is not None,
        "parameter": key,
        "value": value,
        "parameter_scope": schema["scope"] if schema else None,
        "bounded": schema.get("bounded", False) if schema else False,
        "side_effects": (),
    }


def compile_rule(rule):
    if "stream_engine" in repr(rule) or "stream_engine_picker" in repr(rule):
        return {
            "ok": False,
            "compiled": False,
            "reason": "stream_engine_picker_disallowed",
            "side_effects": (),
        }
    normalized = dict(rule)
    digest = hashlib.sha256(repr(sorted(normalized.items())).encode("utf-8")).hexdigest()
    return {
        "ok": {"rule_id", "scope", "condition"} <= set(normalized),
        "compiled": {"rule_id", "scope", "condition"} <= set(normalized),
        "rule": normalized,
        "scope": normalized.get("scope"),
        "condition": normalized.get("condition"),
        "compiled_hash": digest,
        "side_effects": (),
    }


def evaluate_rule(compiled, context=None):
    supplied = dict(context or {})
    breached = compiled.get("rule", {}).get("rule_id") == "appetite_breach_gate" and supplied.get("residual_score", 0) > supplied.get("threshold", 999)
    return {
        "ok": compiled.get("ok") is True,
        "allowed": compiled.get("ok") is True and not breached,
        "scope": compiled.get("scope"),
        "decision": "blocked" if breached else "allowed",
        "context": supplied,
        "side_effects": (),
    }


def governance_smoke_test():
    compiled = compile_rule(DOMAIN_RULE_SCHEMA[0])
    validation = validate_configuration()
    return {
        "ok": configuration_manifest()["ok"] and parameter_manifest()["ok"] and rule_manifest()["ok"] and validation["ok"] and evaluate_rule(compiled)["allowed"],
        "validation": validation,
        "side_effects": (),
    }


def smoke_test():
    return governance_smoke_test()
