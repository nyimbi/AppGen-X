"""Generated release evidence for the clinical_trials_management PBC."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import controls
from . import forms
from . import ui
from . import wizards
from .runtime import clinical_trials_management_build_api_contract
from .runtime import clinical_trials_management_build_release_evidence as runtime_build_release_evidence
from .runtime import clinical_trials_management_build_schema_contract
from .runtime import clinical_trials_management_build_service_contract
from .runtime import clinical_trials_management_permissions_contract
from .standalone import standalone_smoke_test

PBC_KEY = "clinical_trials_management"
PACKAGE_DIR = Path(__file__).parent


def build_release_evidence() -> dict:
    """Return generated release audit evidence for this PBC."""
    runtime_evidence = runtime_build_release_evidence()
    standalone = standalone_smoke_test()
    checks = tuple(runtime_evidence.get("checks", ())) + ({"id": "standalone_one_pbc_app", "ok": standalone["ok"]},)
    return {
        **runtime_evidence,
        "checks": checks,
        "standalone_app_ok": standalone["ok"],
        "pbc": PBC_KEY,
        "schema": clinical_trials_management_build_schema_contract(),
        "service": clinical_trials_management_build_service_contract(),
        "api": clinical_trials_management_build_api_contract(),
        "permissions": clinical_trials_management_permissions_contract(),
        "ui": ui.clinical_trials_management_ui_contract(),
        "forms": forms.clinical_trials_management_form_catalog(),
        "wizards": wizards.clinical_trials_management_wizard_catalog(),
        "controls": controls.clinical_trials_management_control_catalog(),
        "assistant": agent.composed_agent_contribution(),
        "docs_present": {
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
        for name in ("schema", "service", "api", "permissions", "ui", "forms", "wizards", "controls", "assistant")
        if isinstance(evidence.get(name), dict)
    ) + (("standalone_app",) if evidence.get("standalone_app_ok") is True else ())
    checks = tuple(evidence.get("checks", ()))
    docs_present = evidence.get("docs_present", {})
    blocking_gaps = tuple(evidence.get("blocking_gaps", ())) + tuple(name for name, present in docs_present.items() if not present)
    return {
        "ok": evidence.get("ok") is True and bool(checks) and not blocking_gaps,
        "pbc": PBC_KEY,
        "format": evidence.get("format"),
        "sections": sections,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "required_sections": ("schema", "service", "api", "permissions", "ui", "forms", "wizards", "controls", "assistant", "standalone_app"),
        "docs_present": docs_present,
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
    required_commands = {"command_subjects", "command_consent_records", "command_adverse_events", "command_monitoring_findings"}
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", schema.get("shared_table_access") is not False),
            ("service_shared_table_access", service.get("shared_table_access") is True),
            ("service_missing_clinical_commands", not required_commands <= set(service.get("command_methods", ()))),
            ("missing_forms", not forms_catalog.get("ok")),
            ("missing_wizards", not wizard_catalog.get("ok")),
            ("missing_controls", not control_catalog.get("ok")),
            ("missing_assistant", not assistant.get("ok")),
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


def smoke_test() -> dict:
    """Exercise release evidence readiness validation side-effect-free."""
    validation = validate_release_evidence()
    evidence = build_release_evidence()
    return {"ok": validation["ok"] and evidence.get("ok") is True, "validation": validation, "evidence": evidence, "side_effects": ()}
