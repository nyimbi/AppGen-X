"""UI fragments for the facilities_space_management PBC."""
PBC_KEY = 'facilities_space_management'
UI_FRAGMENTS = ('FacilitiesSpaceManagementWorkbench', 'FacilitiesSpaceManagementDetail', 'FacilitiesSpaceManagementAssistantPanel')


def facilities_space_management_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('facilities_space_management.read', 'facilities_space_management.create', 'facilities_space_management.update', 'facilities_space_management.approve', 'facilities_space_management.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def facilities_space_management_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('facilities_space_management.read', 'facilities_space_management.create', 'facilities_space_management.update', 'facilities_space_management.approve', 'facilities_space_management.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': facilities_space_management_ui_contract()['ok'] and facilities_space_management_render_workbench()['ok'], 'side_effects': ()}

# Full UI capability surface bound to the world-class domain-depth contract.
from .domain_depth import ui_capability_surface_contract as facilities_space_management_ui_capability_surface_contract
from .domain_depth import domain_capability_surface_contract as facilities_space_management_domain_capability_surface_contract

_BASE_FACILITIES_SPACE_MANAGEMENT_UI_CONTRACT = facilities_space_management_ui_contract
_BASE_FACILITIES_SPACE_MANAGEMENT_RENDER_WORKBENCH = facilities_space_management_render_workbench


def facilities_space_management_ui_contract():
    base = dict(_BASE_FACILITIES_SPACE_MANAGEMENT_UI_CONTRACT())
    full = facilities_space_management_ui_capability_surface_contract()
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


def facilities_space_management_render_workbench(state=None):
    base = dict(_BASE_FACILITIES_SPACE_MANAGEMENT_RENDER_WORKBENCH(state=state))
    full = facilities_space_management_ui_capability_surface_contract()
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
