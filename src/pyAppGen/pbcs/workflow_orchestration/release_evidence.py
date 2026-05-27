"""Generated release evidence for the workflow_orchestration PBC."""

from __future__ import annotations

from .runtime import workflow_orchestration_build_release_evidence
from .schema_contract import build_schema_contract
from .service_contract import build_service_contract


RELEASE_EVIDENCE = {
    **workflow_orchestration_build_release_evidence(),
    "pbc": "workflow_orchestration",
}


def build_release_evidence() -> dict:
    """Return generated release audit evidence for this PBC."""
    evidence = dict(RELEASE_EVIDENCE)
    evidence.setdefault("schema", build_schema_contract())
    evidence.setdefault("service", build_service_contract())
    evidence.setdefault("pbc", "workflow_orchestration")
    return evidence


def release_readiness_manifest() -> dict:
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(name for name in ("schema", "service", "api", "permissions", "ui_binding", "events") if isinstance(evidence.get(name), dict))
    checks = tuple(evidence.get("checks", ()))
    return {
        "ok": evidence.get("ok") is True and bool(checks),
        "pbc": "workflow_orchestration",
        "format": evidence.get("format"),
        "sections": sections,
        "checks": checks,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "required_sections": ("schema", "service", "api", "permissions", "ui_binding"),
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    """Validate release evidence, blocking gaps, and owned-boundary proof."""
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["required_sections"] if section not in manifest["sections"])
    failed_checks = tuple(check for check in manifest["checks"] if check.get("ok") is not True)
    schema = evidence.get("schema", {}) if isinstance(evidence.get("schema"), dict) else {}
    service = evidence.get("service", {}) if isinstance(evidence.get("service"), dict) else {}
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", schema.get("shared_table_access") is not False),
            ("service_shared_table_access", service.get("shared_table_access") is True),
            ("service_missing_command_methods", not bool(service.get("command_methods"))),
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
        "pbc": "workflow_orchestration",
        "manifest": manifest,
        "missing_sections": missing_sections,
        "failed_checks": failed_checks,
        "boundary_gaps": boundary_gaps,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise release evidence readiness validation side-effect-free."""
    validation = validate_release_evidence()
    evidence = build_release_evidence()
    return {"ok": validation["ok"] and evidence.get("ok") is True, "validation": validation, "evidence": evidence, "side_effects": ()}
