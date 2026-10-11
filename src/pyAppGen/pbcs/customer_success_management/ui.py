"""UI fragments for the customer_success_management PBC."""
from __future__ import annotations

from .domain_depth import ui_capability_surface_contract
from .slice_app import build_standalone_app, build_ui_contract

PBC_KEY = "customer_success_management"
UI_FRAGMENTS = tuple(build_ui_contract()["fragments"])


def customer_success_management_ui_contract() -> dict:
    contract = build_ui_contract()
    # The capability surface is derived from the domain-depth contract, so the
    # screens and the operations they invoke cannot drift apart.
    capability = ui_capability_surface_contract()
    return {
        **contract,
        "ok": contract["ok"] and capability["ok"],
        "stream_engine_picker_visible": False,
        "full_capability_surface": capability,
        "operation_actions": capability["operation_actions"],
        "rule_editors": capability["rule_editors"],
        "parameter_editors": capability["parameter_editors"],
        "advanced_panels": capability["advanced_panels"],
        "edge_case_queues": capability["edge_case_queues"],
        "table_browsers": capability["table_browsers"],
        "navigation_sections": capability["navigation_sections"],
    }


def customer_success_management_render_workbench(state: dict | None = None) -> dict:
    tenant = (state or {}).get("tenant", "default")
    app = build_standalone_app()
    workbench = app.build_workbench_view(tenant=tenant)
    capability = ui_capability_surface_contract()
    contract = customer_success_management_ui_contract()
    return {
        "ok": workbench["ok"] and capability["ok"],
        "pbc": PBC_KEY,
        "view": workbench["view"],
        "panels": tuple(dict.fromkeys(tuple(workbench["panels"]) + capability["navigation_sections"])),
        "forms": workbench["forms"],
        "wizards": workbench["wizards"],
        "controls": workbench["controls"],
        "summary": workbench["summary"],
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": tuple(contract["action_permissions"]),
        "advanced_panels": capability["advanced_panels"],
        "operation_actions": capability["operation_actions"],
        "edge_case_queues": capability["edge_case_queues"],
        "table_browsers": capability["table_browsers"],
        "agent_tools": capability["agent_tools"],
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
