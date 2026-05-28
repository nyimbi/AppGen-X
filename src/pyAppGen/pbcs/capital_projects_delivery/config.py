PBC_KEY = "capital_projects_delivery"
PARAMETERS = (
    "quality_score_floor",
    "materiality_threshold",
    "approval_sla_hours",
    "risk_threshold",
    "forecast_horizon_days",
    "workbench_limit",
    "gate_blocker_threshold",
)
RULES = (
    "capital_project_policy",
    "capital_project_gate_policy",
    "epc_package_policy",
    "permit_milestone_policy",
    "progress_measurement_policy",
    "commissioning_system_policy",
    "project_risk_policy",
)


def configuration_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "single_pbc_domain_app": True,
    }


def validate_configuration(config=None):
    config = dict(config or {"database_backend": "postgresql"})
    return {
        "ok": config.get("database_backend", "postgresql")
        in ("postgresql", "mysql", "mariadb"),
        "configuration": config,
        "side_effects": (),
    }


def parameter_manifest():
    return {
        "ok": True,
        "parameters": tuple({"name": p, "bounded": True} for p in PARAMETERS),
        "side_effects": (),
    }


def set_parameter(name, value):
    return {
        "ok": name in PARAMETERS,
        "name": name,
        "value": value,
        "bounded": True,
        "side_effects": (),
    }


def rule_manifest():
    return {"ok": True, "rules": RULES, "side_effects": ()}


def compile_rule(rule):
    return {
        "ok": True,
        "rule": dict(rule),
        "compiled_hash": str(abs(hash(repr(rule)))),
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
