"""Generated release evidence for the predictive_demand PBC."""

from __future__ import annotations

from .runtime import predictive_demand_build_release_evidence
from .app_surface import app_surface_smoke_test
from .app_surface import single_pbc_predictive_demand_app_contract

RELEASE_EVIDENCE = predictive_demand_build_release_evidence()


def build_release_evidence():
    """Return generated release audit evidence for this PBC."""
    evidence = dict(RELEASE_EVIDENCE)
    standalone_app = single_pbc_predictive_demand_app_contract()
    standalone_smoke = app_surface_smoke_test()
    evidence["standalone_app"] = standalone_app
    evidence["standalone_app_smoke"] = standalone_smoke
    evidence["checks"] = tuple(evidence.get("checks", ())) + ({"id": "standalone_forms_wizards_controls", "ok": standalone_smoke["ok"]},)
    return evidence


def release_readiness_manifest():
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    section_keys = {
        "schema": "schema_contract",
        "service": "service_contract",
        "api": "api_contract",
        "permissions": "permissions_contract",
        "ui": "ui_contract",
        "standalone_app": "standalone_app",
        "standalone_app_smoke": "standalone_app_smoke",
    }
    sections = tuple(
        name
        for name, key in section_keys.items()
        if isinstance(evidence.get(key), dict)
    )
    checks = tuple(evidence.get("checks", ()))
    return {
        "ok": evidence.get("ok") is True and bool(checks),
        "pbc": "predictive_demand",
        "format": evidence.get("format"),
        "sections": sections,
        "checks": checks,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "required_sections": ("schema", "service", "api", "permissions", "ui", "standalone_app"),
        "side_effects": (),
    }


def validate_release_evidence():
    """Validate release evidence, blocking gaps, and owned-boundary proof."""
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(
        section for section in manifest["required_sections"] if section not in manifest["sections"]
    )
    failed_checks = tuple(check for check in manifest["checks"] if check.get("ok") is not True)
    schema = (
        evidence.get("schema_contract", {})
        if isinstance(evidence.get("schema_contract"), dict)
        else {}
    )
    service = (
        evidence.get("service_contract", {})
        if isinstance(evidence.get("service_contract"), dict)
        else {}
    )
    standalone_app = evidence.get("standalone_app", {}) if isinstance(evidence.get("standalone_app"), dict) else {}
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", schema.get("shared_table_access") is not False),
            ("service_shared_table_access", service.get("shared_table_access") is True),
            ("service_missing_command_methods", not bool(service.get("command_methods"))),
            ("standalone_app_not_database_backed", standalone_app.get("database_backed") is not True),
            ("standalone_app_missing_forms", not bool(standalone_app.get("forms"))),
            ("standalone_app_missing_wizards", not bool(standalone_app.get("wizards"))),
            ("standalone_app_missing_controls", not bool(standalone_app.get("controls"))),
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
        "pbc": "predictive_demand",
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
