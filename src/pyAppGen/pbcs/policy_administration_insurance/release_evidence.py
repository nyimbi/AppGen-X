"""Release evidence helpers for the policy_administration_insurance PBC."""

from __future__ import annotations

from pathlib import Path

from .runtime import policy_administration_insurance_build_release_evidence as _runtime_release_evidence
from .standalone import policy_administration_insurance_standalone_app_contract


_DOCS = (
    "README.md",
    "implementation-plan.md",
    "implementation-status.md",
    "SPECIFICATION.md",
    "RELEASE_EVIDENCE.md",
)


def _documentation_artifacts() -> dict:
    base = Path(__file__).parent
    artifacts = tuple({"name": name, "exists": (base / name).exists()} for name in _DOCS)
    missing = tuple(item["name"] for item in artifacts if not item["exists"])
    return {
        "ok": not missing,
        "artifacts": artifacts,
        "missing": missing,
    }


def build_release_evidence() -> dict:
    evidence = dict(_runtime_release_evidence())
    evidence["standalone_app"] = policy_administration_insurance_standalone_app_contract()
    evidence["documentation"] = _documentation_artifacts()
    evidence["ui_surface"] = {
        "forms": evidence["generated_artifacts"]["ui"],
        "standalone_workbench": "policy_administration_insurance_render_standalone_workbench",
    }
    extra_checks = (
        {"id": "standalone_app_surface", "ok": evidence["standalone_app"]["ok"] is True},
        {"id": "package_documentation_present", "ok": evidence["documentation"]["ok"] is True},
    )
    evidence["checks"] = tuple(evidence.get("checks", ())) + extra_checks
    evidence["blocking_gaps"] = tuple(check for check in evidence["checks"] if check.get("ok") is not True)
    evidence["ok"] = not evidence["blocking_gaps"]
    return evidence


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    return {
        "ok": evidence["ok"] and bool(evidence.get("checks")),
        "pbc": evidence["pbc"],
        "sections": (
            "schema",
            "services",
            "events",
            "handlers",
            "ui",
            "agent",
            "governance",
            "standalone_app",
            "documentation",
        ),
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    manifest = release_readiness_manifest()
    evidence = manifest["evidence"]
    failed_checks = tuple(check for check in manifest["blocking_gaps"] if check.get("ok") is not True)
    missing_sections = tuple(
        section
        for section in ("standalone_app", "documentation")
        if not isinstance(evidence.get(section), dict)
    )
    return {
        "ok": manifest["ok"] and not missing_sections and not failed_checks,
        "pbc": manifest["pbc"],
        "missing_sections": missing_sections,
        "failed_checks": failed_checks,
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test() -> dict:
    evidence = build_release_evidence()
    validation = validate_release_evidence()
    return {
        "ok": evidence["ok"] and validation["ok"],
        "evidence": evidence,
        "validation": validation,
        "side_effects": (),
    }

# Improve1 policy release evidence extension.
from .policy_control import improve1_policy_control_contract as _improve1_policy_control_contract

_POLICY_CONTROL_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence
_POLICY_CONTROL_BASE_RELEASE_READINESS_MANIFEST = release_readiness_manifest
_POLICY_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE = validate_release_evidence


def build_release_evidence() -> dict:
    evidence = dict(_POLICY_CONTROL_BASE_BUILD_RELEASE_EVIDENCE())
    control = _improve1_policy_control_contract()
    evidence["ok"] = bool(evidence.get("ok")) and control["ok"]
    evidence["policy_control"] = control
    evidence["traceability"] = tuple(dict.fromkeys(tuple(evidence.get("traceability", ())) + ("improve1_policy_control", "tests/test_domain_behavior.py")))
    evidence["blocking_gaps"] = tuple(evidence.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ()))
    return evidence


def release_readiness_manifest() -> dict:
    manifest = dict(_POLICY_CONTROL_BASE_RELEASE_READINESS_MANIFEST())
    control = _improve1_policy_control_contract()
    manifest["ok"] = bool(manifest.get("ok")) and control["ok"]
    manifest["policy_control"] = control
    manifest["blocking_gaps"] = tuple(manifest.get("blocking_gaps", ())) + tuple(control.get("blocking_gaps", ()))
    return manifest


def validate_release_evidence() -> dict:
    validation = dict(_POLICY_CONTROL_BASE_VALIDATE_RELEASE_EVIDENCE())
    control = _improve1_policy_control_contract()
    validation["ok"] = bool(validation.get("ok")) and control["ok"]
    validation["policy_control"] = control
    validation["failed_checks"] = tuple(validation.get("failed_checks", ())) + tuple(control.get("blocking_gaps", ()))
    return validation
