"""UI fragments for the contract_lifecycle PBC."""

from .application import PBC_KEY, render_workbench, ui_contract
from .domain_depth import domain_capability_surface_contract, ui_capability_surface_contract


def contract_lifecycle_ui_contract():
    base = ui_contract()
    capability = ui_capability_surface_contract()
    return {
        **base,
        "ok": base["ok"] and capability["ok"],
        "configuration_editor": base.get("configuration_editor", {"event_contract": "AppGen-X"}),
        "stream_engine_picker_visible": False,
        "action_permissions": base.get("action_permissions", {}),
        "full_capability_surface": capability,
        "operation_actions": capability["operation_actions"],
        "rule_editors": capability["rule_editors"],
        "parameter_editors": capability["parameter_editors"],
        "advanced_panels": capability["advanced_panels"],
        "edge_case_queues": capability["edge_case_queues"],
        "table_browsers": capability["table_browsers"],
        "navigation_sections": capability["navigation_sections"],
    }


def contract_lifecycle_render_workbench(state=None):
    base = render_workbench(state)
    coverage = domain_capability_surface_contract()
    return {
        **base,
        "ok": base["ok"] and coverage["ok"],
        "pbc": PBC_KEY,
        "coverage": coverage,
    }


def smoke_test():
    contract = contract_lifecycle_ui_contract()
    workbench = contract_lifecycle_render_workbench()
    return {"ok": contract["ok"] and workbench["ok"], "contract": contract, "workbench": workbench}
