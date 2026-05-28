from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
PBC_KEY = 'telecom_subscription_lifecycle'

def telecom_subscription_lifecycle_ui_contract():
    surface = domain_capability_surface_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('TelecomSubscriptionLifecycleWorkbench',
 'TelecomSubscriptionLifecycleDetail',
 'TelecomSubscriptionLifecycleAssistantPanel'), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('telecom_subscription_lifecycle.read',
 'telecom_subscription_lifecycle.create',
 'telecom_subscription_lifecycle.update',
 'telecom_subscription_lifecycle.approve',
 'telecom_subscription_lifecycle.admin'), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS, 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS), 'navigation_sections': ('overview','operations','edge_case_triage','advanced_intelligence','release_evidence'), 'coverage': surface['coverage']}, 'side_effects': ()}

def telecom_subscription_lifecycle_render_workbench():
    ui = telecom_subscription_lifecycle_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'operation_actions': full['operation_actions'], 'table_browsers': full['table_browsers'], 'side_effects': ()}

def smoke_test():
    return {'ok': telecom_subscription_lifecycle_ui_contract()['ok'] and telecom_subscription_lifecycle_render_workbench()['ok'], 'side_effects': ()}
