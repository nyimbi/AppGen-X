"""Configuration, parameters, and rules for electronic health records core."""
from __future__ import annotations

from hashlib import sha256

PBC_KEY = "electronic_health_records_core"
PARAMETERS = (
    "quality_score_floor",
    "critical_result_ack_minutes",
    "unsigned_note_sla_hours",
    "duplicate_chart_review_hours",
    "summary_staleness_hours",
    "workbench_limit",
)
RULES = (
    "chart_identity_review_policy",
    "encounter_documentation_policy",
    "clinical_order_safety_policy",
    "critical_result_escalation_policy",
    "care_note_attestation_policy",
    "summary_redaction_policy",
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
    config = dict(
        config
        or {
            "database_backend": "postgresql",
            "event_topic": "pbc.electronic_health_records_core.events",
            "retry_limit": 5,
        }
    )
    ok = config.get("database_backend") in {"postgresql", "mysql", "mariadb"}
    ok = ok and config.get("event_topic", "pbc.electronic_health_records_core.events") == "pbc.electronic_health_records_core.events"
    return {"ok": ok, "configuration": config, "side_effects": ()}


def parameter_manifest() -> dict:
    bounds = {
        "quality_score_floor": (0, 1),
        "critical_result_ack_minutes": (1, 120),
        "unsigned_note_sla_hours": (1, 168),
        "duplicate_chart_review_hours": (1, 168),
        "summary_staleness_hours": (1, 720),
        "workbench_limit": (1, 500),
    }
    return {
        "ok": True,
        "parameters": tuple({"name": name, "bounded": True, "bounds": bounds[name]} for name in PARAMETERS),
        "side_effects": (),
    }


def set_parameter(name: str, value: int | float) -> dict:
    manifest = {item["name"]: item["bounds"] for item in parameter_manifest()["parameters"]}
    if name not in manifest:
        return {"ok": False, "reason": "unknown_parameter", "name": name, "side_effects": ()}
    lower, upper = manifest[name]
    return {
        "ok": lower <= value <= upper,
        "name": name,
        "value": value,
        "bounded": True,
        "bounds": (lower, upper),
        "side_effects": (),
    }


def rule_manifest() -> dict:
    return {"ok": True, "rules": RULES, "side_effects": ()}


def compile_rule(rule: dict) -> dict:
    return {
        "ok": rule.get("rule_id") in RULES or rule.get("rule_id") is not None,
        "rule": dict(rule),
        "compiled_hash": sha256(repr(rule).encode("utf-8")).hexdigest(),
        "side_effects": (),
    }


def evaluate_rule(rule: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    passed = True
    explanation = "rule_passed"
    if rule == "summary_redaction_policy":
        passed = payload.get("requested_profile", "clinical") in {"clinical", "handoff", "patient_portal"}
        explanation = "valid_summary_profile" if passed else "unsupported_summary_profile"
    elif rule == "care_note_attestation_policy":
        passed = bool(payload.get("signer_ref"))
        explanation = "signer_required"
    elif rule == "critical_result_escalation_policy":
        passed = payload.get("acknowledged") is True or payload.get("critical_flag") is False
        explanation = "critical_results_require_acknowledgement"
    return {"ok": True, "passed": passed, "rule": rule, "payload": payload, "explanation": explanation, "side_effects": ()}


def governance_smoke_test() -> dict:
    return {
        "ok": validate_configuration()["ok"]
        and parameter_manifest()["ok"]
        and rule_manifest()["ok"]
        and compile_rule({"rule_id": RULES[0]})["ok"]
        and evaluate_rule("summary_redaction_policy", {"requested_profile": "clinical"})["passed"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    return governance_smoke_test()
