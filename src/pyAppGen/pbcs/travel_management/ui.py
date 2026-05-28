"""UI fragments for the travel_management PBC."""
PBC_KEY = 'travel_management'
UI_FRAGMENTS = ('TravelManagementWorkbench', 'TravelManagementDetail', 'TravelManagementAssistantPanel')


def travel_management_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('travel_management.read', 'travel_management.create', 'travel_management.update', 'travel_management.approve', 'travel_management.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def travel_management_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('travel_management.read', 'travel_management.create', 'travel_management.update', 'travel_management.approve', 'travel_management.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': travel_management_ui_contract()['ok'] and travel_management_render_workbench()['ok'], 'side_effects': ()}

# Full UI capability surface bound to the world-class domain-depth contract.
from .domain_depth import ui_capability_surface_contract as travel_management_ui_capability_surface_contract
from .domain_depth import domain_capability_surface_contract as travel_management_domain_capability_surface_contract

_BASE_TRAVEL_MANAGEMENT_UI_CONTRACT = travel_management_ui_contract
_BASE_TRAVEL_MANAGEMENT_RENDER_WORKBENCH = travel_management_render_workbench


def travel_management_ui_contract():
    base = dict(_BASE_TRAVEL_MANAGEMENT_UI_CONTRACT())
    full = travel_management_ui_capability_surface_contract()
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


def travel_management_render_workbench(state=None):
    base = dict(_BASE_TRAVEL_MANAGEMENT_RENDER_WORKBENCH(state=state))
    full = travel_management_ui_capability_surface_contract()
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
