"""Seeded scenario library for the clinical_trials_management PBC."""

from __future__ import annotations


PBC_KEY = "clinical_trials_management"
SEED_SCENARIOS = {
    "new_protocol": (
        {"table": "clinical_trials_management_trial_protocol", "record_id": "PROT-101", "status": "active"},
        {"table": "clinical_trials_management_clinical_trials_management_policy_rule", "record_id": "trial.safety.sla", "status": "active"},
    ),
    "site_activation": (
        {"table": "clinical_trials_management_study_site", "record_id": "SITE-001", "status": "active"},
    ),
    "subject_enrollment": (
        {"table": "clinical_trials_management_consent_record", "record_id": "CONS-001", "status": "current"},
        {"table": "clinical_trials_management_subject", "record_id": "SUBJ-001", "status": "enrolled"},
    ),
    "serious_event": (
        {"table": "clinical_trials_management_adverse_event", "record_id": "AE-001", "status": "closed"},
    ),
    "monitoring_finding": (
        {"table": "clinical_trials_management_monitoring_finding", "record_id": "MON-001", "status": "resolved"},
    ),
    "data_lock": (
        {"table": "clinical_trials_management_clinical_trials_management_control_assertion", "record_id": "LOCK-READINESS", "status": "ready"},
    ),
}


def scenario_library() -> dict:
    return {
        "ok": bool(SEED_SCENARIOS),
        "pbc": PBC_KEY,
        "scenario_names": tuple(SEED_SCENARIOS),
        "scenarios": dict(SEED_SCENARIOS),
        "side_effects": (),
    }


def seed_plan(name: str | None = None) -> dict:
    selected = dict(SEED_SCENARIOS) if name is None else {name: SEED_SCENARIOS.get(name, ())}
    if name is not None and name not in SEED_SCENARIOS:
        return {"ok": False, "pbc": PBC_KEY, "reason": "unknown_seed_scenario", "name": name, "side_effects": ()}
    records = tuple(record for scenario in selected.values() for record in scenario)
    return {"ok": True, "pbc": PBC_KEY, "scenarios": selected, "records": records, "side_effects": ()}


def validate_seed_data() -> dict:
    library = scenario_library()
    invalid_tables = tuple(
        record["table"]
        for scenario in SEED_SCENARIOS.values()
        for record in scenario
        if not record["table"].startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": library["ok"] and not invalid_tables,
        "pbc": PBC_KEY,
        "invalid_tables": invalid_tables,
        "side_effects": (),
    }


def smoke_test():
    plan = seed_plan()
    validation = validate_seed_data()
    return {"ok": plan["ok"] and validation["ok"], "plan": plan, "validation": validation, "side_effects": ()}
