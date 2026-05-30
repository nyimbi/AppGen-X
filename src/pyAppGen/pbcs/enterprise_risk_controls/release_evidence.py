"""Release evidence for the enterprise_risk_controls PBC."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import config
from . import controls
from . import forms
from . import handlers
from . import routes
from . import ui
from . import wizards
from .events import event_contract_manifest
from .permissions import permission_manifest
from .runtime import enterprise_risk_controls_build_schema_contract
from .runtime import enterprise_risk_controls_build_release_evidence
from .service_contract import build_service_contract

PBC_KEY = "enterprise_risk_controls"
PACKAGE_DIR = Path(__file__).parent


def build_release_evidence() -> dict:
    runtime_evidence = enterprise_risk_controls_build_release_evidence()
    return {
        **runtime_evidence,
        "pbc": PBC_KEY,
        "schema": enterprise_risk_controls_build_schema_contract(),
        "service": build_service_contract(),
        "api": routes.api_route_contracts(),
        "events": event_contract_manifest(),
        "handlers": handlers.handler_manifest(),
        "permissions": permission_manifest(),
        "config": config.configuration_manifest(),
        "ui": ui.enterprise_risk_controls_ui_contract(),
        "forms": forms.enterprise_risk_controls_form_catalog(),
        "wizards": wizards.enterprise_risk_controls_wizard_catalog(),
        "controls": controls.enterprise_risk_controls_control_catalog(),
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
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in (
            "schema",
            "service",
            "api",
            "events",
            "handlers",
            "permissions",
            "config",
            "ui",
            "forms",
            "wizards",
            "controls",
            "assistant",
        )
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
        "required_sections": (
            "schema",
            "service",
            "api",
            "events",
            "handlers",
            "permissions",
            "config",
            "ui",
            "forms",
            "wizards",
            "controls",
            "assistant",
        ),
        "docs_present": docs_present,
        "side_effects": (),
    }


def validate_release_evidence() -> dict:
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest["required_sections"] if section not in manifest["sections"])
    failed_checks = tuple(check for check in manifest["checks"] if check.get("ok") is not True)
    service = evidence.get("service", {})
    forms_catalog = evidence.get("forms", {})
    wizard_catalog = evidence.get("wizards", {})
    control_catalog = evidence.get("controls", {})
    assistant = evidence.get("assistant", {})
    required_commands = {
        "register_risk",
        "assess_inherent_risk",
        "define_control",
        "schedule_control_test",
        "record_attestation",
        "open_remediation",
        "generate_assurance_packet",
    }
    required_queries = {
        "query_enterprise_risk_controls_workbench",
        "query_enterprise_risk_controls_controls",
        "query_enterprise_risk_controls_assistant_preview",
    }
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ("service_shared_table_access", service.get("shared_table_access") is True),
            ("service_missing_commands", not required_commands <= set(service.get("command_methods", ()))),
            ("service_missing_queries", not required_queries <= set(service.get("query_methods", ()))),
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
    validation = validate_release_evidence()
    evidence = build_release_evidence()
    return {
        "ok": validation["ok"] and evidence.get("ok") is True,
        "validation": validation,
        "evidence": evidence,
        "side_effects": (),
    }
