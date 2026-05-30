"""UI and workbench contracts for defense_readiness_logistics."""

from __future__ import annotations

from .defense_control import improve1_defense_control_contract
from .defense_app import controls_contract, forms_contract, single_pbc_app_contract, workflow_contracts, wizards_contract
from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_EDGE_CASES,
    DOMAIN_OPERATIONS,
    DOMAIN_OWNED_TABLES,
    DOMAIN_PARAMETERS,
    DOMAIN_RULES,
    domain_capability_surface_contract,
)
from .models import PBC_KEY


def defense_readiness_logistics_ui_contract() -> dict:
    surface = domain_capability_surface_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": ("DefenseReadinessLogisticsWorkbench", "DefenseReadinessLogisticsDetail", "DefenseReadinessLogisticsAssistantPanel"),
        "forms": forms_contract()["forms"],
        "wizards": wizards_contract()["wizards"],
        "controls": controls_contract()["controls"],
        "workflows": workflow_contracts()["workflows"],
        "single_pbc_app": single_pbc_app_contract(),
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "defense_control_contract": improve1_defense_control_contract(),
        "action_permissions": (
            f"{PBC_KEY}.read",
            f"{PBC_KEY}.create",
            f"{PBC_KEY}.update",
            f"{PBC_KEY}.approve",
            f"{PBC_KEY}.admin",
        ),
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": DOMAIN_RULES,
            "parameter_editors": DOMAIN_PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES,
            "table_browsers": DOMAIN_OWNED_TABLES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "agent_tools": tuple(f"{PBC_KEY}_skills.{name}" for name in DOMAIN_OPERATIONS),
            "navigation_sections": ("overview", "operations", "workflows", "edge_case_triage", "advanced_intelligence", "release_evidence"),
            "defense_control_panels": tuple(item["ui_surface"] for item in improve1_defense_control_contract()["capabilities"]),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def defense_readiness_logistics_render_workbench() -> dict:
    ui = defense_readiness_logistics_ui_contract()
    full = ui["full_capability_surface"]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "queues": (
            "commander_readiness_board",
            "maintenance_control",
            "supply_readiness",
            "movement_control",
            "classified_export_review",
            "exception_backlog",
        ),
        "operation_actions": full["operation_actions"],
        "forms": ui["forms"],
        "wizards": ui["wizards"],
        "controls": ui["controls"],
        "workflows": ui["workflows"],
        "table_browsers": full["table_browsers"],
        "side_effects": (),
    }


def defense_readiness_logistics_forms_contract() -> dict:
    return forms_contract()


def defense_readiness_logistics_wizards_contract() -> dict:
    return wizards_contract()


def defense_readiness_logistics_controls_contract() -> dict:
    return controls_contract()


def smoke_test() -> dict:
    return {
        "ok": defense_readiness_logistics_ui_contract()["ok"] and defense_readiness_logistics_render_workbench()["ok"],
        "side_effects": (),
    }
