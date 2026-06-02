from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
PBC_KEY = 'public_sector_case_management'

def public_sector_case_management_ui_contract():
    surface = domain_capability_surface_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('PublicSectorCaseManagementWorkbench',
 'PublicSectorCaseManagementDetail',
 'PublicSectorCaseManagementAssistantPanel'), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('public_sector_case_management.read',
 'public_sector_case_management.create',
 'public_sector_case_management.update',
 'public_sector_case_management.approve',
 'public_sector_case_management.admin'), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS, 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS), 'navigation_sections': ('overview','operations','edge_case_triage','advanced_intelligence','release_evidence'), 'coverage': surface['coverage']}, 'side_effects': ()}

def public_sector_case_management_render_workbench():
    ui = public_sector_case_management_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'operation_actions': full['operation_actions'], 'table_browsers': full['table_browsers'], 'side_effects': ()}

def smoke_test():
    return {'ok': public_sector_case_management_ui_contract()['ok'] and public_sector_case_management_render_workbench()['ok'], 'side_effects': ()}

# Improve1 public sector case control UI extension.
from .public_sector_case_control import improve1_public_sector_case_control_contract as _improve1_public_sector_case_control_contract

_PUBLIC_SECTOR_CASE_CONTROL_BASE_UI_CONTRACT = public_sector_case_management_ui_contract
_PUBLIC_SECTOR_CASE_CONTROL_BASE_RENDER_WORKBENCH = public_sector_case_management_render_workbench


def public_sector_case_management_ui_contract() -> dict:
    ui = dict(_PUBLIC_SECTOR_CASE_CONTROL_BASE_UI_CONTRACT())
    control = _improve1_public_sector_case_control_contract()
    ui.update({
        "ok": ui.get("ok") is True and control["ok"],
        "public_sector_case_control_contract": control,
        "public_sector_case_control_panels": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]),
        "public_sector_case_control_service_actions": tuple(item["evidence"]["service_api"] for item in control["capabilities"]),
        "stream_engine_picker_visible": False,
    })
    return ui


def public_sector_case_management_render_workbench(*args, **kwargs) -> dict:
    workbench = dict(_PUBLIC_SECTOR_CASE_CONTROL_BASE_RENDER_WORKBENCH(*args, **kwargs))
    control = _improve1_public_sector_case_control_contract()
    workbench.update({
        "ok": workbench.get("ok") is True and control["ok"],
        "public_sector_case_control_panels": tuple(item["evidence"]["ui_surface"] for item in control["capabilities"]),
        "public_sector_case_control_service_actions": tuple(item["evidence"]["service_api"] for item in control["capabilities"]),
        "public_sector_case_control_agent_tools": tuple(f"public_sector_case_management.skills.{item['slug']}" for item in control["capabilities"]),
    })
    return workbench
