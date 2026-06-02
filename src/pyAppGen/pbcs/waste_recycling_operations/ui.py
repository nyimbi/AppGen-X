from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
PBC_KEY = 'waste_recycling_operations'

def waste_recycling_operations_ui_contract():
    surface = domain_capability_surface_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('WasteRecyclingOperationsWorkbench',
 'WasteRecyclingOperationsDetail',
 'WasteRecyclingOperationsAssistantPanel'), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('waste_recycling_operations.read',
 'waste_recycling_operations.create',
 'waste_recycling_operations.update',
 'waste_recycling_operations.approve',
 'waste_recycling_operations.admin'), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS, 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS), 'navigation_sections': ('overview','operations','edge_case_triage','advanced_intelligence','release_evidence'), 'coverage': surface['coverage']}, 'side_effects': ()}

def waste_recycling_operations_render_workbench():
    ui = waste_recycling_operations_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'operation_actions': full['operation_actions'], 'table_browsers': full['table_browsers'], 'side_effects': ()}

def smoke_test():
    return {'ok': waste_recycling_operations_ui_contract()['ok'] and waste_recycling_operations_render_workbench()['ok'], 'side_effects': ()}


# Improve1 waste recycling operations control UI extension.
from .waste_recycling_operations_control import improve1_waste_recycling_operations_control_contract as _improve1_waste_recycling_operations_control_contract

_WASTE_CONTROL_BASE_UI_CONTRACT = waste_recycling_operations_ui_contract
_WASTE_CONTROL_BASE_RENDER_WORKBENCH = waste_recycling_operations_render_workbench


def waste_recycling_operations_ui_contract() -> dict:
    ui = dict(_WASTE_CONTROL_BASE_UI_CONTRACT())
    control = _improve1_waste_recycling_operations_control_contract()
    ui.update({"ok": ui.get("ok") is True and control["ok"], "waste_recycling_operations_control_contract": control, "waste_recycling_operations_control_panels": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]), "waste_recycling_operations_control_service_actions": tuple(item["evidence"]["service_api"] for item in control["capabilities"]), "stream_engine_picker_visible": False})
    return ui


def waste_recycling_operations_render_workbench(*args, **kwargs) -> dict:
    workbench = dict(_WASTE_CONTROL_BASE_RENDER_WORKBENCH(*args, **kwargs))
    control = _improve1_waste_recycling_operations_control_contract()
    workbench.update({"ok": workbench.get("ok") is True and control["ok"], "waste_recycling_operations_control_panels": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]), "waste_recycling_operations_control_service_actions": tuple(item["evidence"]["service_api"] for item in control["capabilities"]), "waste_recycling_operations_control_agent_tools": tuple(f"waste_recycling_operations.skills.{item['slug']}" for item in control["capabilities"])})
    return workbench
