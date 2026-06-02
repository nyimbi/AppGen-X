"""Seed data hooks for provider_revenue_cycle."""

from __future__ import annotations

from .standalone import DEFAULT_CONTROLS
from .standalone import DEFAULT_GOVERNED_MODELS
from .standalone import DEFAULT_PARAMETERS
from .standalone import DEFAULT_RULES

PBC_KEY = "provider_revenue_cycle"


def seed_plan() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "records": (
            {"table": "provider_revenue_cycle_patient_account", "code": "SEED_ACCOUNT", "tenant": "seed", "account_state": "registered"},
            {"table": "provider_revenue_cycle_provider_revenue_cycle_policy_rule", "code": DEFAULT_RULES[0]["rule_id"], "tenant": "seed"},
            {"table": "provider_revenue_cycle_provider_revenue_cycle_runtime_parameter", "code": "workbench_limit", "tenant": "seed", "value": DEFAULT_PARAMETERS["workbench_limit"]},
            {"table": "provider_revenue_cycle_provider_revenue_cycle_control_assertion", "code": DEFAULT_CONTROLS[0]["control_id"], "tenant": "seed"},
            {"table": "provider_revenue_cycle_provider_revenue_cycle_governed_model", "code": DEFAULT_GOVERNED_MODELS[0]["model_id"], "tenant": "seed"},
        ),
        "side_effects": (),
    }


def validate_seed_data() -> dict:
    plan = seed_plan()
    return {
        "ok": plan["ok"] and len(plan["records"]) >= 5,
        "pbc": PBC_KEY,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
