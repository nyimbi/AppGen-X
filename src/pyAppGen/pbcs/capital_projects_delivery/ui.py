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
    CAPITAL_PROJECTS_DELIVERY_UI_FRAGMENT_KEYS,
    capital_projects_delivery_build_controls_contract,
    capital_projects_delivery_build_forms_contract,
    capital_projects_delivery_build_wizards_contract,
    capital_projects_delivery_build_workbench_view,
)

PBC_KEY = "capital_projects_delivery"


def capital_projects_delivery_ui_contract():
    surface = domain_capability_surface_contract()
    forms = capital_projects_delivery_build_forms_contract()
    wizards = capital_projects_delivery_build_wizards_contract()
    controls = capital_projects_delivery_build_controls_contract()
    workbench = capital_projects_delivery_build_workbench_view()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": CAPITAL_PROJECTS_DELIVERY_UI_FRAGMENT_KEYS,
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": (
            "capital_projects_delivery.read",
            "capital_projects_delivery.create",
            "capital_projects_delivery.update",
            "capital_projects_delivery.approve",
            "capital_projects_delivery.admin",
        ),
        "forms": forms["forms"],
        "wizards": wizards["wizards"],
        "controls": controls["controls"],
        "workbench": workbench,
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
                "operations",
                "edge_case_triage",
                "advanced_intelligence",
                "release_evidence",
            ),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def capital_projects_delivery_render_workbench():
    ui = capital_projects_delivery_ui_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "views": ui["workbench"]["views"],
        "forms": tuple(form["name"] for form in ui["forms"]),
        "wizards": tuple(wizard["name"] for wizard in ui["wizards"]),
        "controls": tuple(control["name"] for control in ui["controls"]),
        "table_browsers": ui["full_capability_surface"]["table_browsers"],
        "side_effects": (),
    }


def smoke_test():
    return {
        "ok": capital_projects_delivery_ui_contract()["ok"]
        and capital_projects_delivery_render_workbench()["ok"],
        "side_effects": (),
    }
