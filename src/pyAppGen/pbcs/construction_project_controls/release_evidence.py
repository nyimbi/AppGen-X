"""Release evidence helpers for construction project controls."""
from __future__ import annotations

from .runtime import (
    construction_project_controls_build_release_evidence,
    construction_project_controls_build_single_pbc_app_contract,
)
from .seed_data import seed_plan, validate_seed_data


def build_release_evidence():
    evidence = construction_project_controls_build_release_evidence()
    return {
        **evidence,
        "seed_scenarios": seed_plan()["scenarios"],
    }


def release_readiness_manifest():
    evidence = build_release_evidence()
    app_contract = construction_project_controls_build_single_pbc_app_contract()
    seeds = validate_seed_data()
    return {
        "ok": evidence["ok"] and app_contract["ok"] and seeds["ok"],
        "pbc": evidence["pbc"],
        "sections": (
            "schema",
            "services",
            "events",
            "handlers",
            "ui",
            "forms",
            "wizards",
            "controls",
            "agent",
            "go_live_scorecard",
        ),
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": (),
        "evidence": evidence,
        "seed_validation": seeds,
        "side_effects": (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {
        "ok": manifest["ok"],
        "pbc": manifest["pbc"],
        "missing_sections": (),
        "failed_checks": tuple(manifest["blocking_gaps"]),
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test():
    return {
        "ok": release_readiness_manifest()["ok"] and validate_release_evidence()["ok"],
        "side_effects": (),
    }
