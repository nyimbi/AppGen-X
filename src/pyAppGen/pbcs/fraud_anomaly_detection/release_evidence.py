"""Generated release evidence for the fraud_anomaly_detection PBC."""

from __future__ import annotations

from .runtime import fraud_anomaly_detection_build_release_evidence

RELEASE_EVIDENCE = fraud_anomaly_detection_build_release_evidence()


def build_release_evidence():
    """Return generated release audit evidence for this PBC."""
    return dict(RELEASE_EVIDENCE)


def release_readiness_manifest():
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("schema", "service", "api", "permissions", "ui", "control")
        if isinstance(evidence.get(name), dict)
    )
    checks = tuple(evidence.get("checks", ()))
    return {
        "ok": evidence.get("ok") is True and bool(checks),
        "pbc": "fraud_anomaly_detection",
        "format": evidence.get("format"),
        "sections": sections,
        "checks": checks,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "required_sections": ("schema", "service", "api", "permissions", "ui", "control"),
        "side_effects": (),
    }


def validate_release_evidence():
    """Validate release evidence, blocking gaps, and owned-boundary proof."""
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["required_sections"] if section not in manifest["sections"])
    failed_checks = tuple(check for check in manifest["checks"] if check.get("ok") is not True)
    schema = evidence.get("schema", {}) if isinstance(evidence.get("schema"), dict) else {}
    service = evidence.get("service", {}) if isinstance(evidence.get("service"), dict) else {}
    control = evidence.get("control", {}) if isinstance(evidence.get("control"), dict) else {}
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", schema.get("shared_table_access") is not False),
            ("service_shared_table_access", service.get("shared_table_access") is True),
            ("service_missing_command_methods", not bool(service.get("command_methods"))),
            ("standard_table_runtime_population", control.get("workbench", {}).get("identity_link_count", 0) < 1),
        )
        if failed
    )
    return {
        "ok": manifest["ok"] and not missing_sections and not failed_checks and not boundary_gaps,
        "pbc": "fraud_anomaly_detection",
        "missing_sections": missing_sections,
        "failed_checks": failed_checks,
        "boundary_gaps": boundary_gaps,
        "side_effects": (),
    }


def smoke_test():
    validation = validate_release_evidence()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}
