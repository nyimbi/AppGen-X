"""Release evidence for the customer_success_management PBC."""
from __future__ import annotations

from .success_control import improve1_success_control_contract
from .slice_app import (
    PBC_KEY,
    build_release_evidence as _build_release_evidence,
    pbc_generation_smoke_audit,
    pbc_implementation_release_audit,
    pbc_source_artifact_contract,
)


def build_release_evidence() -> dict:
    evidence = _build_release_evidence()
    success_control = improve1_success_control_contract()
    checks = tuple(evidence.get("checks", ())) + ({"id": "improve1_success_control", "ok": success_control["ok"]},)
    return {**evidence, "ok": evidence["ok"] and success_control["ok"], "checks": checks, "improve1_success_control": success_control, "blocking_gaps": tuple(check.get("id") for check in checks if not check.get("ok"))}


def customer_success_management_build_release_evidence() -> dict:
    return build_release_evidence()


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"],
        "pbc": PBC_KEY,
        "sections": (
            "schema",
            "service",
            "api",
            "events",
            "handlers",
            "ui",
            "agent",
            "governance",
            "tests",
            "release_audits",
        ),
        "checks": evidence["checks"],
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "boundary_gaps": tuple(evidence.get("boundary_gaps", ())),
        "audits": evidence["audits"],
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    evidence = build_release_evidence()
    failed = tuple(check for check in evidence["checks"] if not check["ok"])
    return {
        "ok": evidence["ok"] and not failed and not evidence["boundary_gaps"],
        "missing_sections": (),
        "failed_checks": failed,
        "boundary_gaps": evidence["boundary_gaps"],
        "blocking_gaps": evidence["blocking_gaps"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    source = pbc_source_artifact_contract()
    implementation = pbc_implementation_release_audit()
    generation = pbc_generation_smoke_audit()
    validation = validate_release_evidence()
    return {
        "ok": source["ok"] and implementation["ok"] and generation["ok"] and validation["ok"],
        "validation": validation,
        "side_effects": (),
    }
