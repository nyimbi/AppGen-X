from . import operations_engine as engine

PBC_KEY = engine.PBC_KEY
PARAMETERS = tuple(engine.PARAMETER_SPECS)
RULES = engine.RULES


def configuration_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": engine.ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
    }


def validate_configuration(config=None):
    configuration = dict(config or {"database_backend": "postgresql", "event_topic": engine.REQUIRED_EVENT_TOPIC})
    if any(key in configuration for key in ("stream_engine", "stream_processor", "runtime_profile")):
        return {"ok": False, "configuration": configuration, "reason": "stream_eventing_forbidden", "side_effects": ()}
    return {
        "ok": configuration.get("database_backend", "postgresql") in engine.ALLOWED_DATABASE_BACKENDS and configuration.get("event_topic", engine.REQUIRED_EVENT_TOPIC) == engine.REQUIRED_EVENT_TOPIC,
        "configuration": configuration,
        "side_effects": (),
    }


def parameter_manifest():
    return {"ok": True, "parameters": tuple({"name": name, **spec, "bounded": True} for name, spec in engine.PARAMETER_SPECS.items()), "side_effects": ()}


def set_parameter(state, name, value):
    result = engine.set_parameter(state or engine.empty_state(), name, value)
    return {"accepted": result["ok"], **result}


def rule_manifest():
    return {"ok": True, "rules": RULES, "side_effects": ()}


def compile_rule(rule):
    result = engine.register_rule(engine.empty_state(), rule)
    if not result["ok"]:
        return {"ok": False, "compiled": False, "reason": result["reason"], "rule": dict(rule), "side_effects": ()}
    compiled_rule = result["rule"]
    return {"ok": True, "compiled": True, "compiled_hash": compiled_rule["compiled_hash"], "rule": compiled_rule, "side_effects": ()}


def evaluate_rule(rule, payload=None):
    compiled_rule = rule["rule"] if isinstance(rule, dict) and "rule" in rule else rule
    configuration = dict(payload or {})
    allowed = configuration.get("database_backend", "postgresql") in engine.ALLOWED_DATABASE_BACKENDS and configuration.get("event_contract", "AppGen-X") == "AppGen-X"
    return {"ok": True, "allowed": allowed, "passed": allowed, "rule": compiled_rule, "payload": configuration, "side_effects": ()}


def governance_smoke_test():
    compiled_rule = compile_rule({"rule_id": RULES[0], "policy_area": "sampling_compliance"})
    return {
        "ok": configuration_manifest()["ok"] and validate_configuration()["ok"] and parameter_manifest()["ok"] and rule_manifest()["ok"] and compiled_rule["ok"] and evaluate_rule(compiled_rule, {"database_backend": "postgresql", "event_contract": "AppGen-X"})["allowed"],
        "side_effects": (),
    }


def smoke_test():
    return governance_smoke_test()
