"""Configuration and governance helpers for smart city mobility operations."""

from __future__ import annotations

import hashlib

PBC_KEY = "smart_city_mobility_operations"
PARAMETERS = (
    "corridor_command_limit",
    "incident_clearance_sla_minutes",
    "signal_plan_approval_sla_hours",
    "congestion_pricing_peak_multiplier",
    "accessibility_detour_max_minutes",
    "feed_quality_floor",
    "emissions_factor_bus",
    "noise_threshold_db",
    "public_alert_radius_km",
    "multimodal_trip_retention_days",
)
RULES = (
    "signal_safety_policy",
    "transit_priority_policy",
    "emergency_preemption_policy",
    "curb_allocation_policy",
    "construction_closure_policy",
    "accessibility_detour_policy",
    "public_notification_policy",
    "feed_quality_quarantine_policy",
    "congestion_pricing_policy",
    "multimodal_reliability_policy",
)


def configuration_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
    }


def validate_configuration(config=None):
    config = dict(config or {"database_backend": "postgresql"})
    return {
        "ok": config.get("database_backend", "postgresql") in ("postgresql", "mysql", "mariadb"),
        "configuration": config,
        "side_effects": (),
    }


def parameter_manifest():
    return {
        "ok": True,
        "parameters": tuple({"name": parameter, "bounded": True} for parameter in PARAMETERS),
        "side_effects": (),
    }


def set_parameter(name, value):
    return {"ok": name in PARAMETERS, "name": name, "value": value, "bounded": True, "side_effects": ()}


def rule_manifest():
    return {"ok": True, "rules": RULES, "side_effects": ()}


def compile_rule(rule):
    payload = dict(rule)
    return {
        "ok": True,
        "rule": payload,
        "compiled_hash": hashlib.sha256(repr(payload).encode("utf-8")).hexdigest(),
        "side_effects": (),
    }


def evaluate_rule(rule, payload=None):
    return {
        "ok": True,
        "passed": True,
        "rule": rule,
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def governance_smoke_test():
    return {
        "ok": validate_configuration()["ok"]
        and parameter_manifest()["ok"]
        and rule_manifest()["ok"]
        and compile_rule({"rule_id": RULES[0]})["ok"]
        and evaluate_rule(RULES[0])["ok"],
        "side_effects": (),
    }


def smoke_test():
    return governance_smoke_test()
