"""Generated release evidence for the composition_engine PBC."""

from __future__ import annotations

from .runtime import composition_engine_build_release_evidence


RELEASE_EVIDENCE = {
    **composition_engine_build_release_evidence(),
    "pbc": "composition_engine",
}


def build_release_evidence():
    """Return generated release audit evidence for this PBC."""
    return dict(RELEASE_EVIDENCE)


def release_readiness_manifest():
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in (
            "schema",
            "service",
            "api",
            "permissions",
            "ui",
            "workbench",
            "smoke_plan",
            "documentation",
            "security",
            "rehearsal",
            "assistant",
            "agent_competencies",
        )
        if isinstance(evidence.get(name), dict)
    )
    checks = tuple(evidence.get("checks", ()))
    return {
        "ok": evidence.get("ok") is True and bool(checks),
        "pbc": "composition_engine",
        "format": evidence.get("format"),
        "sections": sections,
        "checks": checks,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "required_sections": ("schema", "service", "rehearsal", "assistant"),
        "side_effects": (),
    }


def validate_release_evidence():
    """Validate release evidence, blocking gaps, and owned-boundary proof."""
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["required_sections"] if section not in manifest["sections"])
    failed_checks = tuple(check for check in manifest["checks"] if check.get("ok") is not True)
    security = evidence.get("security", {}) if isinstance(evidence.get("security"), dict) else {}
    rehearsal = evidence.get("rehearsal", {}) if isinstance(evidence.get("rehearsal"), dict) else {}
    boundary = evidence.get("boundary", {}) if isinstance(evidence.get("boundary"), dict) else {}
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("security_blocking_findings", bool(security.get("blocking_findings"))),
            ("release_freeze", bool(rehearsal.get("release_freeze"))),
            ("boundary_violation", boundary.get("ok") is not True),
        )
        if failed
    )
    return {
        "ok": manifest["ok"]
        and evidence.get("pbc") == manifest["pbc"]
        and not manifest["blocking_gaps"]
        and not missing_sections
        and not failed_checks
        and not boundary_gaps,
        "pbc": "composition_engine",
        "manifest": manifest,
        "missing_sections": missing_sections,
        "failed_checks": failed_checks,
        "boundary_gaps": boundary_gaps,
        "side_effects": (),
    }


def smoke_test():
    """Exercise release evidence readiness validation side-effect-free."""
    validation = validate_release_evidence()
    evidence = build_release_evidence()
    return {
        "ok": validation["ok"] and evidence.get("ok") is True,
        "validation": validation,
        "evidence": evidence,
        "side_effects": (),
    }
