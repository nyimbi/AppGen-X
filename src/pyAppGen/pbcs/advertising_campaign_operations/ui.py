from .campaign_planning import build_command_center_summary
from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
PBC_KEY = 'advertising_campaign_operations'

def advertising_campaign_operations_ui_contract():
    surface = domain_capability_surface_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('AdvertisingCampaignOperationsWorkbench',
 'AdvertisingCampaignOperationsDetail',
 'AdvertisingCampaignOperationsAssistantPanel'), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('advertising_campaign_operations.read',
 'advertising_campaign_operations.create',
 'advertising_campaign_operations.update',
 'advertising_campaign_operations.approve',
 'advertising_campaign_operations.admin'), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS + ('create_campaign_plan','attempt_launch_campaign'), 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS + ('create_campaign_plan','attempt_launch_campaign')), 'planning_panels': ('campaign_brief_canvas','launch_readiness_gate'), 'navigation_sections': ('overview','campaign_planning','launch_command_center','operations','edge_case_triage','advanced_intelligence','release_evidence'), 'coverage': surface['coverage']}, 'side_effects': ()}

def advertising_campaign_operations_render_workbench(campaign_plans=()):
    ui = advertising_campaign_operations_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'operation_actions': full['operation_actions'], 'table_browsers': full['table_browsers'], 'planning_panels': full['planning_panels'], 'command_center': build_command_center_summary(campaign_plans), 'side_effects': ()}

def smoke_test():
    return {'ok': advertising_campaign_operations_ui_contract()['ok'] and advertising_campaign_operations_render_workbench()['ok'], 'side_effects': ()}
