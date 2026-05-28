from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
from .court_operations_app import controls_contract, forms_contract, single_pbc_app_contract, wizards_contract
PBC_KEY = 'court_case_management'

def court_case_management_ui_contract():
    surface = domain_capability_surface_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('CourtCaseManagementWorkbench', 'CourtCaseManagementDetail', 'CourtCaseManagementAssistantPanel'), 'forms': forms_contract()['forms'], 'wizards': wizards_contract()['wizards'], 'controls': controls_contract()['controls'], 'single_pbc_app': single_pbc_app_contract(), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('court_case_management.read',
 'court_case_management.create',
 'court_case_management.update',
 'court_case_management.approve',
 'court_case_management.admin'), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS, 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS), 'navigation_sections': ('overview','operations','edge_case_triage','advanced_intelligence','release_evidence'), 'coverage': surface['coverage']}, 'side_effects': ()}

def court_case_management_render_workbench():
    ui = court_case_management_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'queues': ('clerk_deficiency_queue','accepted_filings','chambers_order_review','courtroom_calendar','sealed_or_restricted_items','open_cases'), 'operation_actions': full['operation_actions'], 'forms': ui['forms'], 'wizards': ui['wizards'], 'controls': ui['controls'], 'table_browsers': full['table_browsers'], 'side_effects': ()}

def court_case_management_forms_contract():
    return forms_contract()

def court_case_management_wizard_contract():
    return wizards_contract()

def court_case_management_controls_contract():
    return controls_contract()

def smoke_test():
    return {'ok': court_case_management_ui_contract()['ok'] and court_case_management_render_workbench()['ok'], 'side_effects': ()}
