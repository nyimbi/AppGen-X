"""UI fragments for the sustainability_esg_reporting PBC."""
PBC_KEY = 'sustainability_esg_reporting'
UI_FRAGMENTS = ('SustainabilityEsgReportingWorkbench', 'SustainabilityEsgReportingDetail', 'SustainabilityEsgReportingAssistantPanel')


def sustainability_esg_reporting_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('sustainability_esg_reporting.read', 'sustainability_esg_reporting.create', 'sustainability_esg_reporting.update', 'sustainability_esg_reporting.approve', 'sustainability_esg_reporting.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def sustainability_esg_reporting_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('sustainability_esg_reporting.read', 'sustainability_esg_reporting.create', 'sustainability_esg_reporting.update', 'sustainability_esg_reporting.approve', 'sustainability_esg_reporting.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': sustainability_esg_reporting_ui_contract()['ok'] and sustainability_esg_reporting_render_workbench()['ok'], 'side_effects': ()}

# Full UI capability surface bound to the world-class domain-depth contract.
from .domain_depth import ui_capability_surface_contract as sustainability_esg_reporting_ui_capability_surface_contract
from .domain_depth import domain_capability_surface_contract as sustainability_esg_reporting_domain_capability_surface_contract

_BASE_SUSTAINABILITY_ESG_REPORTING_UI_CONTRACT = sustainability_esg_reporting_ui_contract
_BASE_SUSTAINABILITY_ESG_REPORTING_RENDER_WORKBENCH = sustainability_esg_reporting_render_workbench


def sustainability_esg_reporting_ui_contract():
    base = dict(_BASE_SUSTAINABILITY_ESG_REPORTING_UI_CONTRACT())
    full = sustainability_esg_reporting_ui_capability_surface_contract()
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


def sustainability_esg_reporting_render_workbench(state=None):
    base = dict(_BASE_SUSTAINABILITY_ESG_REPORTING_RENDER_WORKBENCH(state=state))
    full = sustainability_esg_reporting_ui_capability_surface_contract()
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
