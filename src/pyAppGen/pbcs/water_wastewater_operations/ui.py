from . import operations_engine as engine
from .domain_depth import domain_capability_surface_contract

PBC_KEY = engine.PBC_KEY


def water_wastewater_operations_ui_contract():
    surface = domain_capability_surface_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": engine.UI_FRAGMENTS,
        "configuration_editor": {"enabled": True, "stream_engine_picker_visible": False},
        "forms": engine.FORM_DEFINITIONS,
        "wizards": engine.WIZARD_DEFINITIONS,
        "controls": engine.CONTROL_DEFINITIONS,
        "command_center_sections": engine.WORKBENCH_SECTIONS,
        "stream_engine_picker_visible": False,
        "action_permissions": (
            f"{PBC_KEY}.read",
            f"{PBC_KEY}.operate",
            f"{PBC_KEY}.approve",
            f"{PBC_KEY}.admin",
            f"{PBC_KEY}.event",
            f"{PBC_KEY}.audit",
        ),
        "full_capability_surface": {
            "operation_actions": engine.DOMAIN_OPERATIONS,
            "rule_editors": engine.RULES,
            "parameter_editors": tuple(engine.PARAMETER_SPECS),
            "advanced_panels": engine.ADVANCED_CAPABILITIES,
            "table_browsers": engine.OWNED_TABLES,
            "edge_case_queues": surface["edge_case_surfaces"],
            "agent_tools": tuple(f"{PBC_KEY}_skills.{skill['name']}" for skill in engine.AGENT_SKILLS),
            "navigation_sections": ("overview", "operations", "compliance", "incidents", "release_evidence"),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def water_wastewater_operations_ui_binding_contract():
    return {
        "format": "appgen.water-wastewater-operations-ui-binding-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "binding_evidence": {
            "runtime_tables": engine.RUNTIME_TABLES,
            "forms": engine.FORM_DEFINITIONS,
            "wizards": engine.WIZARD_DEFINITIONS,
            "controls": engine.CONTROL_DEFINITIONS,
            "outbox_table": engine.RUNTIME_TABLES[0],
        },
        "side_effects": (),
    }


def water_wastewater_operations_render_workbench(state=None, tenant="default", filters=None):
    return engine.build_workbench_view(state, tenant=tenant, filters=filters)


def smoke_test():
    return {"ok": water_wastewater_operations_ui_contract()["ok"] and water_wastewater_operations_render_workbench()["ok"] and water_wastewater_operations_ui_binding_contract()["ok"], "side_effects": ()}


# Improve1 water wastewater operations control UI extension.
from .water_wastewater_operations_control import improve1_water_wastewater_operations_control_contract as _improve1_water_wastewater_operations_control_contract
_WATER_CONTROL_BASE_UI_CONTRACT = water_wastewater_operations_ui_contract
_WATER_CONTROL_BASE_RENDER_WORKBENCH = water_wastewater_operations_render_workbench
def water_wastewater_operations_ui_contract() -> dict:
    ui=dict(_WATER_CONTROL_BASE_UI_CONTRACT()); control=_improve1_water_wastewater_operations_control_contract(); ui.update({"ok":ui.get("ok") is True and control["ok"],"water_wastewater_operations_control_contract":control,"water_wastewater_operations_control_panels":tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]),"water_wastewater_operations_control_service_actions":tuple(item["evidence"]["service_api"] for item in control["capabilities"]),"stream_engine_picker_visible":False}); return ui
def water_wastewater_operations_render_workbench(*args, **kwargs) -> dict:
    workbench=dict(_WATER_CONTROL_BASE_RENDER_WORKBENCH(*args, **kwargs)); control=_improve1_water_wastewater_operations_control_contract(); workbench.update({"ok":workbench.get("ok") is True and control["ok"],"water_wastewater_operations_control_panels":tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]),"water_wastewater_operations_control_service_actions":tuple(item["evidence"]["service_api"] for item in control["capabilities"]),"water_wastewater_operations_control_agent_tools":tuple(f"water_wastewater_operations.skills.{item['slug']}" for item in control["capabilities"])}); return workbench
