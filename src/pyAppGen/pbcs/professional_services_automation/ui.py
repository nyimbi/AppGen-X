"""UI fragments for the professional_services_automation PBC."""
PBC_KEY = 'professional_services_automation'
UI_FRAGMENTS = ('ProfessionalServicesAutomationWorkbench', 'ProfessionalServicesAutomationDetail', 'ProfessionalServicesAutomationAssistantPanel')


def professional_services_automation_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('professional_services_automation.read', 'professional_services_automation.create', 'professional_services_automation.update', 'professional_services_automation.approve', 'professional_services_automation.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def professional_services_automation_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('professional_services_automation.read', 'professional_services_automation.create', 'professional_services_automation.update', 'professional_services_automation.approve', 'professional_services_automation.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': professional_services_automation_ui_contract()['ok'] and professional_services_automation_render_workbench()['ok'], 'side_effects': ()}

# Full UI capability surface bound to the world-class domain-depth contract.
from .domain_depth import ui_capability_surface_contract as professional_services_automation_ui_capability_surface_contract
from .domain_depth import domain_capability_surface_contract as professional_services_automation_domain_capability_surface_contract

_BASE_PROFESSIONAL_SERVICES_AUTOMATION_UI_CONTRACT = professional_services_automation_ui_contract
_BASE_PROFESSIONAL_SERVICES_AUTOMATION_RENDER_WORKBENCH = professional_services_automation_render_workbench


def professional_services_automation_ui_contract():
    base = dict(_BASE_PROFESSIONAL_SERVICES_AUTOMATION_UI_CONTRACT())
    full = professional_services_automation_ui_capability_surface_contract()
    return {
        **base,
        'ok': base.get('ok') is True and full['ok'],
        'full_capability_surface': full,
        'operation_actions': full['operation_actions'],
        'rule_editors': full['rule_editors'],
        'parameter_editors': full['parameter_editors'],
        'advanced_panels': full['advanced_panels'],
        'edge_case_queues': full['edge_case_queues'],
        'table_browsers': full['table_browsers'],
        'navigation_sections': full['navigation_sections'],
    }


def professional_services_automation_render_workbench(state=None):
    base = dict(_BASE_PROFESSIONAL_SERVICES_AUTOMATION_RENDER_WORKBENCH(state=state))
    full = professional_services_automation_ui_capability_surface_contract()
    return {
        **base,
        'ok': base.get('ok') is True and full['ok'],
        'panels': tuple(dict.fromkeys(tuple(base.get('panels', ())) + full['navigation_sections'])),
        'operation_actions': full['operation_actions'],
        'advanced_panels': full['advanced_panels'],
        'edge_case_queues': full['edge_case_queues'],
        'table_browsers': full['table_browsers'],
        'agent_tools': full['agent_tools'],
    }
