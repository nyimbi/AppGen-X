"""Configuration, parameter, and rule contracts for gaming_casino_operations."""

from __future__ import annotations

from hashlib import sha256
from typing import Any


PBC_KEY = "gaming_casino_operations"

DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": "pbc.gaming_casino_operations.events",
    "default_policy": "casino_floor_standard",
    "property_id": "property-default",
    "jurisdiction": "NV",
    "default_currency": "USD",
    "retry_limit": 5,
    "workbench_limit": 25,
    "assistant_mutation_confirmation": True,
}

PARAMETER_SPECS = {
    "identity_confidence_floor": {
        "default": 0.9,
        "minimum": 0.5,
        "maximum": 1.0,
        "description": "Minimum confidence before a patron may bypass enrollment review.",
    },
    "duplicate_review_threshold": {
        "default": 0.85,
        "minimum": 0.5,
        "maximum": 1.0,
        "description": "Similarity threshold that forces duplicate patron review.",
    },
    "table_variance_threshold": {
        "default": 100.0,
        "minimum": 0.0,
        "maximum": 5000.0,
        "description": "Maximum allowed bankroll variance when closing a table.",
    },
    "handpay_approval_threshold": {
        "default": 1200.0,
        "minimum": 100.0,
        "maximum": 1000000.0,
        "description": "Threshold above which a payout requires supervisor approval.",
    },
    "suspicious_activity_threshold": {
        "default": 10000.0,
        "minimum": 500.0,
        "maximum": 5000000.0,
        "description": "Threshold above which payouts auto-flag compliance review.",
    },
    "cooling_off_hours": {
        "default": 72,
        "minimum": 1,
        "maximum": 720,
        "description": "Minimum cool-off window for responsible gaming intervention plans.",
    },
    "workbench_limit": {
        "default": 25,
        "minimum": 5,
        "maximum": 250,
        "description": "Maximum items shown per operational queue.",
    },
}

PARAMETERS = tuple(PARAMETER_SPECS)

DEFAULT_RULES = (
    {
        "rule_id": "player_profile_policy",
        "status": "active",
        "scope": "patron_enrollment",
        "requires_age_verification": True,
        "minimum_identity_confidence": PARAMETER_SPECS["identity_confidence_floor"]["default"],
    },
    {
        "rule_id": "table_inventory_policy",
        "status": "active",
        "scope": "table_close",
        "requires_supervisor_signoff": True,
        "maximum_variance": PARAMETER_SPECS["table_variance_threshold"]["default"],
    },
    {
        "rule_id": "slot_machine_policy",
        "status": "active",
        "scope": "slot_recovery",
        "requires_meter_snapshot": True,
        "requires_recovery_approval": True,
    },
    {
        "rule_id": "wager_session_policy",
        "status": "active",
        "scope": "session_open",
        "blocked_restriction_states": (
            "self_excluded",
            "barred",
            "payment_restricted",
            "cooling_off",
        ),
    },
    {
        "rule_id": "payout_approval_policy",
        "status": "active",
        "scope": "payout",
        "approval_threshold": PARAMETER_SPECS["handpay_approval_threshold"]["default"],
        "suspicious_activity_threshold": PARAMETER_SPECS["suspicious_activity_threshold"]["default"],
    },
    {
        "rule_id": "responsible_gaming_policy",
        "status": "active",
        "scope": "responsible_gaming",
        "minimum_cooling_off_hours": PARAMETER_SPECS["cooling_off_hours"]["default"],
    },
    {
        "rule_id": "compliance_case_policy",
        "status": "active",
        "scope": "compliance_case",
        "surveillance_review_required_types": (
            "structuring_indicator",
            "surveillance_review",
            "device_malfunction",
        ),
    },
)
RULES = tuple(rule["rule_id"] for rule in DEFAULT_RULES)


def _parameter_value(parameters: dict[str, Any] | None, name: str) -> Any:
    values = dict(parameters or {})
    if name in values:
        return values[name]
    return PARAMETER_SPECS[name]["default"]


def configuration_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "default_configuration": DEFAULT_CONFIGURATION,
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def validate_configuration(config: dict[str, Any] | None = None) -> dict[str, Any]:
    candidate = {**DEFAULT_CONFIGURATION, **dict(config or {})}
    valid_backend = candidate["database_backend"] in ("postgresql", "mysql", "mariadb")
    valid_topic = candidate["event_topic"] == DEFAULT_CONFIGURATION["event_topic"]
    valid_limit = PARAMETER_SPECS["workbench_limit"]["minimum"] <= candidate["workbench_limit"] <= PARAMETER_SPECS["workbench_limit"]["maximum"]
    return {
        "ok": valid_backend and valid_topic and valid_limit,
        "configuration": candidate,
        "failures": tuple(
            failure
            for failure, failed in (
                ("invalid_backend", not valid_backend),
                ("invalid_event_topic", not valid_topic),
                ("invalid_workbench_limit", not valid_limit),
            )
            if failed
        ),
        "side_effects": (),
    }


def parameter_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "parameters": tuple(
            {
                "name": name,
                "bounded": True,
                "default": spec["default"],
                "minimum": spec["minimum"],
                "maximum": spec["maximum"],
                "description": spec["description"],
            }
            for name, spec in PARAMETER_SPECS.items()
        ),
        "side_effects": (),
    }


def set_parameter(name: str, value: Any) -> dict[str, Any]:
    if name not in PARAMETER_SPECS:
        return {"ok": False, "name": name, "reason": "unknown_parameter", "side_effects": ()}
    spec = PARAMETER_SPECS[name]
    within_bounds = spec["minimum"] <= value <= spec["maximum"]
    return {
        "ok": within_bounds,
        "name": name,
        "value": value,
        "bounded": True,
        "bounds": (spec["minimum"], spec["maximum"]),
        "side_effects": (),
    }


def rule_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "rules": DEFAULT_RULES,
        "side_effects": (),
    }


def compile_rule(rule: dict[str, Any]) -> dict[str, Any]:
    compiled_hash = sha256(repr(sorted(rule.items())).encode("utf-8")).hexdigest()
    return {
        "ok": True,
        "rule": dict(rule),
        "compiled_hash": compiled_hash,
        "side_effects": (),
    }


def evaluate_rule(
    rule: str | dict[str, Any],
    payload: dict[str, Any] | None = None,
    *,
    parameters: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = dict(payload or {})
    params = {name: _parameter_value(parameters, name) for name in PARAMETERS}
    rule_id = rule if isinstance(rule, str) else rule.get("rule_id", "unknown_rule")
    reasons: list[str] = []
    passed = True
    if rule_id == "player_profile_policy":
        if not payload.get("age_verified"):
            passed = False
            reasons.append("age_verification_required")
        if float(payload.get("identity_confidence", 0.0)) < params["identity_confidence_floor"]:
            passed = False
            reasons.append("identity_confidence_below_floor")
    elif rule_id == "table_inventory_policy":
        if payload.get("action") == "close":
            if not payload.get("supervisor_signed"):
                passed = False
                reasons.append("supervisor_signoff_required")
            if not payload.get("reconciliation_complete"):
                passed = False
                reasons.append("reconciliation_required")
            if abs(float(payload.get("variance", 0.0))) > params["table_variance_threshold"]:
                passed = False
                reasons.append("variance_exceeds_threshold")
    elif rule_id == "slot_machine_policy":
        if payload.get("action") in {"recover", "convert"}:
            if not payload.get("has_meter_snapshot"):
                passed = False
                reasons.append("meter_snapshot_required")
            if not payload.get("has_approval"):
                passed = False
                reasons.append("approval_required")
    elif rule_id == "wager_session_policy":
        restricted = payload.get("restriction_state") in {
            "self_excluded",
            "barred",
            "payment_restricted",
            "cooling_off",
        }
        if restricted:
            passed = False
            reasons.append("player_restriction_blocks_session")
        if not payload.get("asset_operational", True):
            passed = False
            reasons.append("asset_not_operational")
    elif rule_id == "payout_approval_policy":
        amount = float(payload.get("amount", 0.0))
        if amount >= params["handpay_approval_threshold"] and not payload.get("has_approval"):
            passed = False
            reasons.append("supervisor_approval_required")
        if amount >= params["suspicious_activity_threshold"]:
            reasons.append("compliance_review_recommended")
    elif rule_id == "responsible_gaming_policy":
        if int(payload.get("cooling_off_hours", 0)) < params["cooling_off_hours"]:
            passed = False
            reasons.append("cooling_off_window_too_short")
    elif rule_id == "compliance_case_policy":
        if payload.get("compliance_type") in {
            "structuring_indicator",
            "surveillance_review",
            "device_malfunction",
        } and not payload.get("surveillance_request"):
            reasons.append("surveillance_review_recommended")
    return {
        "ok": True,
        "passed": passed,
        "rule": rule_id,
        "payload": payload,
        "parameters": params,
        "reasons": tuple(reasons),
        "side_effects": (),
    }


def governance_smoke_test() -> dict[str, Any]:
    config = validate_configuration()
    parameter = set_parameter("handpay_approval_threshold", 2500.0)
    compiled = compile_rule(DEFAULT_RULES[0])
    evaluations = (
        evaluate_rule(
            "player_profile_policy",
            {"age_verified": True, "identity_confidence": 0.98},
        ),
        evaluate_rule(
            "table_inventory_policy",
            {"action": "close", "supervisor_signed": True, "reconciliation_complete": True, "variance": 25.0},
        ),
        evaluate_rule(
            "payout_approval_policy",
            {"amount": 1800.0, "has_approval": True},
        ),
    )
    return {
        "ok": config["ok"]
        and parameter["ok"]
        and compiled["ok"]
        and all(item["ok"] and item["passed"] for item in evaluations),
        "config": config,
        "parameter": parameter,
        "compiled": compiled,
        "evaluations": evaluations,
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    return governance_smoke_test()
