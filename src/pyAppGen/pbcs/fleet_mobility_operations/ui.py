from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
from .forms import form_catalog
from .wizards import wizard_catalog
from .controls import control_catalog
PBC_KEY = 'fleet_mobility_operations'

def fleet_mobility_operations_ui_contract():
    surface = domain_capability_surface_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('FleetMobilityOperationsWorkbench',
 'FleetMobilityOperationsDetail',
 'FleetMobilityOperationsAssistantPanel'), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('fleet_mobility_operations.read',
 'fleet_mobility_operations.create',
 'fleet_mobility_operations.update',
 'fleet_mobility_operations.approve',
 'fleet_mobility_operations.admin'), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS, 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS), 'navigation_sections': ('overview','dispatch_board','live_route_map','blocked_assets','telematics_quarantine','maintenance_workshop','safety_compliance','fuel_ev','agent_workspace','release_evidence'), 'forms': form_catalog()['forms'], 'wizards': wizard_catalog()['wizards'], 'controls': control_catalog()['controls'], 'coverage': surface['coverage']}, 'side_effects': ()}

def fleet_mobility_operations_render_workbench():
    ui = fleet_mobility_operations_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'operation_actions': full['operation_actions'], 'table_browsers': full['table_browsers'], 'side_effects': ()}

def fleet_mobility_operations_standalone_ui_contract():
    ui = fleet_mobility_operations_ui_contract()
    surface = ui['full_capability_surface']
    return {'ok': ui['ok'] and len(surface['forms']) >= 7 and len(surface['wizards']) >= 6 and len(surface['controls']) >= 10, 'pbc': PBC_KEY, 'fragments': ui['fragments'], 'forms': surface['forms'], 'wizards': surface['wizards'], 'controls': surface['controls'], 'side_effects': ()}

def smoke_test():
    standalone = fleet_mobility_operations_standalone_ui_contract()
    return {'ok': fleet_mobility_operations_ui_contract()['ok'] and fleet_mobility_operations_render_workbench()['ok'] and standalone['ok'], 'side_effects': ()}


from .fleet_control import improve1_fleet_control_contract

_fleet_mobility_operations_base_ui_contract = fleet_mobility_operations_ui_contract
_fleet_mobility_operations_base_render_workbench = fleet_mobility_operations_render_workbench

def fleet_mobility_operations_ui_contract():
    ui = _fleet_mobility_operations_base_ui_contract()
    control = improve1_fleet_control_contract()
    surface = dict(ui.get('full_capability_surface', {}))
    surface['fleet_control_panels'] = tuple(item['evidence']['ui_surface'] for item in control['capabilities'])
    surface['fleet_control_service_actions'] = tuple(item['evidence']['service_api'] for item in control['capabilities'])
    surface['fleet_control_tables'] = control['owned_tables']
    return {**ui, 'ok': ui.get('ok') is True and control['ok'], 'full_capability_surface': surface, 'fleet_control_contract': control, 'side_effects': ()}

def fleet_mobility_operations_render_workbench():
    workbench = _fleet_mobility_operations_base_render_workbench()
    control = improve1_fleet_control_contract()
    return {**workbench, 'ok': workbench.get('ok') is True and control['ok'], 'fleet_control_panels': tuple(item['evidence']['ui_surface'] for item in control['capabilities']), 'fleet_control_service_actions': tuple(item['evidence']['service_api'] for item in control['capabilities']), 'side_effects': ()}
