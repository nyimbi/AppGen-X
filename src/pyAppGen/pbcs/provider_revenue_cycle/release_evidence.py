"""Generated release evidence for the provider_revenue_cycle PBC."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import audit
from . import controls
from . import forms
from . import routes
from . import services
from . import standalone
from . import ui
from . import wizards
from .runtime import provider_revenue_cycle_build_api_contract
from .runtime import provider_revenue_cycle_build_release_evidence as runtime_build_release_evidence
from .runtime import provider_revenue_cycle_build_schema_contract
from .runtime import provider_revenue_cycle_build_service_contract
from .runtime import provider_revenue_cycle_permissions_contract

PBC_KEY = "provider_revenue_cycle"
PACKAGE_DIR = Path(__file__).parent


def build_release_evidence() -> dict:
    runtime_evidence = runtime_build_release_evidence()
    documentation = tuple(
        {"path": name, "exists": PACKAGE_DIR.joinpath(name).exists()}
        for name in ("SPECIFICATION.md", "improve1.md", "RELEASE_EVIDENCE.md")
    )
    checks = tuple(runtime_evidence.get("checks", ())) + (
        {"id": "forms_present", "ok": forms.provider_revenue_cycle_form_catalog()["ok"]},
        {"id": "wizards_present", "ok": wizards.provider_revenue_cycle_wizard_catalog()["ok"]},
        {"id": "controls_present", "ok": controls.provider_revenue_cycle_control_catalog()["ok"]},
        {"id": "standalone_application", "ok": standalone.standalone_manifest()["ok"]},
        {"id": "package_audit", "ok": audit.run_provider_revenue_cycle_pbc_audit()["ok"]},
        {"id": "documentation_present", "ok": all(item["exists"] for item in documentation)},
    )
    return {
        **runtime_evidence,
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "schema": provider_revenue_cycle_build_schema_contract(),
        "service": {
            **provider_revenue_cycle_build_service_contract(),
            "descriptor_surface": services.service_operation_manifest(),
            "standalone_surface": services.standalone_service_manifest(),
            "shared_table_access": False,
        },
        "api": {
            **provider_revenue_cycle_build_api_contract(),
            "route_contracts": routes.api_route_contracts(),
            "shared_table_access": False,
        },
        "permissions": provider_revenue_cycle_permissions_contract(),
        "ui": ui.provider_revenue_cycle_ui_contract(),
        "forms": forms.provider_revenue_cycle_form_catalog(),
        "wizards": wizards.provider_revenue_cycle_wizard_catalog(),
        "controls": controls.provider_revenue_cycle_control_catalog(),
        "assistant": agent.composed_agent_contribution(),
        "standalone": standalone.standalone_manifest(),
        "documentation": documentation,
        "audit": audit.run_provider_revenue_cycle_pbc_audit(),
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


RELEASE_EVIDENCE = build_release_evidence()


def release_readiness_manifest() -> dict:
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in (
            "schema",
            "service",
            "api",
            "permissions",
            "ui",
            "forms",
            "wizards",
            "controls",
            "assistant",
            "standalone",
            "documentation",
            "audit",
        )
        if isinstance(evidence.get(name), (dict, tuple))
    )
    checks = tuple(evidence.get("checks", ()))
    return {
        "ok": evidence.get("ok") is True and bool(checks),
        "pbc": PBC_KEY,
        "format": evidence.get("format"),
        "sections": sections,
        "checks": checks,
        "blocking_gaps": tuple(evidence.get("blocking_gaps", ())),
        "required_sections": ("schema", "service", "api", "permissions", "ui", "forms", "wizards", "controls", "assistant", "standalone", "audit"),
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["required_sections"] if section not in manifest["sections"])
    failed_checks = tuple(check for check in manifest["checks"] if check.get("ok") is not True)
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("missing_forms", not evidence.get("forms", {}).get("ok")),
            ("missing_wizards", not evidence.get("wizards", {}).get("ok")),
            ("missing_controls", not evidence.get("controls", {}).get("ok")),
            ("missing_assistant", not evidence.get("assistant", {}).get("ok")),
            ("missing_standalone", not evidence.get("standalone", {}).get("ok")),
            ("api_contract_invalid", not evidence.get("api", {}).get("ok")),
            ("service_shared_table_access", evidence.get("service", {}).get("shared_table_access") is True),
        )
        if failed
    )
    return {
        "ok": manifest["ok"]
        and evidence.get("pbc") == manifest["pbc"]
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


def smoke_test() -> dict:
    validation = validate_release_evidence()
    evidence = build_release_evidence()
    return {"ok": validation["ok"] and evidence.get("ok") is True, "validation": validation, "evidence": evidence, "side_effects": ()}
