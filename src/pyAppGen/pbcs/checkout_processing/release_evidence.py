"""Generated release evidence for the checkout_processing PBC."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import controls
from . import forms
from . import ui
from . import wizards
from .runtime import checkout_processing_build_api_contract
from .runtime import checkout_processing_build_release_evidence
from .runtime import checkout_processing_build_schema_contract
from .runtime import checkout_processing_build_service_contract
from .runtime import checkout_processing_permissions_contract

PBC_KEY = "checkout_processing"
PACKAGE_DIR = Path(__file__).parent


def build_release_evidence() -> dict:
    """Return generated release audit evidence for this PBC."""
    runtime_evidence = checkout_processing_build_release_evidence()
    return {
        **runtime_evidence,
        "pbc": PBC_KEY,
        "schema": checkout_processing_build_schema_contract(),
        "service": checkout_processing_build_service_contract(),
        "api": checkout_processing_build_api_contract(),
        "permissions": checkout_processing_permissions_contract(),
        "ui": ui.checkout_processing_ui_contract(),
        "forms": forms.checkout_processing_form_catalog(),
        "wizards": wizards.checkout_processing_wizard_catalog(),
        "controls": controls.checkout_processing_control_catalog(),
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
        "required_sections": ("schema", "service", "api", "permissions", "ui", "forms", "wizards", "controls", "assistant"),
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
    finalization_commands = {"confirm_inventory_reservation", "authorize_payment_intent", "capture_payment_intent"}
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("schema_shared_table_access", schema.get("shared_table_access") is not False),
            ("service_shared_table_access", service.get("shared_table_access") is True),
            ("service_missing_finalization_commands", not finalization_commands <= set(service.get("command_methods", ()))),
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
    return {
        "ok": validation["ok"] and evidence.get("ok") is True,
        "validation": validation,
        "evidence": evidence,
        "side_effects": (),
    }



def _standalone_documentation_evidence() -> dict:
    docs = {
        "README.md": PACKAGE_DIR.joinpath("README.md").exists(),
        "SPECIFICATION.md": PACKAGE_DIR.joinpath("SPECIFICATION.md").exists(),
        "RELEASE_EVIDENCE.md": PACKAGE_DIR.joinpath("RELEASE_EVIDENCE.md").exists(),
        "repository.py": PACKAGE_DIR.joinpath("repository.py").exists(),
        "standalone.py": PACKAGE_DIR.joinpath("standalone.py").exists(),
    }
    return {"ok": all(docs.values()), "pbc": PBC_KEY, "artifacts": docs, "side_effects": ()}


_BASE_BUILD_RELEASE_EVIDENCE = build_release_evidence


def build_release_evidence() -> dict:
    """Return release evidence with standalone one-PBC app proof."""
    evidence = _BASE_BUILD_RELEASE_EVIDENCE()
    from . import standalone
    from .repository import standalone_repository_contract
    from .services import standalone_service_operation_contracts
    from .routes import standalone_route_contracts

    standalone_app = standalone.checkout_processing_standalone_app_contract()
    standalone_repo = standalone_repository_contract()
    standalone_services = standalone_service_operation_contracts()
    standalone_routes = standalone_route_contracts()
    docs = _standalone_documentation_evidence()
    ok = (
        evidence.get("ok") is True
        and standalone_app["ok"]
        and standalone_repo["ok"]
        and standalone_services["ok"]
        and standalone_routes["ok"]
        and docs["ok"]
    )
    return {
        **evidence,
        "ok": ok,
        "standalone_app": standalone_app,
        "standalone_repository": standalone_repo,
        "standalone_services": standalone_services,
        "standalone_routes": standalone_routes,
        "documentation": docs,
        "docs_present": {**evidence.get("docs_present", {}), **docs["artifacts"]},
    }


RELEASE_EVIDENCE = build_release_evidence()
