"""Release evidence for the laboratory_information_management PBC."""

from __future__ import annotations

from pathlib import Path

from .runtime import laboratory_information_management_build_release_evidence
from .standalone import documentation_presence
from .standalone import standalone_manifest
from .standalone import standalone_smoke_test


def build_release_evidence():
    evidence = dict(laboratory_information_management_build_release_evidence())
    evidence["standalone_app"] = standalone_manifest()
    evidence["documentation"] = documentation_presence()
    extra_checks = (
        {"id": "standalone_app_surface", "ok": evidence["standalone_app"].get("ok") is True},
        {"id": "package_documentation_present", "ok": evidence["documentation"].get("ok") is True},
    )
    evidence["checks"] = tuple(evidence.get("checks", ())) + extra_checks
    evidence["blocking_gaps"] = tuple(check for check in evidence["checks"] if check.get("ok") is not True)
    evidence["ok"] = not evidence["blocking_gaps"]
    return evidence


def release_readiness_manifest():
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("generated_artifacts", "standalone_app", "documentation")
        if isinstance(evidence.get(name), dict)
    )
    return {
        "ok": evidence["ok"],
        "pbc": evidence["pbc"],
        "sections": sections,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    evidence = manifest["evidence"]
    missing_sections = tuple(section for section in ("generated_artifacts", "standalone_app", "documentation") if section not in manifest["sections"])
    failed_checks = tuple(check for check in evidence.get("checks", ()) if check.get("ok") is not True)
    return {
        "ok": manifest["ok"] and not missing_sections and not failed_checks,
        "pbc": manifest["pbc"],
        "missing_sections": missing_sections,
        "failed_checks": failed_checks,
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test():
    standalone = standalone_smoke_test()
    validation = validate_release_evidence()
    return {
        "ok": standalone["ok"] and validation["ok"],
        "standalone": standalone,
        "validation": validation,
        "side_effects": (),
    }
