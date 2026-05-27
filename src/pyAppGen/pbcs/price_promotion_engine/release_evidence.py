"""Generated release evidence for the price_promotion_engine PBC."""

from __future__ import annotations

from .runtime import price_promotion_engine_build_release_evidence


RELEASE_EVIDENCE = price_promotion_engine_build_release_evidence()


def build_release_evidence():
    """Return generated release audit evidence for this PBC."""
    return dict(RELEASE_EVIDENCE)


def release_readiness_manifest():
    """Return side-effect-free release evidence coverage and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("schema", "service", "api", "permissions", "ui_contract", "rendered_workbench", "workbench", "runtime_smoke")
        if isinstance(evidence.get(name), dict)
    )
    checks = tuple(evidence.get("checks", ()))
    return {
        "ok": evidence.get("ok") is True and bool(checks),
        "pbc": "price_promotion_engine",
        "format": evidence.get("format"),
        "sections": sections,
        "checks": checks,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "required_sections": ("schema", "service", "api", "permissions", "workbench", "runtime_smoke"),
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
    workbench = evidence.get("workbench", {}) if isinstance(evidence.get("workbench"), dict) else {}
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", schema.get("shared_table_access") is not False),
            ("service_shared_table_access", service.get("shared_table_access") is True),
            ("service_missing_approval_redemption_commands", not {"approve_promotion", "redeem_coupon"} <= set(service.get("command_methods", ()))),
            ("workbench_missing_coupon_redemption", int(workbench.get("coupon_redemption_count", 0)) < 1),
            ("workbench_missing_approved_promotion", int(workbench.get("approved_promotion_count", 0)) < 1),
        )
        if failed
    )
    return {
        "ok": manifest["ok"]
        and evidence.get("pbc", "price_promotion_engine") == manifest["pbc"]
        and not manifest["blocking_gaps"]
        and not missing_sections
        and not failed_checks
        and not boundary_gaps,
        "pbc": "price_promotion_engine",
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
