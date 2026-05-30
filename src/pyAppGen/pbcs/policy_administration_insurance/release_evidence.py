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
