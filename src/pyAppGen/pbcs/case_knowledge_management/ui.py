"""UI fragments for the case_knowledge_management PBC."""

from __future__ import annotations

from .application import create_app
from .domain_depth import WORKBENCH_CONTROLS
from .domain_depth import WORKBENCH_FORMS
from .domain_depth import WORKBENCH_WIZARDS
from .domain_depth import ui_capability_surface_contract


PBC_KEY = "case_knowledge_management"
UI_FRAGMENTS = (
    "CaseKnowledgeManagementWorkbench",
    "CaseKnowledgeManagementDetail",
    "CaseKnowledgeManagementAssistantPanel",
)


def case_knowledge_management_ui_contract() -> dict:
    full = ui_capability_surface_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": UI_FRAGMENTS,
        "workbench_view": UI_FRAGMENTS[0],
        "configuration_editor": True,
        "forms": WORKBENCH_FORMS,
        "wizards": WORKBENCH_WIZARDS,
        "controls": WORKBENCH_CONTROLS,
        "action_permissions": (
            "case_knowledge_management.read",
            "case_knowledge_management.create",
            "case_knowledge_management.update",
            "case_knowledge_management.approve",
            "case_knowledge_management.admin",
        ),
        "stream_engine_picker_visible": False,
        "full_capability_surface": full,
        "operation_actions": full["operation_actions"],
        "rule_editors": full["rule_editors"],
        "parameter_editors": full["parameter_editors"],
        "advanced_panels": full["advanced_panels"],
        "table_browsers": full["table_browsers"],
        "navigation_sections": full["navigation_sections"],
        "side_effects": (),
    }


def case_knowledge_management_render_workbench(state: dict | None = None) -> dict:
    app = create_app(state)
    overview = app.query_workbench()
    full = ui_capability_surface_contract()
    return {
        "ok": overview["ok"],
        "pbc": PBC_KEY,
        "view": UI_FRAGMENTS[0],
        "panels": full["navigation_sections"],
        "configuration_editor": True,
        "forms": WORKBENCH_FORMS,
        "wizards": WORKBENCH_WIZARDS,
        "controls": WORKBENCH_CONTROLS,
        "records": overview["records"],
        "metrics": overview["metrics"],
        "operation_actions": full["operation_actions"],
        "advanced_panels": full["advanced_panels"],
        "table_browsers": full["table_browsers"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": case_knowledge_management_ui_contract()["ok"] and case_knowledge_management_render_workbench()["ok"],
        "side_effects": (),
    }


from .app_surface import (
    case_knowledge_management_controls_contract,
    case_knowledge_management_forms_contract,
    case_knowledge_management_wizards_contract,
    single_pbc_case_knowledge_management_app_contract,
)

_BASE_CASE_KNOWLEDGE_MANAGEMENT_UI_CONTRACT = case_knowledge_management_ui_contract
_BASE_CASE_KNOWLEDGE_MANAGEMENT_RENDER_WORKBENCH = case_knowledge_management_render_workbench

def case_knowledge_management_ui_contract() -> dict:
    base = dict(_BASE_CASE_KNOWLEDGE_MANAGEMENT_UI_CONTRACT())
    return {
        **base,
        'forms_contract': case_knowledge_management_forms_contract(),
        'wizards_contract': case_knowledge_management_wizards_contract(),
        'controls_contract': case_knowledge_management_controls_contract(),
        'single_pbc_app': single_pbc_case_knowledge_management_app_contract(),
    }

def case_knowledge_management_render_workbench(state: dict | None = None) -> dict:
    base = dict(_BASE_CASE_KNOWLEDGE_MANAGEMENT_RENDER_WORKBENCH(state=state))
    return {**base, 'single_pbc_app': single_pbc_case_knowledge_management_app_contract(state=state)}

def smoke_test() -> dict:
    contract = case_knowledge_management_ui_contract()
    workbench = case_knowledge_management_render_workbench()
    return {'ok': contract['ok'] and workbench['ok'] and contract['single_pbc_app']['ok'], 'contract': contract, 'workbench': workbench, 'side_effects': ()}
