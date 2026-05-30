"""Configuration, parameter, and rule contracts for insurance underwriting."""

from __future__ import annotations

import hashlib
import json


PBC_KEY = "insurance_underwriting"
SUPPORTED_CONFIGURATION_FIELDS = (
    "database_backend",
    "event_topic",
    "workbench_limit",
    "appetite_mode",
    "default_authority_level",
    "assistant_requires_citations",
)
ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
DEFAULT_RUNTIME_PARAMETERS = {
    "quality_score_floor": 0.75,
    "risk_threshold": 0.64,
    "quote_validity_days": 30,
    "auto_bind_limit": 2500000.0,
    "referral_sla_hours": 24,
    "max_override_delta_pct": 0.15,
}
DEFAULT_RULES = (
    {
        "rule_id": "submission_completeness_gate",
        "rule_type": "completeness",
        "description": "Blocks quote generation until critical submission evidence is present.",
        "threshold": DEFAULT_RUNTIME_PARAMETERS["quality_score_floor"],
    },
    {
        "rule_id": "risk_appetite_screening",
        "rule_type": "appetite",
        "description": "Routes high hazard or catastrophe-heavy risks to referral.",
        "threshold": DEFAULT_RUNTIME_PARAMETERS["risk_threshold"],
    },
    {
        "rule_id": "rating_override_control",
        "rule_type": "override",
        "description": "Requires rationale and authority for pricing overrides.",
        "threshold": DEFAULT_RUNTIME_PARAMETERS["max_override_delta_pct"],
    },
    {
        "rule_id": "authority_matrix",
        "rule_type": "authority",
        "description": "Matches requested limit and adverse terms to approval authority.",
        "threshold": DEFAULT_RUNTIME_PARAMETERS["auto_bind_limit"],
    },
    {
        "rule_id": "bind_readiness",
        "rule_type": "bind",
        "description": "Requires subjectivities, exclusions, and payment evidence before bind.",
        "threshold": 1.0,
    },
)


def _stable_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode("utf-8")).hexdigest()


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "supported_fields": SUPPORTED_CONFIGURATION_FIELDS,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "defaults": {
            "database_backend": "postgresql",
            "event_topic": "pbc.insurance_underwriting.events",
            "workbench_limit": 50,
            "appetite_mode": "balanced",
            "default_authority_level": "senior",
            "assistant_requires_citations": True,
        },
        "side_effects": (),
    }


def validate_configuration(config: dict | None = None) -> dict:
    manifest = configuration_manifest()
    supplied = dict(manifest["defaults"])
    supplied.update(dict(config or {}))
    invalid_fields = tuple(
        key for key in supplied if key not in manifest["supported_fields"]
    )
    ok = (
        supplied["database_backend"] in ALLOWED_DATABASE_BACKENDS
        and supplied["event_topic"] == "pbc.insurance_underwriting.events"
        and not invalid_fields
    )
    return {
        "ok": ok,
        "pbc": PBC_KEY,
        "configuration": supplied,
        "invalid_fields": invalid_fields,
        "side_effects": (),
    }


def parameter_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "parameters": tuple(
            {
                "name": name,
                "bounded": True,
                "default": value,
            }
            for name, value in DEFAULT_RUNTIME_PARAMETERS.items()
        ),
        "side_effects": (),
    }


def set_parameter(name: str, value: float | int) -> dict:
    if name not in DEFAULT_RUNTIME_PARAMETERS:
        return {
            "ok": False,
            "reason": "unknown_parameter",
            "name": name,
            "side_effects": (),
        }
    lower, upper = {
        "quality_score_floor": (0.0, 1.0),
        "risk_threshold": (0.0, 1.0),
        "quote_validity_days": (1, 365),
        "auto_bind_limit": (1000.0, 100000000.0),
        "referral_sla_hours": (1, 168),
        "max_override_delta_pct": (0.0, 1.0),
    }[name]
    ok = lower <= float(value) <= upper
    return {
        "ok": ok,
        "name": name,
        "value": value,
        "bounds": (lower, upper),
        "side_effects": (),
    }


def rule_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "rules": DEFAULT_RULES,
        "side_effects": (),
    }


def compile_rule(rule: dict) -> dict:
    required = ("rule_id", "rule_type", "description")
    if any(not rule.get(field) for field in required):
        return {
            "ok": False,
            "reason": "missing_required_rule_field",
            "required_fields": required,
            "rule": dict(rule),
            "side_effects": (),
        }
    compiled = {
        **dict(rule),
        "compiled_hash": _stable_hash(rule),
        "compiled_evidence": {
            "event_contract": "AppGen-X",
            "shared_table_access": False,
        },
    }
    return {"ok": True, "rule": compiled, "side_effects": ()}


def evaluate_rule(rule: str | dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    rule_id = rule["rule_id"] if isinstance(rule, dict) else str(rule)
    if rule_id == "submission_completeness_gate":
        score = float(payload.get("completeness_score", 0.0))
        passed = score >= DEFAULT_RUNTIME_PARAMETERS["quality_score_floor"]
        outcome = "pass" if passed else "block"
    elif rule_id == "risk_appetite_screening":
        score = float(payload.get("hazard_score", 0.0))
        passed = score < DEFAULT_RUNTIME_PARAMETERS["risk_threshold"]
        outcome = "accept" if passed else "refer"
    elif rule_id == "rating_override_control":
        delta = abs(float(payload.get("override_delta_pct", 0.0)))
        passed = delta <= DEFAULT_RUNTIME_PARAMETERS["max_override_delta_pct"]
        outcome = "pass" if passed else "refer"
    elif rule_id == "authority_matrix":
        limit = float(payload.get("requested_limit", 0.0))
        passed = limit <= DEFAULT_RUNTIME_PARAMETERS["auto_bind_limit"]
        outcome = "approve" if passed else "refer"
    elif rule_id == "bind_readiness":
        passed = not bool(payload.get("missing_items"))
        outcome = "bind" if passed else "block"
    else:
        passed = True
        outcome = "inform"
    return {
        "ok": True,
        "rule_id": rule_id,
        "passed": passed,
        "outcome": outcome,
        "payload": payload,
        "side_effects": (),
    }


def governance_smoke_test() -> dict:
    manifest = configuration_manifest()
    validation = validate_configuration()
    parameters = parameter_manifest()
    rules = rule_manifest()
    compiled = compile_rule(DEFAULT_RULES[0])
    evaluated = evaluate_rule("submission_completeness_gate", {"completeness_score": 0.8})
    return {
        "ok": (
            manifest["ok"]
            and validation["ok"]
            and parameters["ok"]
            and rules["ok"]
            and compiled["ok"]
            and evaluated["passed"]
        ),
        "manifest": manifest,
        "validation": validation,
        "parameters": parameters,
        "rules": rules,
        "compiled": compiled,
        "evaluated": evaluated,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return governance_smoke_test()
