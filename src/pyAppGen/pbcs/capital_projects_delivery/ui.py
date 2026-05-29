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
    capital_projects_delivery_build_workflow_contracts,
    capital_projects_delivery_permissions_contract,
    capital_projects_delivery_query_workbench,
)

PBC_KEY = "capital_projects_delivery"
ACTION_PERMISSIONS = {
    "view_workbench": f"{PBC_KEY}.read",
    "create_project": f"{PBC_KEY}.create",
    "update_gate_checklist": f"{PBC_KEY}.update",
    "approve_gate": f"{PBC_KEY}.approve",
    "configure_domain": f"{PBC_KEY}.admin",
}


def capital_projects_delivery_standalone_app_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "app_id": "capital_projects_delivery_one_pbc_app",
        "workbench_route": f"/workbench/pbcs/{PBC_KEY}",
        "navigation": (
            {"key": "overview", "route": f"/workbench/pbcs/{PBC_KEY}"},
            {"key": "approvals", "route": f"/workbench/pbcs/{PBC_KEY}/approvals"},
            {"key": "workflows", "route": f"/workbench/pbcs/{PBC_KEY}/workflows"},
            {"key": "assistant", "route": f"/workbench/pbcs/{PBC_KEY}/assistant"},
            {"key": "release", "route": f"/workbench/pbcs/{PBC_KEY}/release"},
        ),
        "forms": tuple(form["name"] for form in capital_projects_delivery_build_forms_contract()["forms"]),
        "wizards": tuple(wizard["name"] for wizard in capital_projects_delivery_build_wizards_contract()["wizards"]),
        "controls": tuple(control["name"] for control in capital_projects_delivery_build_controls_contract()["controls"]),
        "single_agent_namespace": f"{PBC_KEY}_skills",
        "side_effects": (),
    }


def capital_projects_delivery_ui_contract():
    surface = domain_capability_surface_contract()
    forms = capital_projects_delivery_build_forms_contract()
    wizards = capital_projects_delivery_build_wizards_contract()
    controls = capital_projects_delivery_build_controls_contract()
    workbench = capital_projects_delivery_build_workbench_view()
    workflows = capital_projects_delivery_build_workflow_contracts()
    shell = capital_projects_delivery_standalone_app_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": CAPITAL_PROJECTS_DELIVERY_UI_FRAGMENT_KEYS,
        "routes": tuple(item["route"] for item in shell["navigation"]),
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": ACTION_PERMISSIONS,
        "forms": forms["forms"],
        "wizards": wizards["wizards"],
        "controls": controls["controls"],
        "workflows": workflows["workflows"],
        "workbench": workbench,
        "standalone_app": shell,
        "permissions": capital_projects_delivery_permissions_contract(),
        "panels": (
            {
                "key": "overview",
                "fragment": "CapitalProjectsDeliveryWorkbench",
                "binds_to": ("capital_project", "permit_milestone", "project_risk"),
                "actions": ("command_capital_project", "record_gate_checklist", "approve_capital_project_gate"),
            },
            {
                "key": "detail",
                "fragment": "CapitalProjectsDeliveryDetail",
                "binds_to": ("capital_project",),
                "actions": ("get_capital_project_detail",),
            },
            {
                "key": "assistant",
                "fragment": "CapitalProjectsDeliveryAssistantPanel",
                "binds_to": ("document_instruction", "crud_plan", "workflow_plan"),
                "actions": ("parse_document_instruction", "build_agent_help_contract"),
            },
            {
                "key": "release",
                "fragment": "CapitalProjectGateApprovalWizard",
                "binds_to": DOMAIN_OWNED_TABLES,
                "actions": ("build_workflow_contracts", "build_single_pbc_app_contract"),
            },
        ),
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": DOMAIN_RULES,
            "parameter_editors": DOMAIN_PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES,
            "table_browsers": DOMAIN_OWNED_TABLES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "agent_tools": tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),
            "navigation_sections": tuple(item["key"] for item in shell["navigation"]),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def capital_projects_delivery_render_workbench(state=None, *, tenant="default", principal_permissions=None):
    ui = capital_projects_delivery_ui_contract()
    shell = capital_projects_delivery_standalone_app_contract()
    permissions = set(principal_permissions or tuple(ACTION_PERMISSIONS.values()))
    snapshot = capital_projects_delivery_query_workbench(state or {"records": {}}, {"tenant": tenant})
    visible_actions = tuple(action for action, permission in ACTION_PERMISSIONS.items() if permission in permissions)
    return {
        "ok": snapshot["ok"],
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": shell["workbench_route"],
        "views": ui["workbench"]["views"],
        "navigation": shell["navigation"],
        "forms": ui["forms"],
        "wizards": ui["wizards"],
        "controls": ui["controls"],
        "workflows": ui["workflows"],
        "summary_cards": (
            {"key": "projects", "value": snapshot["summary"]["project_count"]},
            {"key": "blocked", "value": snapshot["summary"]["blocked_projects"]},
            {"key": "ready", "value": snapshot["summary"]["ready_projects"]},
        ),
        "records": snapshot["records"],
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in ACTION_PERMISSIONS if action not in visible_actions),
        "table_browsers": ui["full_capability_surface"]["table_browsers"],
        "side_effects": (),
    }


def capital_projects_delivery_render_standalone_app(state=None, *, tenant="default", principal_permissions=None):
    workbench = capital_projects_delivery_render_workbench(state, tenant=tenant, principal_permissions=principal_permissions)
    return {
        "ok": workbench["ok"],
        "pbc": PBC_KEY,
        "shell": capital_projects_delivery_standalone_app_contract(),
        "workbench": workbench,
        "side_effects": (),
    }


def smoke_test():
    rendered = capital_projects_delivery_render_standalone_app({"records": {}}, tenant="tenant_smoke", principal_permissions=tuple(ACTION_PERMISSIONS.values()))
    return {
        "ok": capital_projects_delivery_ui_contract()["ok"] and capital_projects_delivery_render_workbench({"records": {}})["ok"] and rendered["ok"],
        "manifest": capital_projects_delivery_ui_contract(),
        "rendered": rendered["workbench"],
        "side_effects": (),
    }
