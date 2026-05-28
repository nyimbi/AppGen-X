from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
PBC_KEY = 'aviation_maintenance_repair'

def aviation_maintenance_repair_ui_contract():
    surface = domain_capability_surface_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('AviationMaintenanceRepairWorkbench',
 'AviationMaintenanceRepairDetail',
 'AviationMaintenanceRepairAssistantPanel'), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('aviation_maintenance_repair.read',
 'aviation_maintenance_repair.create',
 'aviation_maintenance_repair.update',
 'aviation_maintenance_repair.approve',
 'aviation_maintenance_repair.admin'), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS + ('assess_release_to_service',), 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS + ('assess_release_to_service',)), 'release_panels': ('release_to_service_pack','duplicate_inspection_evidence','component_life_traceability','tooling_and_consumable_lockouts'), 'navigation_sections': ('overview','release_to_service','operations','edge_case_triage','advanced_intelligence','release_evidence'), 'coverage': surface['coverage']}, 'side_effects': ()}

def aviation_maintenance_repair_render_workbench():
    ui = aviation_maintenance_repair_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'operation_actions': full['operation_actions'], 'table_browsers': full['table_browsers'], 'release_panels': full['release_panels'], 'side_effects': ()}

def smoke_test():
    return {'ok': aviation_maintenance_repair_ui_contract()['ok'] and aviation_maintenance_repair_render_workbench()['ok'], 'side_effects': ()}
