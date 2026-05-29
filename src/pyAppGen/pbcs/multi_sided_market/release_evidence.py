"""Release evidence facade for the multi_sided_market PBC."""

from __future__ import annotations

from .runtime import multi_sided_market_build_api_contract
from .runtime import multi_sided_market_build_release_evidence
from .runtime import multi_sided_market_build_schema_contract
from .runtime import multi_sided_market_build_service_contract
from .runtime import multi_sided_market_permissions_contract
from .app_surface import app_surface_smoke_test, single_pbc_multi_sided_market_app_contract

PBC_KEY = "multi_sided_market"

RELEASE_EVIDENCE = {
    **multi_sided_market_build_release_evidence(),
    "pbc": PBC_KEY,
    "schema": multi_sided_market_build_schema_contract(),
    "service": multi_sided_market_build_service_contract(),
    "api": multi_sided_market_build_api_contract(),
    "permissions": multi_sided_market_permissions_contract(),
}


def build_release_evidence():
    evidence = dict(RELEASE_EVIDENCE)
    standalone_app = single_pbc_multi_sided_market_app_contract()
    standalone_smoke = app_surface_smoke_test()
    evidence["standalone_app"] = standalone_app
    evidence["standalone_app_smoke"] = standalone_smoke
    evidence["checks"] = tuple(evidence.get("checks", ())) + ({"id": "standalone_forms_wizards_controls", "ok": standalone_smoke["ok"]},)
    return evidence


def release_readiness_manifest():
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in ("schema", "service", "api", "permissions", "ui", "events", "control", "standalone_app", "standalone_app_smoke")
        if isinstance(evidence.get(name), dict)
    )
    checks = tuple(evidence.get("checks", ()))
    return {
        "ok": evidence["ok"] and bool(checks),
        "pbc": PBC_KEY,
        "sections": sections,
        "checks": checks,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "required_sections": ("schema", "service", "api", "permissions", "standalone_app"),
        "side_effects": (),
    }


def validate_release_evidence():
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["required_sections"] if section not in manifest["sections"])
    failed_checks = tuple(check for check in manifest["checks"] if check.get("ok") is not True)
    schema = evidence.get("schema", {}) if isinstance(evidence.get("schema"), dict) else {}
    service = evidence.get("service", {}) if isinstance(evidence.get("service"), dict) else {}
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
        and evidence.get("pbc") == PBC_KEY
        and not manifest["blocking_gaps"]
        and not missing_sections
        and not failed_checks
        and not boundary_gaps,
        "pbc": PBC_KEY,
        "manifest": manifest,
        "missing_sections": missing_sections,
        "failed_checks": failed_checks,
        "boundary_gaps": boundary_gaps,
        "side_effects": (),
    }


def smoke_test():
    validation = validate_release_evidence()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}
