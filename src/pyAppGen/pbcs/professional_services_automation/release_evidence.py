"""Generated release evidence for the professional_services_automation PBC."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import controls
from . import forms
from . import standalone
from . import ui
from . import wizards
from .runtime import professional_services_automation_build_api_contract
from .runtime import professional_services_automation_build_release_evidence as runtime_build_release_evidence
from .runtime import professional_services_automation_build_schema_contract
from .runtime import professional_services_automation_build_service_contract
from .runtime import professional_services_automation_permissions_contract


PBC_KEY = "professional_services_automation"
PACKAGE_DIR = Path(__file__).parent



def build_release_evidence() -> dict:
    """Return generated release audit evidence for this PBC."""
    runtime_evidence = runtime_build_release_evidence()
    return {
        **runtime_evidence,
        "pbc": PBC_KEY,
        "schema": professional_services_automation_build_schema_contract(),
        "service": professional_services_automation_build_service_contract(),
        "api": professional_services_automation_build_api_contract(),
        "permissions": professional_services_automation_permissions_contract(),
        "ui": ui.professional_services_automation_ui_contract(),
        "forms": forms.professional_services_automation_form_catalog(),
        "wizards": wizards.professional_services_automation_wizard_catalog(),
        "controls": controls.professional_services_automation_control_catalog(),
        "assistant": agent.composed_agent_contribution(),
        "standalone_app": standalone.professional_services_automation_standalone_app_contract(),
        "documentation": {
            "README.md": PACKAGE_DIR.joinpath("README.md").exists(),
            "implementation-plan.md": PACKAGE_DIR.joinpath("implementation-plan.md").exists(),
            "implementation-status.md": PACKAGE_DIR.joinpath("implementation-status.md").exists(),
            "RELEASE_EVIDENCE.md": PACKAGE_DIR.joinpath("RELEASE_EVIDENCE.md").exists(),
        },
    }


RELEASE_EVIDENCE = build_release_evidence()



def release_readiness_manifest() -> dict:
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
            "forms",
            "wizards",
            "controls",
            "assistant",
            "standalone_app",
        )
        if isinstance(evidence.get(name), dict)
    )
    checks = tuple(evidence.get("checks", ()))
    docs_present = evidence.get("documentation", {})
    blocking_gaps = tuple(evidence.get("blocking_gaps", ())) + tuple(
        name for name, present in docs_present.items() if not present
    )
    return {
        "ok": evidence.get("ok") is True and bool(checks) and not blocking_gaps,
        "pbc": PBC_KEY,
        "format": evidence.get("format"),
        "sections": sections,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "required_sections": (
            "schema",
            "service",
            "api",
            "permissions",
            "ui",
            "forms",
            "wizards",
            "controls",
            "assistant",
            "standalone_app",
        ),
        "documentation": docs_present,
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
    forms_catalog = evidence.get("forms", {})
    wizard_catalog = evidence.get("wizards", {})
    control_catalog = evidence.get("controls", {})
    assistant = evidence.get("assistant", {})
    standalone_app = evidence.get("standalone_app", {})
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", schema.get("shared_table_access") is not False),
            ("service_shared_table_access", service.get("shared_table_access") is True),
            ("missing_forms", not forms_catalog.get("ok")),
            ("missing_wizards", not wizard_catalog.get("ok")),
            ("missing_controls", not control_catalog.get("ok")),
            ("missing_assistant", not assistant.get("ok")),
            ("missing_standalone_app", not standalone_app.get("ok")),
        )
        if failed
    )
    return {
        "ok": manifest["ok"]
        and evidence.get("pbc", PBC_KEY) == manifest["pbc"]
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



def professional_services_automation_build_release_evidence() -> dict:
    return build_release_evidence()



def smoke_test() -> dict:
    """Exercise release evidence readiness validation side-effect-free."""
    validation = validate_release_evidence()
    evidence = build_release_evidence()
    return {
        "ok": validation["ok"] and evidence.get("ok") is True,
        "validation": validation,
        "evidence": evidence,
        "side_effects": (),
    }
