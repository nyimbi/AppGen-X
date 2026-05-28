from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
from .fundraising_app import controls_contract, forms_contract, single_pbc_app_contract, wizards_contract
PBC_KEY = 'donor_grant_fundraising'

def donor_grant_fundraising_ui_contract():
    surface = domain_capability_surface_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('DonorGrantFundraisingWorkbench',
 'DonorGrantFundraisingDetail',
 'DonorGrantFundraisingAssistantPanel'), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('donor_grant_fundraising.read',
 'donor_grant_fundraising.create',
 'donor_grant_fundraising.update',
 'donor_grant_fundraising.approve',
 'donor_grant_fundraising.admin'), 'forms': forms_contract()['forms'], 'wizards': wizards_contract()['wizards'], 'controls': controls_contract()['controls'], 'single_pbc_app': single_pbc_app_contract(), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS, 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS), 'navigation_sections': ('portfolio','campaigns','pledges_gifts','grant_pipeline','stewardship','restrictions','assistant','release_evidence'), 'coverage': surface['coverage']}, 'side_effects': ()}

def donor_grant_fundraising_render_workbench():
    ui = donor_grant_fundraising_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'queues': ('portfolio_next_actions','pledge_exposure','acknowledgement_backlog','grant_deadline_risk','stewardship_gaps','campaign_performance','exception_backlog'), 'operation_actions': full['operation_actions'], 'forms': ui['forms'], 'wizards': ui['wizards'], 'controls': ui['controls'], 'table_browsers': full['table_browsers'], 'side_effects': ()}

def donor_grant_fundraising_forms_contract():
    return forms_contract()

def donor_grant_fundraising_wizards_contract():
    return wizards_contract()

def donor_grant_fundraising_controls_contract():
    return controls_contract()

def smoke_test():
    return {'ok': donor_grant_fundraising_ui_contract()['ok'] and donor_grant_fundraising_render_workbench()['ok'], 'side_effects': ()}
