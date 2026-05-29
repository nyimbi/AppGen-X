"""Configuration and rule helpers for the advertising campaign standalone slice."""

from __future__ import annotations

import hashlib

from .campaign_planning import review_launch_readiness
from .runtime import ADVERTISING_CAMPAIGN_OPERATIONS_ALLOWED_DATABASE_BACKENDS
from .runtime import ADVERTISING_CAMPAIGN_OPERATIONS_REQUIRED_EVENT_TOPIC

PBC_KEY = "advertising_campaign_operations"
DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": ADVERTISING_CAMPAIGN_OPERATIONS_REQUIRED_EVENT_TOPIC,
    "retry_limit": 5,
    "default_currency": "USD",
    "default_timezone": "UTC",
    "budget_control_mode": "strict",
    "tracking_required": True,
    "workbench_limit": 50,
}
PARAMETERS = (
    {"name": "quality_score_floor", "type": "float", "minimum": 0.0, "maximum": 1.0},
    {"name": "materiality_threshold", "type": "float", "minimum": 0.0, "maximum": 1.0},
    {"name": "approval_sla_hours", "type": "int", "minimum": 1, "maximum": 240},
    {"name": "risk_threshold", "type": "float", "minimum": 0.0, "maximum": 1.0},
    {"name": "forecast_horizon_days", "type": "int", "minimum": 1, "maximum": 365},
    {"name": "workbench_limit", "type": "int", "minimum": 1, "maximum": 500},
)
RULE_TEMPLATES = (
    {
        "rule_id": "advertising_campaign_operations.launch_gate",
        "scope": "launch_readiness",
        "required_flags": (
            "budget_approved",
            "creative_approved",
            "audience_ready",
            "placements_ready",
            "tracking_ready",
            "suppliers_eligible",
            "policy_compliant",
        ),
    },
    {
        "rule_id": "advertising_campaign_operations.brief_quality",
        "scope": "campaign_brief",
        "required_sections": (
            "objective",
            "offer",
            "audience_promise",
            "channels",
            "primary_kpi",
            "guardrails",
            "launch_dependencies",
        ),
    },
)


def _hash(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "defaults": DEFAULT_CONFIGURATION,
        "required_fields": tuple(DEFAULT_CONFIGURATION),
        "database_backends": ADVERTISING_CAMPAIGN_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": ADVERTISING_CAMPAIGN_OPERATIONS_REQUIRED_EVENT_TOPIC,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def validate_configuration(config: dict | None = None) -> dict:
    merged = {**DEFAULT_CONFIGURATION, **dict(config or {})}
    ok = (
        merged["database_backend"] in ADVERTISING_CAMPAIGN_OPERATIONS_ALLOWED_DATABASE_BACKENDS
        and merged["event_topic"] == ADVERTISING_CAMPAIGN_OPERATIONS_REQUIRED_EVENT_TOPIC
        and int(merged["workbench_limit"]) > 0
    )
    return {
        "ok": ok,
        "configuration": merged,
        "side_effects": (),
    }


def parameter_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "parameters": tuple({**item, "bounded": True} for item in PARAMETERS),
        "side_effects": (),
    }


def set_parameter(name: str, value: object) -> dict:
    definition = next((item for item in PARAMETERS if item["name"] == name), None)
    if definition is None:
        return {"ok": False, "reason": "unknown_parameter", "name": name, "side_effects": ()}
    numeric = float(value)
    ok = definition["minimum"] <= numeric <= definition["maximum"]
    return {
        "ok": ok,
        "name": name,
        "value": value,
        "definition": definition,
        "bounded": True,
        "side_effects": (),
    }


def rule_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "rules": RULE_TEMPLATES,
        "side_effects": (),
    }


def compile_rule(rule: dict) -> dict:
    compiled = {**dict(rule), "compiled_hash": _hash(rule)}
    return {"ok": bool(rule.get("rule_id")), "rule": compiled, "side_effects": ()}


def evaluate_rule(rule: dict | str, payload: dict | None = None) -> dict:
    resolved_rule = next((item for item in RULE_TEMPLATES if item["rule_id"] == rule), None) if isinstance(rule, str) else dict(rule)
    if not resolved_rule:
        return {"ok": False, "reason": "unknown_rule", "rule": rule, "side_effects": ()}
    if resolved_rule["scope"] == "launch_readiness":
        review = review_launch_readiness(payload or {})
        return {
            "ok": True,
            "passed": review["launch_report"]["ready"],
            "rule": resolved_rule,
            "evaluation": review["launch_report"],
            "side_effects": (),
        }
    brief = dict((payload or {}).get("brief") or {})
    missing = tuple(field for field in resolved_rule.get("required_sections", ()) if not brief.get(field))
    return {
        "ok": True,
        "passed": not missing,
        "rule": resolved_rule,
        "missing_fields": missing,
        "side_effects": (),
    }


def governance_smoke_test() -> dict:
    config_result = validate_configuration()
    parameter_result = set_parameter("workbench_limit", 50)
    compiled_rule = compile_rule(RULE_TEMPLATES[0])
    evaluated_rule = evaluate_rule(
        RULE_TEMPLATES[0]["rule_id"],
        {
            "campaign_plan": {
                "campaign_id": "SMOKE",
                "brief": {
                    "objective": "Acquire qualified signups",
                    "offer": "30 day trial",
                    "audience_promise": "Reach in-market buyers",
                    "channels": ("search",),
                    "primary_kpi": "qualified_signups",
                    "guardrails": ("cpa",),
                    "launch_dependencies": ("tracking",),
                },
            },
            "readiness": {
                "budget_approved": True,
                "creative_approved": True,
                "audience_ready": True,
                "placements_ready": True,
                "tracking_ready": True,
                "suppliers_eligible": True,
                "policy_compliant": True,
                "dependency_status": {"tracking": True},
            },
        },
    )
    return {
        "ok": config_result["ok"] and parameter_result["ok"] and compiled_rule["ok"] and evaluated_rule["passed"] is True,
        "configuration": config_result,
        "parameter": parameter_result,
        "compiled_rule": compiled_rule,
        "evaluated_rule": evaluated_rule,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return governance_smoke_test()
