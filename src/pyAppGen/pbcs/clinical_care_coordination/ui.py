from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
from .care_coordination_app import care_coordination_controls_contract, care_coordination_forms_contract, care_coordination_wizards_contract, single_pbc_app_contract
PBC_KEY = 'clinical_care_coordination'

def clinical_care_coordination_ui_contract():
    surface = domain_capability_surface_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('ClinicalCareCoordinationWorkbench',
 'ClinicalCareCoordinationDetail',
 'ClinicalCareCoordinationAssistantPanel'), 'forms': care_coordination_forms_contract()['forms'], 'wizards': care_coordination_wizards_contract()['wizards'], 'controls': care_coordination_controls_contract()['controls'], 'single_pbc_app': single_pbc_app_contract(), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('clinical_care_coordination.read',
 'clinical_care_coordination.create',
 'clinical_care_coordination.update',
 'clinical_care_coordination.approve',
 'clinical_care_coordination.admin'), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS, 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS), 'navigation_sections': ('overview','operations','edge_case_triage','advanced_intelligence','release_evidence'), 'coverage': surface['coverage']}, 'side_effects': ()}

def clinical_care_coordination_render_workbench():
    ui = clinical_care_coordination_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'queues': ('high_risk_patients','unscheduled_referrals','unreconciled_results','active_transitions','blocked_care_gaps','outreach_due_today','care_team_coverage_gaps','control_failures'), 'operation_actions': full['operation_actions'], 'forms': ui['forms'], 'wizards': ui['wizards'], 'controls': ui['controls'], 'table_browsers': full['table_browsers'], 'side_effects': ()}

def clinical_care_coordination_forms_contract():
    return care_coordination_forms_contract()

def clinical_care_coordination_wizard_contract():
    return care_coordination_wizards_contract()

def clinical_care_coordination_controls_contract():
    return care_coordination_controls_contract()

def smoke_test():
    return {'ok': clinical_care_coordination_ui_contract()['ok'] and clinical_care_coordination_render_workbench()['ok'], 'side_effects': ()}
