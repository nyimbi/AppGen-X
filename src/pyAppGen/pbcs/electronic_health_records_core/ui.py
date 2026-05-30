"""Workbench, forms, wizards, and controls for electronic health records core."""
from __future__ import annotations

from .ehr_control import improve1_ehr_control_contract
from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_EDGE_CASES,
    DOMAIN_OPERATIONS,
    DOMAIN_OWNED_TABLES,
    DOMAIN_PARAMETERS,
    DOMAIN_RULES,
    domain_capability_surface_contract,
)
from .ehr_core_app import (
    ehr_core_controls_contract,
    ehr_core_forms_contract,
    ehr_core_wizards_contract,
    single_pbc_app_contract,
)

PBC_KEY = "electronic_health_records_core"


def electronic_health_records_core_ui_contract() -> dict:
    surface = domain_capability_surface_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": (
            "ElectronicHealthRecordsCoreWorkbench",
            "ElectronicHealthRecordsCoreDetail",
            "ElectronicHealthRecordsCoreAssistantPanel",
        ),
        "ehr_control_contract": improve1_ehr_control_contract(),
        "forms": ehr_core_forms_contract()["forms"],
        "wizards": ehr_core_wizards_contract()["wizards"],
        "controls": ehr_core_controls_contract()["controls"],
        "single_pbc_app": single_pbc_app_contract(),
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": (
            "electronic_health_records_core.read",
            "electronic_health_records_core.create",
            "electronic_health_records_core.update",
            "electronic_health_records_core.approve",
            "electronic_health_records_core.admin",
        ),
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": DOMAIN_RULES,
            "parameter_editors": DOMAIN_PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES,
            "table_browsers": DOMAIN_OWNED_TABLES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "agent_tools": tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),
            "ehr_control_panels": tuple(item["ui_surface"] for item in improve1_ehr_control_contract()["capabilities"]),
            "navigation_sections": ("overview", "operations", "edge_case_triage", "advanced_intelligence", "release_evidence"),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def electronic_health_records_core_render_workbench() -> dict:
    ui = electronic_health_records_core_ui_contract()
    full = ui["full_capability_surface"]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "queues": (
            "duplicate_chart_reviews",
            "incomplete_encounters",
            "pending_orders",
            "critical_results",
            "medication_reconciliation_needed",
            "unsigned_notes",
            "summary_redaction_requests",
            "control_failures",
        ),
        "operation_actions": full["operation_actions"],
        "forms": ui["forms"],
        "wizards": ui["wizards"],
        "controls": ui["controls"],
        "table_browsers": full["table_browsers"],
        "side_effects": (),
    }


def electronic_health_records_core_forms_contract() -> dict:
    return ehr_core_forms_contract()


def electronic_health_records_core_wizard_contract() -> dict:
    return ehr_core_wizards_contract()


def electronic_health_records_core_controls_contract() -> dict:
    return ehr_core_controls_contract()


def smoke_test() -> dict:
    return {
        "ok": electronic_health_records_core_ui_contract()["ok"] and electronic_health_records_core_render_workbench()["ok"],
        "side_effects": (),
    }
