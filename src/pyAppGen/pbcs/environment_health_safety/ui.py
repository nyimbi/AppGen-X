from __future__ import annotations

from .standalone import UI_FRAGMENT_KEYS, build_ui_contract, query_workbench, seed_state
from .domain_depth import domain_capability_surface_contract

PBC_KEY = "environment_health_safety"


def environment_health_safety_ui_contract():
    surface = domain_capability_surface_contract()
    contract = build_ui_contract()
    contract["full_capability_surface"] = {
        "operation_actions": tuple(item["operation"] for item in surface["operation_surfaces"]),
        "rule_editors": tuple(item["rule"] for item in surface["rule_surfaces"]),
        "parameter_editors": tuple(item["parameter"] for item in surface["parameter_surfaces"]),
        "advanced_panels": tuple(item["capability"] for item in surface["advanced_surfaces"]),
        "table_browsers": tuple(item["owned_table"] for item in surface["table_surfaces"]),
        "navigation_sections": contract["navigation_sections"],
        "coverage": surface["coverage"],
    }
    return contract


def environment_health_safety_render_workbench(state=None, tenant="tenant-seed"):
    workbench = query_workbench(state or seed_state(), {"tenant": tenant})
    return {"ok": True, "pbc": PBC_KEY, "route": f"/workbench/pbcs/{PBC_KEY}", "fragments": UI_FRAGMENT_KEYS, "queues": workbench["queues"], "metrics": workbench["metrics"], "side_effects": ()}


def smoke_test():
    return {"ok": environment_health_safety_ui_contract()["ok"] and environment_health_safety_render_workbench()["ok"], "side_effects": ()}
