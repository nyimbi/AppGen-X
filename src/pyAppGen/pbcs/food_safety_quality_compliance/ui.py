from .slice_app import build_app_surface
from .slice_app import build_ui_contract
from .slice_app import domain_capability_surface_contract
from .slice_app import PBC_KEY


def food_safety_quality_compliance_ui_contract():
    surface = domain_capability_surface_contract()
    ui = build_ui_contract()
    return {
        "ok": ui["ok"],
        "pbc": PBC_KEY,
        "fragments": ui["fragments"],
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": ui["action_permissions"],
        "full_capability_surface": {
            "operation_actions": tuple(item["operation"] for item in surface["operation_surfaces"]),
            "rule_editors": tuple(item["rule"] for item in surface["rule_surfaces"]),
            "parameter_editors": tuple(item["parameter"] for item in surface["parameter_surfaces"]),
            "advanced_panels": tuple(item["capability"] for item in surface["advanced_surfaces"]),
            "table_browsers": tuple(item["owned_table"] for item in surface["table_surfaces"]),
            "edge_case_queues": tuple(item["edge_case"] for item in surface["edge_case_surfaces"]),
            "agent_tools": surface["specialist_capabilities"],
            "navigation_sections": ("overview", "operations", "wizards", "edge_case_triage", "release_evidence"),
            "coverage": surface["coverage"],
            "forms": ui["forms"],
            "controls": ui["controls"],
        },
        "side_effects": (),
    }


def food_safety_quality_compliance_render_workbench(state=None, tenant: str = "default"):
    return build_app_surface(state, tenant=tenant)


def smoke_test():
    return {"ok": food_safety_quality_compliance_ui_contract()["ok"] and food_safety_quality_compliance_render_workbench()["ok"], "side_effects": ()}
