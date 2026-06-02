from __future__ import annotations

from .standalone import PBC_KEY, build_standalone_app, default_configuration, default_governed_models, default_parameter_values, default_rules, default_units, seed_plan as standalone_seed_plan


def seed_plan() -> dict:
    return standalone_seed_plan()


def default_configuration_bundle() -> dict:
    return default_configuration()


def default_parameter_bundle() -> dict:
    return default_parameter_values()


def default_rule_bundle() -> tuple[dict, ...]:
    return default_rules()


def default_unit_bundle(tenant: str = "tenant_alpha") -> tuple[dict, ...]:
    return default_units(tenant)


def default_governed_model_bundle() -> tuple[dict, ...]:
    return default_governed_models()


def validate_seed_data() -> dict:
    app = build_standalone_app()
    app.load_demo_workspace("tenant_seed")
    workbench = app.build_workbench_view("tenant_seed")
    return {"ok": workbench["summary"]["active_incident_count"] >= 1 and workbench["summary"]["available_unit_count"] >= 1, "pbc": PBC_KEY, "workbench": workbench, "side_effects": ()}


def smoke_test() -> dict:
    validation = validate_seed_data()
    return {"ok": seed_plan()["ok"] and validation["ok"], "validation": validation, "side_effects": ()}
