"""Configuration, rules, and parameters for hotel revenue management."""

from __future__ import annotations

import hashlib

from .runtime import HOTEL_REVENUE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
from .runtime import HOTEL_REVENUE_MANAGEMENT_REQUIRED_EVENT_TOPIC
from .runtime import PARAMETER_BOUNDS
from .runtime import PBC_KEY
from .runtime import RULE_DEFAULTS


DOMAIN_PARAMETER_SCHEMA = tuple(
    {
        "key": key,
        "scope": "runtime" if key in {"workbench_limit", "approval_sla_hours"} else "control",
        "default": bounds[0],
        "min_value": bounds[0],
        "max_value": bounds[1],
    }
    for key, bounds in PARAMETER_BOUNDS.items()
)
DOMAIN_RULE_SCHEMA = RULE_DEFAULTS


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": HOTEL_REVENUE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": HOTEL_REVENUE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "domain_parameter_schema": DOMAIN_PARAMETER_SCHEMA,
        "domain_rule_schema": DOMAIN_RULE_SCHEMA,
        "side_effects": (),
    }


def validate_configuration(config: dict | None = None) -> dict:
    config = dict(config or {"database_backend": "postgresql"})
    forbidden = tuple(
        field for field in config if field in {"stream_engine", "stream_engine_picker", "eventing_choice"}
    )
    ok = (
        config.get("database_backend", "postgresql") in HOTEL_REVENUE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
        and config.get("event_topic", HOTEL_REVENUE_MANAGEMENT_REQUIRED_EVENT_TOPIC)
        == HOTEL_REVENUE_MANAGEMENT_REQUIRED_EVENT_TOPIC
        and not forbidden
    )
    return {
        "ok": ok,
        "config": config,
        "forbidden_fields": forbidden,
        "side_effects": (),
    }


def parameter_manifest() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "parameters": DOMAIN_PARAMETER_SCHEMA, "side_effects": ()}


def set_parameter(name: str, value: object) -> dict:
    schema = next((item for item in DOMAIN_PARAMETER_SCHEMA if item["key"] == name), None)
    if schema is None:
        return {"ok": False, "parameter": name, "reason": "unknown_parameter", "side_effects": ()}
    numeric = float(value)
    ok = schema["min_value"] <= numeric <= schema["max_value"]
    return {
        "ok": ok,
        "parameter": name,
        "value": numeric,
        "parameter_scope": schema["scope"],
        "bounded": True,
        "reason": None if ok else "parameter_out_of_bounds",
        "side_effects": (),
    }


def rule_manifest() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "rules": DOMAIN_RULE_SCHEMA, "side_effects": ()}


def compile_rule(rule: dict | None) -> dict:
    rule = dict(rule or {})
    if any(key in rule for key in ("stream_engine", "stream_engine_picker", "eventing_choice")):
        return {"ok": False, "compiled": False, "reason": "stream_engine_picker_disallowed", "side_effects": ()}
    compiled_hash = hashlib.sha256(repr(sorted(rule.items())).encode("utf-8")).hexdigest()
    return {
        "ok": True,
        "compiled": True,
        "rule": rule,
        "scope": rule.get("scope"),
        "condition": rule.get("condition"),
        "compiled_hash": compiled_hash,
        "side_effects": (),
    }


def evaluate_rule(compiled: dict | str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    if isinstance(compiled, str):
        compiled = compile_rule({"rule_id": compiled, "scope": "ad-hoc", "condition": compiled})
    condition = str(compiled.get("condition", "")).lower()
    allowed = compiled.get("ok") is True
    if "sellable_rooms <= physical_rooms" in condition:
        allowed = payload.get("sellable_rooms", 0) <= payload.get("physical_rooms", 0)
    elif "member_rate <= public_rate" in condition:
        allowed = payload.get("member_rate", 0) <= payload.get("public_rate", payload.get("member_rate", 0))
    elif "allotment >= 0" in condition:
        allowed = payload.get("allotment", 0) >= 0
    elif "reconciles to property forecast" in condition:
        allowed = payload.get("forecast_rooms", 0) == sum(payload.get("segments", ()))
    return {
        "ok": compiled.get("ok") is True,
        "allowed": allowed,
        "scope": compiled.get("scope"),
        "context": payload,
        "side_effects": (),
    }


def governance_smoke_test() -> dict:
    compiled = compile_rule(DOMAIN_RULE_SCHEMA[0])
    return {
        "ok": configuration_manifest()["ok"]
        and validate_configuration({"database_backend": "postgresql"})["ok"]
        and parameter_manifest()["ok"]
        and set_parameter("workbench_limit", 30)["ok"]
        and rule_manifest()["ok"]
        and compiled["ok"]
        and evaluate_rule(compiled, {"sellable_rooms": 8, "physical_rooms": 10})["allowed"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    return governance_smoke_test()
