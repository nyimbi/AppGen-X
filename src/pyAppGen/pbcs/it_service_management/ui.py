from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
from .controls import control_catalog
from .forms import form_catalog
from .wizards import wizard_catalog
PBC_KEY = 'it_service_management'

def it_service_management_ui_contract():
    surface = domain_capability_surface_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('ItServiceManagementWorkbench', 'ItServiceManagementDetail', 'ItServiceManagementAssistantPanel'), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('it_service_management.read',
 'it_service_management.create',
 'it_service_management.update',
 'it_service_management.approve',
 'it_service_management.admin'), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS, 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS), 'navigation_sections': ('overview','operations','edge_case_triage','advanced_intelligence','service_desk','change_enablement','cmdb','sla_control','release_evidence'), 'forms': form_catalog()['forms'], 'wizards': wizard_catalog()['wizards'], 'controls': control_catalog()['controls'], 'coverage': surface['coverage']}, 'side_effects': ()}

def it_service_management_render_workbench():
    ui = it_service_management_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'operation_actions': full['operation_actions'], 'table_browsers': full['table_browsers'], 'side_effects': ()}


def it_service_management_standalone_ui_contract():
    ui = it_service_management_ui_contract()
    full = ui['full_capability_surface']
    return {
        'ok': ui['ok'] and len(full['forms']) >= 9 and len(full['wizards']) >= 6 and len(full['controls']) >= 8,
        'pbc': PBC_KEY,
        'single_pbc_app_route': f'/apps/{PBC_KEY}',
        'forms': full['forms'],
        'wizards': full['wizards'],
        'controls': full['controls'],
        'assistant_panel': 'ItServiceManagementAssistantPanel',
        'side_effects': (),
    }

def smoke_test():
    return {'ok': it_service_management_ui_contract()['ok'] and it_service_management_render_workbench()['ok'] and it_service_management_standalone_ui_contract()['ok'], 'side_effects': ()}

# Improve1 ITSM UI control extension.
from .itsm_control import improve1_itsm_control_contract as it_service_management_improve1_itsm_control_contract

_IT_SERVICE_MANAGEMENT_BASE_UI_CONTRACT = it_service_management_ui_contract
_IT_SERVICE_MANAGEMENT_BASE_RENDER_WORKBENCH = it_service_management_render_workbench


def it_service_management_ui_contract():
    base = dict(_IT_SERVICE_MANAGEMENT_BASE_UI_CONTRACT())
    itsm_control = it_service_management_improve1_itsm_control_contract()
    control_panels = tuple(item["evidence"]["ui_surface"] for item in itsm_control["capabilities"])
    service_actions = tuple(item["evidence"]["service_api"] for item in itsm_control["capabilities"])
    full_surface = dict(base.get("full_capability_surface", {}))
    full_surface.update({"itsm_control_panels": control_panels, "itsm_control_service_actions": service_actions, "itsm_control_tables": itsm_control["owned_tables"]})
    return {**base, "ok": base.get("ok") is True and itsm_control["ok"], "full_capability_surface": full_surface, "itsm_control_contract": itsm_control, "itsm_control_panels": control_panels, "itsm_control_service_actions": service_actions, "side_effects": ()}


def it_service_management_render_workbench():
    base = dict(_IT_SERVICE_MANAGEMENT_BASE_RENDER_WORKBENCH())
    itsm_control = it_service_management_improve1_itsm_control_contract()
    return {**base, "ok": base.get("ok") is True and itsm_control["ok"], "itsm_control_panels": tuple(item["evidence"]["ui_surface"] for item in itsm_control["capabilities"]), "itsm_control_service_actions": tuple(item["evidence"]["service_api"] for item in itsm_control["capabilities"]), "itsm_control_agent_tools": tuple(f"it_service_management.agent.{item['slug']}" for item in itsm_control["capabilities"]), "side_effects": ()}
