"""Release evidence for the student_financial_aid PBC."""
from __future__ import annotations

from .slice_app import (
    PBC_KEY,
    build_release_evidence as _build_release_evidence,
    pbc_generation_smoke_audit,
    pbc_implementation_release_audit,
    pbc_source_artifact_contract,
)


def build_release_evidence() -> dict:
    return _build_release_evidence()


def student_financial_aid_build_release_evidence() -> dict:
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

# Improve1 student financial aid control release extension.
from .student_financial_aid_control import improve1_student_financial_aid_control_contract as _improve1_student_financial_aid_control_contract

_AID_CONTROL_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_AID_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence() -> dict:
    evidence = dict(_AID_CONTROL_BASE_BUILD_RELEASE_EVIDENCE())
    control = _improve1_student_financial_aid_control_contract()
    checks = tuple(evidence.get("checks", ())) + ({"id": "improve1_student_financial_aid_control", "ok": control["ok"]},)
    evidence.update({
        "ok": bool(evidence.get("ok")) and control["ok"],
        "checks": checks,
        "student_financial_aid_control": control,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ())),
    })
    return evidence


def validate_release_evidence() -> dict:
    validation = dict(_AID_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE())
    control = _improve1_student_financial_aid_control_contract()
    validation["ok"] = validation.get("ok") is True and control["ok"]
    validation["student_financial_aid_control"] = control
    validation["blocking_gaps"] = tuple(validation.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ()))
    return validation
