"""UI contracts for the media_production_management PBC."""
from __future__ import annotations

from .controls import control_catalog
from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_EDGE_CASES,
    DOMAIN_OPERATIONS,
    DOMAIN_OWNED_TABLES,
    DOMAIN_PARAMETERS,
    DOMAIN_RULES,
    domain_capability_surface_contract,
)
from .forms import form_catalog
from .wizards import wizard_catalog

PBC_KEY = "media_production_management"


def media_production_management_ui_contract():
    surface = domain_capability_surface_contract()
    forms = form_catalog()
    wizards = wizard_catalog()
    controls = control_catalog()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": (
            "MediaProductionManagementWorkbench",
            "MediaProductionManagementDetail",
            "MediaProductionManagementAssistantPanel",
            "MediaProductionManagementSlateBoard",
            "MediaProductionManagementCallSheetConsole",
            "MediaProductionManagementPostDeliveryMatrix",
        ),
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": (
            "media_production_management.read",
            "media_production_management.create",
            "media_production_management.update",
            "media_production_management.approve",
            "media_production_management.admin",
        ),
        "role_boards": (
            "slate_and_development",
            "budget_control",
            "casting_and_crew",
            "schedule_and_call_sheets",
            "locations_and_safety",
            "daily_reports_and_dailies",
            "post_vfx_finishing",
            "rights_qc_deliverables",
            "exception_triage",
        ),
        "forms": forms["forms"],
        "wizards": wizards["wizards"],
        "controls": controls["controls"],
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": DOMAIN_RULES,
            "parameter_editors": DOMAIN_PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES,
            "table_browsers": DOMAIN_OWNED_TABLES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "agent_tools": tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),
            "navigation_sections": (
                "overview",
                "slate",
                "production_office",
                "shoot_day_control",
                "post_and_delivery",
                "edge_case_triage",
                "advanced_intelligence",
                "release_evidence",
            ),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def media_production_management_render_workbench():
    ui = media_production_management_ui_contract()
    full = ui["full_capability_surface"]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "role_boards": ui["role_boards"],
        "operation_actions": full["operation_actions"],
        "table_browsers": full["table_browsers"],
        "forms": tuple(form["id"] for form in ui["forms"]),
        "wizards": tuple(wizard["id"] for wizard in ui["wizards"]),
        "exception_queues": full["edge_case_queues"],
        "side_effects": (),
    }


def smoke_test():
    ui = media_production_management_ui_contract()
    workbench = media_production_management_render_workbench()
    return {
        "ok": ui["ok"] and workbench["ok"] and len(ui["forms"]) >= 8 and len(ui["wizards"]) >= 6,
        "side_effects": (),
    }
