"""Generated release evidence for the smart_city_mobility_operations PBC."""

from __future__ import annotations

from pathlib import Path

from .runtime import smart_city_mobility_operations_build_release_evidence


def _documentation_artifacts():
    base = Path(__file__).parent
    artifacts = (
        {"name": "SPECIFICATION.md", "exists": (base / "SPECIFICATION.md").exists()},
        {"name": "RELEASE_EVIDENCE.md", "exists": (base / "RELEASE_EVIDENCE.md").exists()},
        {"name": "improve1.md", "exists": (base / "improve1.md").exists()},
        {"name": "standalone.py", "exists": (base / "standalone.py").exists()},
    )
    missing = tuple(item["name"] for item in artifacts if not item["exists"])
    return {"ok": not missing, "artifacts": artifacts, "missing": missing}


def build_release_evidence():
    evidence = dict(smart_city_mobility_operations_build_release_evidence())
    evidence["documentation"] = _documentation_artifacts()
    checks = tuple(evidence.get("checks", ())) + (
        {"id": "package_documentation_present", "ok": evidence["documentation"]["ok"]},
    )
    evidence["checks"] = checks
    evidence["blocking_gaps"] = tuple(check for check in checks if check.get("ok") is not True)
    evidence["ok"] = not evidence["blocking_gaps"]
    return evidence


def release_readiness_manifest():
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("generated_artifacts", "documentation")
        if name in evidence
    )
    return {
        "ok": evidence["ok"],
        "pbc": evidence["pbc"],
        "sections": sections,
        "blocking_gaps": evidence["blocking_gaps"],
        "boundary_gaps": (),
        "evidence": evidence,
        "side_effects": (),
    }


def validate_release_evidence():
    manifest = release_readiness_manifest()
    return {
        "ok": manifest["ok"],
        "pbc": manifest["pbc"],
        "missing_sections": tuple(
            section for section in ("generated_artifacts", "documentation") if section not in manifest["sections"]
        ),
        "failed_checks": tuple(check for check in manifest["evidence"]["checks"] if check["ok"] is not True),
        "boundary_gaps": (),
        "side_effects": (),
    }


def smoke_test():
    validation = validate_release_evidence()
    evidence = build_release_evidence()
    return {
        "ok": validation["ok"] and evidence["ok"],
        "validation": validation,
        "evidence": evidence,
        "side_effects": (),
    }
