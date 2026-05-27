"""Runtime-backed release evidence for the production_control PBC."""

from __future__ import annotations

from .runtime import production_control_build_api_contract
from .runtime import production_control_build_release_evidence
from .runtime import production_control_build_schema_contract
from .runtime import production_control_build_service_contract
from .runtime import production_control_permissions_contract

PBC_KEY = "production_control"


def build_release_evidence() -> dict:
    """Return generated release audit evidence for this PBC."""
    return {
        **production_control_build_release_evidence(),
        "pbc": PBC_KEY,
        "schema": production_control_build_schema_contract(),
        "service": production_control_build_service_contract(),
        "api": production_control_build_api_contract(),
        "permissions": production_control_permissions_contract(),
    }


RELEASE_EVIDENCE = build_release_evidence()


def release_readiness_manifest() -> dict:
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(name for name in ("schema", "service", "api", "permissions", "ui", "events") if isinstance(evidence.get(name), dict))
    checks = tuple(evidence.get("checks", ()))
    return {
        "ok": evidence.get("ok") is True and bool(checks),
        "pbc": PBC_KEY,
        "format": evidence.get("format"),
        "sections": sections,
        "checks": checks,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "required_sections": ("schema", "service", "api", "permissions"),
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
        "ok": manifest["ok"] and not manifest["blocking_gaps"] and not missing_sections and not failed_checks and not boundary_gaps,
        "pbc": PBC_KEY,
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
