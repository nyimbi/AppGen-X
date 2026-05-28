from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
from .defense_app import controls_contract, forms_contract, single_pbc_app_contract, wizards_contract
PBC_KEY = 'defense_readiness_logistics'

def defense_readiness_logistics_ui_contract():
    surface = domain_capability_surface_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('DefenseReadinessLogisticsWorkbench',
 'DefenseReadinessLogisticsDetail',
 'DefenseReadinessLogisticsAssistantPanel'), 'forms': forms_contract()['forms'], 'wizards': wizards_contract()['wizards'], 'controls': controls_contract()['controls'], 'single_pbc_app': single_pbc_app_contract(), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('defense_readiness_logistics.read',
 'defense_readiness_logistics.create',
 'defense_readiness_logistics.update',
 'defense_readiness_logistics.approve',
 'defense_readiness_logistics.admin'), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS, 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS), 'navigation_sections': ('overview','operations','edge_case_triage','advanced_intelligence','release_evidence'), 'coverage': surface['coverage']}, 'side_effects': ()}

def defense_readiness_logistics_render_workbench():
    ui = defense_readiness_logistics_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'queues': ('commander_readiness_board','maintenance_control','supply_readiness','movement_control','classified_export_review','exception_backlog'), 'operation_actions': full['operation_actions'], 'forms': ui['forms'], 'wizards': ui['wizards'], 'controls': ui['controls'], 'table_browsers': full['table_browsers'], 'side_effects': ()}

def defense_readiness_logistics_forms_contract():
    return forms_contract()

def defense_readiness_logistics_wizards_contract():
    return wizards_contract()

def defense_readiness_logistics_controls_contract():
    return controls_contract()

def smoke_test():
    return {'ok': defense_readiness_logistics_ui_contract()['ok'] and defense_readiness_logistics_render_workbench()['ok'], 'side_effects': ()}
