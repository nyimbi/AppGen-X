"""UI contracts for the court_case_management standalone slice."""
from __future__ import annotations

from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_EDGE_CASES, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES, DOMAIN_PARAMETERS, DOMAIN_RULES, domain_capability_surface_contract
from .court_operations_app import controls_contract, forms_contract, single_pbc_app_contract, wizards_contract

PBC_KEY = "court_case_management"
WORKBENCH_QUEUES = (
    "clerk_deficiency_queue",
    "accepted_filings",
    "evidence_review_queue",
    "chambers_order_review",
    "courtroom_calendar",
    "pending_tasks",
    "sealed_or_restricted_items",
    "open_cases",
)
DETAIL_SECTIONS = ("summary", "timeline", "parties", "filings", "evidence", "hearings", "orders", "tasks", "docket")


def court_case_management_ui_contract() -> dict:
    surface = domain_capability_surface_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": ("CourtCaseManagementWorkbench", "CourtCaseManagementDetail", "CourtCaseManagementAssistantPanel"),
        "forms": forms_contract()["forms"],
        "wizards": wizards_contract()["wizards"],
        "controls": controls_contract()["controls"],
        "single_pbc_app": single_pbc_app_contract(),
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": (
            "court_case_management.read",
            "court_case_management.create",
            "court_case_management.update",
            "court_case_management.approve",
            "court_case_management.admin",
        ),
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": DOMAIN_RULES,
            "parameter_editors": DOMAIN_PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES,
            "table_browsers": DOMAIN_OWNED_TABLES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "agent_tools": tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),
            "navigation_sections": ("overview", "operations", "intake", "calendar", "evidence", "tasks", "release_evidence"),
            "coverage": surface["coverage"],
        },
        "workbench_queues": WORKBENCH_QUEUES,
        "detail_sections": DETAIL_SECTIONS,
        "side_effects": (),
    }


def court_case_management_render_workbench() -> dict:
    ui_contract = court_case_management_ui_contract()
    full = ui_contract["full_capability_surface"]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "queues": WORKBENCH_QUEUES,
        "detail_sections": DETAIL_SECTIONS,
        "operation_actions": full["operation_actions"],
        "forms": ui_contract["forms"],
        "wizards": ui_contract["wizards"],
        "controls": ui_contract["controls"],
        "table_browsers": full["table_browsers"],
        "side_effects": (),
    }


def court_case_management_forms_contract() -> dict:
    return forms_contract()


def court_case_management_wizard_contract() -> dict:
    return wizards_contract()


def court_case_management_controls_contract() -> dict:
    return controls_contract()


def smoke_test() -> dict:
    rendered = court_case_management_render_workbench()
    return {"ok": court_case_management_ui_contract()["ok"] and rendered["ok"] and len(rendered["queues"]) >= 6, "side_effects": ()}
