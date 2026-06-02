from __future__ import annotations

from .standalone import PBC_KEY, build_standalone_app, default_configuration, default_parameter_values, default_rules

PARAMETERS = tuple(default_parameter_values())
RULES = tuple(rule["rule_id"] for rule in default_rules())


def configuration_manifest() -> dict:
    config = default_configuration()
    return {"ok": True, "pbc": PBC_KEY, "database_backends": ("postgresql", "mysql", "mariadb"), "event_contract": "AppGen-X", "configuration": config, "stream_engine_picker_visible": False}


def validate_configuration(config: dict | None = None) -> dict:
    app = build_standalone_app()
    result = app.configure_runtime(dict(config or default_configuration()))
    return {"ok": result["ok"], "configuration": result["configuration"], "side_effects": ()}


def parameter_manifest() -> dict:
    return {"ok": True, "parameters": tuple({"name": name, "bounded": True} for name in PARAMETERS), "side_effects": ()}


def set_parameter(name: str, value):
    return build_standalone_app().set_parameter(name, value)


def rule_manifest() -> dict:
    return {"ok": True, "rules": RULES, "side_effects": ()}


def compile_rule(rule: dict) -> dict:
    return build_standalone_app().register_rule(rule)


def evaluate_rule(rule: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    return {"ok": rule in RULES, "passed": rule in RULES and not payload.get("force_fail"), "rule": rule, "payload": payload, "side_effects": ()}


def governance_smoke_test() -> dict:
    return {"ok": validate_configuration()["ok"] and parameter_manifest()["ok"] and rule_manifest()["ok"] and compile_rule({"rule_id": RULES[0]})["ok"] and evaluate_rule(RULES[0])["ok"], "side_effects": ()}


def smoke_test() -> dict:
    return governance_smoke_test()
