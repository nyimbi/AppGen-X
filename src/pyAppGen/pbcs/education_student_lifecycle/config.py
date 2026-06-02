"""Configuration, rules, and parameter controls for education_student_lifecycle."""

from __future__ import annotations

PBC_KEY = "education_student_lifecycle"
PARAMETER_DEFINITIONS = {
    "workbench_limit": {"min": 10, "max": 500, "default": 50},
    "risk_threshold": {"min": 0.0, "max": 1.0, "default": 0.75},
    "minimum_document_confidence": {"min": 0.0, "max": 1.0, "default": 0.8},
    "maximum_leave_terms": {"min": 0, "max": 6, "default": 2},
    "petition_sla_hours": {"min": 4, "max": 240, "default": 72},
    "graduation_credit_margin": {"min": 0, "max": 12, "default": 0},
}
RULES = (
    "applicant_admissions_policy",
    "enrollment_progression_policy",
    "curriculum_audit_policy",
    "course_registration_policy",
    "risk_intervention_policy",
    "credential_award_policy",
)


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "parameters": PARAMETER_DEFINITIONS,
        "rules": RULES,
    }


def validate_configuration(config=None) -> dict:
    config = dict(config or {"database_backend": "postgresql", "event_topic": "pbc.education_student_lifecycle.events"})
    ok = config.get("database_backend", "postgresql") in ("postgresql", "mysql", "mariadb")
    ok = ok and config.get("event_topic", "pbc.education_student_lifecycle.events") == "pbc.education_student_lifecycle.events"
    return {"ok": ok, "configuration": config, "side_effects": ()}


def parameter_manifest() -> dict:
    return {
        "ok": True,
        "parameters": tuple(
            {
                "name": name,
                "bounded": True,
                "minimum": definition["min"],
                "maximum": definition["max"],
                "default": definition["default"],
            }
            for name, definition in PARAMETER_DEFINITIONS.items()
        ),
        "side_effects": (),
    }


def set_parameter(name, value):
    definition = PARAMETER_DEFINITIONS.get(name)
    if definition is None:
        return {"ok": False, "reason": "unknown_parameter", "name": name, "side_effects": ()}
    numeric_value = float(value) if isinstance(value, (int, float)) else value
    bounded = isinstance(numeric_value, (int, float, float))
    ok = True
    if isinstance(numeric_value, (int, float)):
        ok = definition["min"] <= numeric_value <= definition["max"]
    return {"ok": ok, "name": name, "value": value, "bounded": bounded, "side_effects": ()}


def rule_manifest() -> dict:
    return {"ok": True, "rules": RULES, "side_effects": ()}


def compile_rule(rule):
    rule_id = rule.get("rule_id") if isinstance(rule, dict) else rule
    return {"ok": rule_id in RULES, "rule": dict(rule) if isinstance(rule, dict) else {"rule_id": rule_id}, "compiled_hash": str(abs(hash(repr(rule)))), "side_effects": ()}


def evaluate_rule(rule, payload=None):
    payload = dict(payload or {})
    rule_id = rule.get("rule_id") if isinstance(rule, dict) else rule
    if rule_id == "applicant_admissions_policy":
        passed = not payload.get("missing_documents") and payload.get("application_stage") not in {"offered", "accepted"}
    elif rule_id == "enrollment_progression_policy":
        passed = payload.get("status") in {"matriculated", "active", "probation", None} and not payload.get("blocking_hold")
    elif rule_id == "curriculum_audit_policy":
        passed = float(payload.get("remaining_credits", 0.0)) <= float(payload.get("credit_margin", 0.0)) and not payload.get("unmet_competencies")
    elif rule_id == "course_registration_policy":
        passed = payload.get("prerequisites_satisfied", False) or payload.get("override_approved", False)
    elif rule_id == "risk_intervention_policy":
        passed = float(payload.get("risk_score", 0.0)) < PARAMETER_DEFINITIONS["risk_threshold"]["default"] or payload.get("reviewer_confirmed", False)
    elif rule_id == "credential_award_policy":
        passed = payload.get("audit_complete", False) and not payload.get("blocking_holds", False)
    else:
        passed = False
    return {"ok": rule_id in RULES, "passed": passed, "rule": rule_id, "payload": payload, "side_effects": ()}


def governance_smoke_test():
    return {
        "ok": validate_configuration()["ok"]
        and parameter_manifest()["ok"]
        and rule_manifest()["ok"]
        and compile_rule({"rule_id": RULES[0]})["ok"]
        and evaluate_rule("course_registration_policy", {"prerequisites_satisfied": True})["passed"]
        and evaluate_rule("risk_intervention_policy", {"risk_score": 0.8, "reviewer_confirmed": True})["passed"],
        "side_effects": (),
    }


def smoke_test():
    return governance_smoke_test()
