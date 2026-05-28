"""Runtime configuration, RBAC, parameters, and rule evaluation for claims adjudication."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from .models import PBC_KEY

ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
REQUIRED_EVENT_TOPIC = f"pbc.{PBC_KEY}.events"

PERMISSIONS = (
    f"{PBC_KEY}.read",
    f"{PBC_KEY}.create",
    f"{PBC_KEY}.update",
    f"{PBC_KEY}.approve",
    f"{PBC_KEY}.admin",
)

ROLES = {
    "claims_intake_specialist": (f"{PBC_KEY}.read", f"{PBC_KEY}.create"),
    "clinical_coder": (f"{PBC_KEY}.read", f"{PBC_KEY}.update"),
    "medical_director": (f"{PBC_KEY}.read", f"{PBC_KEY}.approve"),
    "appeals_nurse": (f"{PBC_KEY}.read", f"{PBC_KEY}.update", f"{PBC_KEY}.approve"),
    "payment_integrity_analyst": (f"{PBC_KEY}.read", f"{PBC_KEY}.update"),
    "auditor": (f"{PBC_KEY}.read",),
    "platform_admin": PERMISSIONS,
}

PARAMETER_DEFINITIONS = {
    "workbench_limit": {"default": 25, "minimum": 5, "maximum": 200, "unit": "rows"},
    "stale_projection_hours": {"default": 24, "minimum": 1, "maximum": 168, "unit": "hours"},
    "coding_review_unit_threshold": {"default": 8, "minimum": 1, "maximum": 50, "unit": "units"},
    "duplicate_claim_score_threshold": {"default": 0.92, "minimum": 0.5, "maximum": 1.0, "unit": "ratio"},
    "payment_integrity_materiality": {"default": 2500, "minimum": 100, "maximum": 100000, "unit": "usd"},
    "max_auto_approve_amount": {"default": 4000, "minimum": 100, "maximum": 100000, "unit": "usd"},
}

RULE_LIBRARY = (
    {
        "rule_name": "stale_projection_guard",
        "description": "Pend claims when eligibility or provider projections are stale.",
        "condition_key": "projection_hours",
        "threshold": 24,
        "action": "pend",
    },
    {
        "rule_name": "high_units_coding_review",
        "description": "Open coding review when service units exceed a safe auto-adjudication threshold.",
        "condition_key": "line_units",
        "threshold": 8,
        "action": "open_coding_review",
    },
    {
        "rule_name": "material_payment_integrity_review",
        "description": "Open payment integrity review when total exposure exceeds the materiality threshold.",
        "condition_key": "charge_amount",
        "threshold": 2500,
        "action": "open_payment_integrity_case",
    },
)

DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "database_url_env": "CLAIMS_ADJUDICATION_HEALTHCARE_DATABASE_URL",
    "event_topic": REQUIRED_EVENT_TOPIC,
    "retry_limit": 5,
    "default_policy": "commercial-default",
    "tenant_isolation": "strict",
    "agent_write_confirmation": True,
}

PARAMETERS = tuple(PARAMETER_DEFINITIONS.keys())
RULES = tuple(item["rule_name"] for item in RULE_LIBRARY)


def configuration_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "default_configuration": deepcopy(DEFAULT_CONFIGURATION),
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def validate_configuration(config: dict[str, Any] | None = None) -> dict[str, Any]:
    merged = deepcopy(DEFAULT_CONFIGURATION)
    merged.update(config or {})
    invalid_fields: list[str] = []
    if merged["database_backend"] not in ALLOWED_DATABASE_BACKENDS:
        invalid_fields.append("database_backend")
    if merged["event_topic"] != REQUIRED_EVENT_TOPIC:
        invalid_fields.append("event_topic")
    if merged.get("retry_limit", 0) < 1:
        invalid_fields.append("retry_limit")
    return {
        "ok": not invalid_fields,
        "pbc": PBC_KEY,
        "configuration": merged,
        "invalid_fields": tuple(invalid_fields),
        "side_effects": (),
    }


def parameter_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "parameters": tuple(
            {"name": name, **definition, "bounded": True}
            for name, definition in PARAMETER_DEFINITIONS.items()
        ),
        "side_effects": (),
    }


def set_parameter(name: str, value: float) -> dict[str, Any]:
    definition = PARAMETER_DEFINITIONS.get(name)
    if definition is None:
        return {
            "ok": False,
            "reason": "unknown_parameter",
            "name": name,
            "side_effects": (),
        }
    bounded = definition["minimum"] <= value <= definition["maximum"]
    return {
        "ok": bounded,
        "name": name,
        "value": value,
        "minimum": definition["minimum"],
        "maximum": definition["maximum"],
        "bounded": True,
        "side_effects": (),
    }


def rule_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "rules": deepcopy(RULE_LIBRARY),
        "side_effects": (),
    }


def compile_rule(rule: dict[str, Any]) -> dict[str, Any]:
    required = ("rule_name", "condition_key", "threshold", "action")
    missing = tuple(field for field in required if field not in rule)
    return {
        "ok": not missing,
        "pbc": PBC_KEY,
        "rule": deepcopy(rule),
        "missing": missing,
        "compiled_hash": abs(hash(tuple(sorted(rule.items())))),
        "side_effects": (),
    }


def evaluate_rule(rule: dict[str, Any], payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    compiled = compile_rule(rule)
    if not compiled["ok"]:
        return {**compiled, "passed": False}
    actual_value = float(payload.get(rule["condition_key"], 0))
    passed = actual_value <= float(rule["threshold"])
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "rule": deepcopy(rule),
        "payload": payload,
        "actual_value": actual_value,
        "passed": passed,
        "recommended_action": None if passed else rule["action"],
        "side_effects": (),
    }


def permission_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": tuple({"role": role, "permissions": permissions} for role, permissions in ROLES.items()),
        "side_effects": (),
    }


def authorize(permission: str, actor: dict[str, Any] | None = None) -> dict[str, Any]:
    if permission == f"{PBC_KEY}.operate":
        permission = f"{PBC_KEY}.update"
    if permission not in PERMISSIONS:
        return {
            "ok": False,
            "permission": permission,
            "reason": "unknown_permission",
            "side_effects": (),
        }
    if not actor:
        return {"ok": True, "permission": permission, "actor": {}, "side_effects": ()}
    actor_roles = tuple(actor.get("roles", (actor.get("role"),)))
    granted = any(permission in ROLES.get(role, ()) for role in actor_roles if role)
    return {
        "ok": granted,
        "permission": permission,
        "actor": dict(actor),
        "granted_by_roles": tuple(role for role in actor_roles if role in ROLES),
        "side_effects": (),
    }


def governance_smoke_test() -> dict[str, Any]:
    config_ok = validate_configuration()["ok"]
    parameter_ok = all(set_parameter(name, definition["default"])["ok"] for name, definition in PARAMETER_DEFINITIONS.items())
    rules_ok = all(compile_rule(rule)["ok"] for rule in RULE_LIBRARY)
    evaluation_ok = evaluate_rule(RULE_LIBRARY[0], {"projection_hours": 12})["passed"] is True
    permission_ok = authorize(PERMISSIONS[0], {"role": "platform_admin"})["ok"] is True
    return {
        "ok": config_ok and parameter_ok and rules_ok and evaluation_ok and permission_ok,
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    return governance_smoke_test()
