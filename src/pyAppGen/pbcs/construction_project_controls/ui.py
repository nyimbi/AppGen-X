"""UI contracts for the construction_project_controls PBC."""
from __future__ import annotations

from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_EDGE_CASES,
    DOMAIN_OPERATIONS,
    DOMAIN_OWNED_TABLES,
    DOMAIN_PARAMETERS,
    DOMAIN_RULES,
    domain_capability_surface_contract,
)
from .runtime import (
    CONSTRUCTION_PROJECT_CONTROLS_UI_FRAGMENT_KEYS,
    construction_project_controls_build_controls_contract,
    construction_project_controls_build_forms_contract,
    construction_project_controls_build_wizards_contract,
    construction_project_controls_build_workbench_view,
)

PBC_KEY = "construction_project_controls"


def construction_project_controls_ui_contract():
    surface = domain_capability_surface_contract()
    forms = construction_project_controls_build_forms_contract()
    wizards = construction_project_controls_build_wizards_contract()
    controls = construction_project_controls_build_controls_contract()
    workbench = construction_project_controls_build_workbench_view()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": CONSTRUCTION_PROJECT_CONTROLS_UI_FRAGMENT_KEYS,
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": (
            "construction_project_controls.read",
            "construction_project_controls.create",
            "construction_project_controls.update",
            "construction_project_controls.approve",
            "construction_project_controls.admin",
        ),
        "forms": forms["forms"],
        "wizards": wizards["wizards"],
        "controls": controls["controls"],
        "workbench": workbench,
        "persona_tabs": (
            "schedule",
            "cost",
            "progress",
            "change",
            "risk_issues",
            "release_evidence",
        ),
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
                "forms",
                "wizards",
                "controls",
                "earned_value",
                "exceptions",
                "release_evidence",
            ),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def construction_project_controls_render_workbench():
    ui = construction_project_controls_ui_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": "/construction-project-controls-workbench",
        "views": ui["workbench"]["views"],
        "forms": tuple(form["name"] for form in ui["forms"]),
        "wizards": tuple(wizard["name"] for wizard in ui["wizards"]),
        "controls": tuple(control["name"] for control in ui["controls"]),
        "table_browsers": ui["full_capability_surface"]["table_browsers"],
        "side_effects": (),
    }


def smoke_test():
    return {
        "ok": construction_project_controls_ui_contract()["ok"]
        and construction_project_controls_render_workbench()["ok"],
        "side_effects": (),
    }
