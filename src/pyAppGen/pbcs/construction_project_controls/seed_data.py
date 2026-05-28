"""Package-local seed scenarios for construction project controls."""
from __future__ import annotations

from .runtime import (
    construction_project_controls_approve_baseline_revision,
    construction_project_controls_command_construction_project,
    construction_project_controls_create_change_event,
    construction_project_controls_empty_state,
    construction_project_controls_record_schedule_risk,
    construction_project_controls_record_site_progress,
    construction_project_controls_record_work_package,
)

PBC_KEY = "construction_project_controls"


def seed_plan():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "scenarios": (
            {"project_code": "SEED-ONTRACK", "profile": "on_track"},
            {"project_code": "SEED-DELAY", "profile": "delayed"},
            {"project_code": "SEED-CHANGE", "profile": "change_heavy"},
            {"project_code": "SEED-OVER", "profile": "contractor_overstatement"},
        ),
        "side_effects": (),
    }


def load_seed_state():
    state = construction_project_controls_empty_state()
    scenarios = (
        {
            "code": "SEED-ONTRACK",
            "name": "On-track logistics hub",
            "approved_budget": 180000.0,
            "wbs_code": "1.1",
            "planned_quantity": 120.0,
            "installed_quantity": 60.0,
            "actual_cost": 70000.0,
            "float_days": 8,
        },
        {
            "code": "SEED-DELAY",
            "name": "Delayed hospital podium",
            "approved_budget": 220000.0,
            "wbs_code": "2.1",
            "planned_quantity": 100.0,
            "installed_quantity": 35.0,
            "actual_cost": 95000.0,
            "float_days": -4,
        },
        {
            "code": "SEED-CHANGE",
            "name": "Change-heavy process plant",
            "approved_budget": 260000.0,
            "wbs_code": "3.1",
            "planned_quantity": 80.0,
            "installed_quantity": 30.0,
            "actual_cost": 110000.0,
            "float_days": 2,
            "change_impact": 45000.0,
        },
    )
    for scenario in scenarios:
        created = construction_project_controls_command_construction_project(
            state,
            {
                "tenant": "seed",
                "code": scenario["code"],
                "name": scenario["name"],
                "approved_budget": scenario["approved_budget"],
                "original_budget": scenario["approved_budget"],
                "reported_at": "2026-05-29",
            },
        )
        state = created["state"]
        state = construction_project_controls_approve_baseline_revision(
            state,
            {
                "project_id": scenario["code"],
                "baseline_start_date": "2026-06-01",
                "baseline_finish_date": "2026-10-31",
                "freeze_reason": "Seed baseline",
                "approved_by": "seed.controls",
                "approved_at": "2026-05-29",
                "approver_role": "project_controls_manager",
            },
        )["state"]
        work_package = construction_project_controls_record_work_package(
            state,
            {
                "project_id": scenario["code"],
                "wbs_code": scenario["wbs_code"],
                "control_account": scenario["wbs_code"].split(".")[0],
                "discipline": "civil",
                "planned_quantity": scenario["planned_quantity"],
                "measurement_unit": "m3",
                "planned_percent_complete": 50.0,
                "approved_budget": scenario["approved_budget"] / 2.0,
            },
        )
        state = work_package["state"]
        state = construction_project_controls_record_site_progress(
            state,
            {
                "project_id": scenario["code"],
                "work_package_id": work_package["record"]["id"],
                "measurement_date": "2026-06-30",
                "installed_quantity": scenario["installed_quantity"],
                "actual_cost_incurred": scenario["actual_cost"],
                "submission_key": f"{scenario['code']}:progress",
                "evidence_bundle": {"photos": 4, "report": "seed"},
            },
        )["state"]
        state = construction_project_controls_record_schedule_risk(
            state,
            {
                "project_id": scenario["code"],
                "work_package_id": work_package["record"]["id"],
                "current_float_days": scenario["float_days"],
                "prior_float_days": scenario["float_days"] + 3,
            },
        )["state"]
        if scenario.get("change_impact"):
            state = construction_project_controls_create_change_event(
                state,
                {
                    "project_id": scenario["code"],
                    "code": f"{scenario['code']}-CE1",
                    "cost_impact": scenario["change_impact"],
                    "approval_state": "pending",
                },
            )["state"]

    created = construction_project_controls_command_construction_project(
        state,
        {
            "tenant": "seed",
            "code": "SEED-OVER",
            "name": "Overstatement contractor package",
            "approved_budget": 140000.0,
            "original_budget": 140000.0,
            "reported_at": "2026-05-29",
        },
    )
    state = created["state"]
    state = construction_project_controls_approve_baseline_revision(
        state,
        {
            "project_id": "SEED-OVER",
            "baseline_start_date": "2026-06-01",
            "baseline_finish_date": "2026-08-31",
            "freeze_reason": "Seed baseline",
            "approved_by": "seed.controls",
            "approved_at": "2026-05-29",
            "approver_role": "project_controls_manager",
        },
    )["state"]
    work_package = construction_project_controls_record_work_package(
        state,
        {
            "project_id": "SEED-OVER",
            "wbs_code": "4.1",
            "control_account": "4",
            "discipline": "structural",
            "planned_quantity": 20.0,
            "measurement_unit": "tons",
            "planned_percent_complete": 40.0,
            "approved_budget": 70000.0,
        },
    )
    state = work_package["state"]
    held = construction_project_controls_record_site_progress(
        state,
        {
            "project_id": "SEED-OVER",
            "work_package_id": work_package["record"]["id"],
            "measurement_date": "2026-06-30",
            "installed_quantity": 25.0,
            "actual_cost_incurred": 20000.0,
            "submission_key": "SEED-OVER:progress",
            "evidence_bundle": {"photos": 1},
        },
    )
    return {
        "ok": held["ok"] is False,
        "pbc": PBC_KEY,
        "state": held["state"],
        "scenarios_loaded": ("SEED-ONTRACK", "SEED-DELAY", "SEED-CHANGE", "SEED-OVER"),
        "held_submission_reason": held["reason"],
        "side_effects": (),
    }


def validate_seed_data():
    loaded = load_seed_state()
    return {
        "ok": loaded["ok"] and len(loaded["scenarios_loaded"]) == 4,
        "pbc": PBC_KEY,
        "side_effects": (),
    }


def smoke_test():
    loaded = load_seed_state()
    return {"ok": loaded["ok"] and validate_seed_data()["ok"], "side_effects": ()}
