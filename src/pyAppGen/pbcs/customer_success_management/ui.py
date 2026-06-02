"""UI fragments for the customer_success_management PBC."""
from __future__ import annotations

from .domain_depth import DOMAIN_OPERATIONS, DOMAIN_PARAMETERS, DOMAIN_RULES
from .slice_app import BUSINESS_TABLES, build_standalone_app, build_ui_contract

PBC_KEY = "customer_success_management"
UI_FRAGMENTS = tuple(build_ui_contract()["fragments"])


def customer_success_management_ui_contract() -> dict:
    contract = build_ui_contract()
    return {
        **contract,
        "stream_engine_picker_visible": False,
        "full_capability_surface": {
            "operation_actions": tuple(DOMAIN_OPERATIONS),
            "rule_editors": tuple(DOMAIN_RULES),
            "parameter_editors": tuple(DOMAIN_PARAMETERS),
            "advanced_panels": tuple(contract["advanced_panels"]),
            "edge_case_queues": ("duplicate_submission", "policy_conflict", "idempotency_replay"),
            "table_browsers": tuple(BUSINESS_TABLES),
            "navigation_sections": (
                "command_center",
                "accounts",
                "health_cockpit",
                "playbook_board",
                "renewal_room",
                "agent_assistant",
                "release_evidence",
            ),
        },
        "operation_actions": tuple(DOMAIN_OPERATIONS),
        "rule_editors": tuple(DOMAIN_RULES),
        "parameter_editors": tuple(DOMAIN_PARAMETERS),
        "edge_case_queues": ("duplicate_submission", "policy_conflict", "idempotency_replay"),
        "table_browsers": tuple(BUSINESS_TABLES),
        "navigation_sections": (
            "command_center",
            "accounts",
            "health_cockpit",
            "playbook_board",
            "renewal_room",
            "agent_assistant",
            "release_evidence",
        ),
    }


def customer_success_management_render_workbench(state: dict | None = None) -> dict:
    tenant = (state or {}).get("tenant", "default")
    app = build_standalone_app()
    workbench = app.build_workbench_view(tenant=tenant)
    return {
        "ok": workbench["ok"],
        "pbc": PBC_KEY,
        "view": workbench["view"],
        "panels": workbench["panels"],
        "forms": workbench["forms"],
        "wizards": workbench["wizards"],
        "controls": workbench["controls"],
        "summary": workbench["summary"],
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": tuple(customer_success_management_ui_contract()["action_permissions"]),
        "advanced_panels": tuple(customer_success_management_ui_contract()["advanced_panels"]),
        "agent_tools": (
            "customer_success_management_plan_document_changes",
            "customer_success_management_preview_mutation",
        ),
        "side_effects": (),
    }


def smoke_test() -> dict:
    contract = customer_success_management_ui_contract()
    workbench = customer_success_management_render_workbench({"tenant": "tenant-smoke"})
    return {
        "ok": contract["ok"] and workbench["ok"] and bool(workbench["forms"]) and bool(workbench["wizards"]) and bool(workbench["controls"]),
        "contract": contract,
        "workbench": workbench,
        "side_effects": (),
    }
