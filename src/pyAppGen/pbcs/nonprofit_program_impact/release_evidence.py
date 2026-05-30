"""Generated release evidence for the nonprofit_program_impact PBC."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import controls
from . import forms
from . import standalone
from . import ui
from . import wizards
from .runtime import nonprofit_program_impact_build_api_contract
from .runtime import nonprofit_program_impact_build_release_evidence as runtime_build_release_evidence
from .runtime import nonprofit_program_impact_build_schema_contract
from .runtime import nonprofit_program_impact_build_service_contract
from .runtime import nonprofit_program_impact_permissions_contract


PBC_KEY = "nonprofit_program_impact"
PACKAGE_DIR = Path(__file__).parent
_REQUIRED_STANDALONE_METHODS = {
    "create_program",
    "enroll_beneficiary",
    "record_service_episode",
    "record_outcome_observation",
    "create_evidence_pack",
    "freeze_donor_report",
    "build_workbench",
    "build_beneficiary_timeline",
}


def build_release_evidence() -> dict:
    """Return generated release audit evidence for this PBC."""
    runtime_evidence = runtime_build_release_evidence()
    return {
        **runtime_evidence,
        "pbc": PBC_KEY,
        "schema": nonprofit_program_impact_build_schema_contract(),
        "service": nonprofit_program_impact_build_service_contract(),
        "api": nonprofit_program_impact_build_api_contract(),
        "permissions": nonprofit_program_impact_permissions_contract(),
        "ui": ui.nonprofit_program_impact_ui_contract(),
        "forms": forms.nonprofit_program_impact_form_catalog(),
        "wizards": wizards.nonprofit_program_impact_wizard_catalog(),
        "controls": controls.nonprofit_program_impact_control_catalog(),
        "assistant": agent.composed_agent_contribution(),
        "standalone": standalone.nonprofit_program_impact_standalone_app_contract(),
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
        for name in ("schema", "service", "api", "permissions", "ui", "forms", "wizards", "controls", "assistant", "standalone")
        if isinstance(evidence.get(name), dict)
    )
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
        "required_sections": ("schema", "service", "api", "permissions", "ui", "forms", "wizards", "controls", "assistant", "standalone"),
        "docs_present": docs_present,
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    """Validate release evidence, blocking gaps, and standalone boundary proof."""
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
    standalone_contract = evidence.get("standalone", {})
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", schema.get("shared_table_access") is not False),
            ("service_shared_table_access", service.get("shared_table_access") is True),
            ("missing_forms", not forms_catalog.get("ok")),
            ("missing_wizards", not wizard_catalog.get("ok")),
            ("missing_controls", not control_catalog.get("ok")),
            ("missing_assistant", not assistant.get("ok")),
            ("missing_standalone", not standalone_contract.get("ok")),
            (
                "standalone_missing_core_methods",
                not _REQUIRED_STANDALONE_METHODS <= set(standalone_contract.get("service_methods", ())),
            ),
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
