from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
from .forms import form_catalog
from .wizards import wizard_catalog
from .controls import control_catalog
PBC_KEY = 'facility_energy_management'

def facility_energy_management_ui_contract():
    surface = domain_capability_surface_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('FacilityEnergyManagementWorkbench',
 'FacilityEnergyManagementDetail',
 'FacilityEnergyManagementAssistantPanel'), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('facility_energy_management.read',
 'facility_energy_management.create',
 'facility_energy_management.update',
 'facility_energy_management.approve',
 'facility_energy_management.admin'), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS, 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS), 'navigation_sections': ('overview','meter_topology','interval_reads','tariffs','hvac_schedules','demand_response','baselines','anomalies','controls','agent_workspace','release_evidence'), 'forms': form_catalog()['forms'], 'wizards': wizard_catalog()['wizards'], 'controls': control_catalog()['controls'], 'coverage': surface['coverage']}, 'side_effects': ()}

def facility_energy_management_render_workbench():
    ui = facility_energy_management_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'operation_actions': full['operation_actions'], 'table_browsers': full['table_browsers'], 'side_effects': ()}

def facility_energy_management_standalone_ui_contract():
    ui = facility_energy_management_ui_contract()
    return {'ok': ui['ok'] and len(ui['full_capability_surface']['forms']) >= 7 and len(ui['full_capability_surface']['wizards']) >= 6 and len(ui['full_capability_surface']['controls']) >= 10, 'pbc': PBC_KEY, 'fragments': ui['fragments'], 'forms': ui['full_capability_surface']['forms'], 'wizards': ui['full_capability_surface']['wizards'], 'controls': ui['full_capability_surface']['controls'], 'side_effects': ()}

def smoke_test():
    standalone = facility_energy_management_standalone_ui_contract()
    return {'ok': facility_energy_management_ui_contract()['ok'] and facility_energy_management_render_workbench()['ok'] and standalone['ok'], 'side_effects': ()}


# Improve1 energy control coverage is part of the visible workbench contract.
from .energy_control import improve1_energy_control_contract

_FACILITY_ENERGY_MANAGEMENT_FULL_UI_CONTRACT = facility_energy_management_ui_contract
_FACILITY_ENERGY_MANAGEMENT_FULL_RENDER_WORKBENCH = facility_energy_management_render_workbench


def facility_energy_management_ui_contract():
    base = dict(_FACILITY_ENERGY_MANAGEMENT_FULL_UI_CONTRACT())
    energy_control = improve1_energy_control_contract()
    full_surface = dict(base.get('full_capability_surface', {}))
    full_surface['energy_control_panels'] = tuple(item['evidence']['ui_surface'] for item in energy_control['capabilities'])
    full_surface['energy_control_service_actions'] = tuple(item['evidence']['service_api'] for item in energy_control['capabilities'])
    return {**base, 'ok': base.get('ok') is True and energy_control['ok'], 'full_capability_surface': full_surface, 'energy_control_contract': energy_control, 'stream_engine_picker_visible': False}


def facility_energy_management_render_workbench():
    base = dict(_FACILITY_ENERGY_MANAGEMENT_FULL_RENDER_WORKBENCH())
    energy_control = improve1_energy_control_contract()
    return {**base, 'ok': base.get('ok') is True and energy_control['ok'], 'energy_control_actions': tuple(item['evidence']['service_api'] for item in energy_control['capabilities']), 'energy_control_contract': energy_control, 'stream_engine_picker_visible': False}
