"""Configuration, rules, and parameter helpers for provider_revenue_cycle."""

from __future__ import annotations

import hashlib

from .runtime import PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS
from .runtime import PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC

PBC_KEY = "provider_revenue_cycle"
PARAMETERS = (
    "workbench_limit",
    "materiality_threshold",
    "timely_filing_warning_days",
    "claim_scrub_warning_limit",
    "underpayment_variance_threshold",
    "patient_statement_cycle_days",
    "collections_hold_days",
    "appeal_deadline_warning_days",
    "default_payment_plan_term_months",
    "charity_auto_hold_threshold",
)
RULES = (
    "patient_account_policy",
    "eligibility_benefits_policy",
    "prior_authorization_policy",
    "charge_capture_policy",
    "coding_cdi_policy",
    "claim_scrub_policy",
    "payer_contract_policy",
    "remit_era_policy",
    "denial_appeal_policy",
    "patient_balance_policy",
    "reconciliation_policy",
)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "required_event_topic": PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
    }


def validate_configuration(config: dict | None = None) -> dict:
    supplied = dict(config or {"database_backend": "postgresql", "event_topic": PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC})
    ok = (
        supplied.get("database_backend") in PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS
        and supplied.get("event_topic", PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC) == PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC
    )
    return {"ok": ok, "configuration": supplied, "side_effects": ()}


def parameter_manifest() -> dict:
    return {
        "ok": True,
        "parameters": tuple({"name": name, "bounded": True} for name in PARAMETERS),
        "side_effects": (),
    }


def set_parameter(name: str, value: object) -> dict:
    return {
        "ok": name in PARAMETERS,
        "name": name,
        "value": value,
        "bounded": True,
        "side_effects": (),
    }


def rule_manifest() -> dict:
    return {"ok": True, "rules": RULES, "side_effects": ()}


def compile_rule(rule: dict) -> dict:
    supplied = dict(rule)
    supplied["compiled_hash"] = _digest(rule)
    return {"ok": supplied.get("rule_id") in RULES or supplied.get("rule_type") in RULES, "rule": supplied, "side_effects": ()}


def evaluate_rule(rule: str, payload: dict | None = None) -> dict:
    supplied = dict(payload or {})
    passed = True
    if rule == "prior_authorization_policy":
        passed = supplied.get("authorization_status", "approved") in {"approved", "not_required"}
    elif rule == "claim_scrub_policy":
        passed = not supplied.get("fatal_findings")
    elif rule == "patient_balance_policy":
        passed = not (supplied.get("active_dispute") and supplied.get("collections_action"))
    elif rule == "reconciliation_policy":
        passed = float(supplied.get("open_variance_amount", 0.0)) <= float(supplied.get("threshold", 0.0))
    return {
        "ok": rule in RULES,
        "passed": passed,
        "rule": rule,
        "payload": supplied,
        "side_effects": (),
    }


def governance_smoke_test() -> dict:
    return {
        "ok": validate_configuration()["ok"]
        and parameter_manifest()["ok"]
        and rule_manifest()["ok"]
        and compile_rule({"rule_id": RULES[0]})["ok"]
        and evaluate_rule("claim_scrub_policy", {"fatal_findings": ()})["passed"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    return governance_smoke_test()
