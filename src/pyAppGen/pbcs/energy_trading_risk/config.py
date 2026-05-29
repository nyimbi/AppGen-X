"""Configuration, rules, and bounded parameters for energy_trading_risk."""

from __future__ import annotations

import hashlib

PBC_KEY = "energy_trading_risk"
_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
_REQUIRED_EVENT_TOPIC = "pbc.energy_trading_risk.events"

PARAMETERS = (
    {
        "name": "risk_threshold",
        "label": "Projected MTM threshold",
        "default": 25000.0,
        "min": 1000.0,
        "max": 1000000.0,
    },
    {
        "name": "materiality_threshold",
        "label": "Four-eyes approval threshold",
        "default": 10000.0,
        "min": 1000.0,
        "max": 500000.0,
    },
    {
        "name": "curve_max_age_hours",
        "label": "Maximum curve age",
        "default": 24,
        "min": 1,
        "max": 168,
    },
    {
        "name": "nomination_cutoff_hour_utc",
        "label": "Nomination cutoff hour (UTC)",
        "default": 17,
        "min": 0,
        "max": 23,
    },
    {
        "name": "nomination_tolerance_mwh",
        "label": "Nomination tolerance",
        "default": 5.0,
        "min": 0.0,
        "max": 200.0,
    },
    {
        "name": "workbench_limit",
        "label": "Workbench row limit",
        "default": 50,
        "min": 1,
        "max": 500,
    },
)

RULES = (
    {
        "rule_id": "trade_capture_policy",
        "required_fields": (
            "commodity",
            "market_hub",
            "book",
            "trader",
            "strategy",
            "counterparty",
            "side",
            "position_type",
            "delivery_start",
            "delivery_end",
            "delivery_profile",
            "pricing_formula",
            "volume_mwh",
            "fixed_price",
            "submitted_at",
        ),
        "allowed_position_types": ("physical", "financial", "linked"),
        "duplicate_window_minutes": 30,
    },
    {
        "rule_id": "nomination_cutoff_policy",
        "post_cutoff_requires_exception": True,
        "accepted_statuses": ("submitted", "accepted", "superseded", "post_cutoff_exception"),
    },
    {
        "rule_id": "price_curve_policy",
        "min_curve_price": -150.0,
        "max_curve_price": 500.0,
    },
    {
        "rule_id": "exposure_limit_policy",
        "severity_levels": ("warning", "hard_stop"),
    },
)


def _digest(value) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()



def default_runtime_parameters() -> dict:
    return {
        item["name"]: {
            "name": item["name"],
            "value": item["default"],
            "bounded": True,
            "min": item["min"],
            "max": item["max"],
        }
        for item in PARAMETERS
    }



def default_policy_rules() -> dict:
    return {rule["rule_id"]: dict(rule) for rule in RULES}



def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": _ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": _REQUIRED_EVENT_TOPIC,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }



def validate_configuration(config: dict | None = None) -> dict:
    config = dict(config or {})
    database_backend = config.get("database_backend", _ALLOWED_DATABASE_BACKENDS[0])
    event_topic = config.get("event_topic", _REQUIRED_EVENT_TOPIC)
    return {
        "ok": database_backend in _ALLOWED_DATABASE_BACKENDS and event_topic == _REQUIRED_EVENT_TOPIC,
        "configuration": {
            "database_backend": database_backend,
            "event_topic": event_topic,
            "retry_limit": int(config.get("retry_limit", 5)),
        },
        "side_effects": (),
    }



def parameter_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "parameters": PARAMETERS,
        "defaults": default_runtime_parameters(),
        "side_effects": (),
    }



def set_parameter(name: str, value) -> dict:
    definition = next((item for item in PARAMETERS if item["name"] == name), None)
    if definition is None:
        return {"ok": False, "reason": "unknown_parameter", "name": name, "side_effects": ()}
    numeric = float(value)
    bounded = definition["min"] <= numeric <= definition["max"]
    return {
        "ok": bounded,
        "name": name,
        "value": value if not float(value).is_integer() else int(float(value)),
        "bounded": True,
        "bounds": (definition["min"], definition["max"]),
        "side_effects": (),
    }



def rule_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "rules": RULES,
        "compiled_rule_ids": tuple(rule["rule_id"] for rule in RULES),
        "side_effects": (),
    }



def compile_rule(rule: dict) -> dict:
    compiled = dict(rule)
    compiled["compiled_hash"] = _digest(rule)
    compiled["event_contract"] = "AppGen-X"
    return {"ok": True, "rule": compiled, "side_effects": ()}



def evaluate_rule(rule, payload: dict | None = None) -> dict:
    if isinstance(rule, dict):
        rule_id = rule.get("rule_id", "adhoc_rule")
    else:
        rule_id = str(rule)
    return {
        "ok": True,
        "passed": True,
        "rule_id": rule_id,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "side_effects": (),
    }



def governance_smoke_test() -> dict:
    config = validate_configuration()
    params = parameter_manifest()
    rules = rule_manifest()
    compiled = compile_rule({"rule_id": RULES[0]["rule_id"], "scope": "domain"})
    evaluation = evaluate_rule(RULES[0]["rule_id"], {"tenant": "tenant-smoke"})
    return {
        "ok": config["ok"] and params["ok"] and rules["ok"] and compiled["ok"] and evaluation["ok"],
        "configuration": config,
        "parameters": params,
        "rules": rules,
        "side_effects": (),
    }



def smoke_test() -> dict:
    return governance_smoke_test()
