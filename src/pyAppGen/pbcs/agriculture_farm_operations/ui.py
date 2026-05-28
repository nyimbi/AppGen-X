from .crop_planning import PLANTING_WINDOW_STATUSES
from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
PBC_KEY = 'agriculture_farm_operations'

def agriculture_farm_operations_ui_contract():
    surface = domain_capability_surface_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('AgricultureFarmOperationsWorkbench',
 'AgricultureFarmOperationsDetail',
 'AgricultureFarmOperationsAssistantPanel'), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('agriculture_farm_operations.read',
 'agriculture_farm_operations.create',
 'agriculture_farm_operations.update',
 'agriculture_farm_operations.approve',
 'agriculture_farm_operations.admin'), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS, 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS), 'navigation_sections': ('overview','operations','crop_plan_timeline','planting_window_alerts','edge_case_triage','advanced_intelligence','release_evidence'), 'planning_widgets': ('crop_plan_timeline','planting_window_alerts','preplant_readiness_blockers'), 'planning_window_statuses': PLANTING_WINDOW_STATUSES, 'coverage': surface['coverage']}, 'side_effects': ()}

def agriculture_farm_operations_render_workbench():
    ui = agriculture_farm_operations_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'operation_actions': full['operation_actions'], 'table_browsers': full['table_browsers'], 'side_effects': ()}

def smoke_test():
    return {'ok': agriculture_farm_operations_ui_contract()['ok'] and agriculture_farm_operations_render_workbench()['ok'], 'side_effects': ()}
