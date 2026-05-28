"""UI fragments for the field_service_management PBC."""
PBC_KEY = 'field_service_management'
UI_FRAGMENTS = ('FieldServiceManagementWorkbench', 'FieldServiceManagementDetail', 'FieldServiceManagementAssistantPanel')


def field_service_management_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('field_service_management.read', 'field_service_management.create', 'field_service_management.update', 'field_service_management.approve', 'field_service_management.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def field_service_management_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('field_service_management.read', 'field_service_management.create', 'field_service_management.update', 'field_service_management.approve', 'field_service_management.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': field_service_management_ui_contract()['ok'] and field_service_management_render_workbench()['ok'], 'side_effects': ()}

# Full UI capability surface bound to the world-class domain-depth contract.
from .domain_depth import ui_capability_surface_contract as field_service_management_ui_capability_surface_contract
from .domain_depth import domain_capability_surface_contract as field_service_management_domain_capability_surface_contract
from .field_operations import FIELD_WORKFORCE_UI_SURFACES, field_service_management_workforce_capability_contract

_BASE_FIELD_SERVICE_MANAGEMENT_UI_CONTRACT = field_service_management_ui_contract
_BASE_FIELD_SERVICE_MANAGEMENT_RENDER_WORKBENCH = field_service_management_render_workbench


def field_service_management_ui_contract():
    base = dict(_BASE_FIELD_SERVICE_MANAGEMENT_UI_CONTRACT())
    full = field_service_management_ui_capability_surface_contract()
    workforce = field_service_management_workforce_capability_contract()
    return {
        **base,
        'ok': base.get('ok') is True and full['ok'] and workforce['ok'],
        'full_capability_surface': full,
        'workforce_capability_surface': workforce,
        'operation_actions': full['operation_actions'],
        'rule_editors': full['rule_editors'],
        'parameter_editors': full['parameter_editors'],
        'advanced_panels': tuple(dict.fromkeys(tuple(full['advanced_panels']) + FIELD_WORKFORCE_UI_SURFACES)),
        'edge_case_queues': full['edge_case_queues'],
        'table_browsers': full['table_browsers'],
        'navigation_sections': tuple(dict.fromkeys(tuple(full['navigation_sections']) + FIELD_WORKFORCE_UI_SURFACES)),
        'live_workforce_map': True,
        'route_optimizer': True,
        'skill_assignment_console': True,
        'job_tool_requirement_planner': True,
        'task_dependency_board': True,
    }


def field_service_management_render_workbench(state=None):
    base = dict(_BASE_FIELD_SERVICE_MANAGEMENT_RENDER_WORKBENCH(state=state))
    full = field_service_management_ui_capability_surface_contract()
    workforce = field_service_management_workforce_capability_contract()
    return {
        **base,
        'ok': base.get('ok') is True and full['ok'] and workforce['ok'],
        'panels': tuple(dict.fromkeys(tuple(base.get('panels', ())) + full['navigation_sections'] + FIELD_WORKFORCE_UI_SURFACES)),
        'operation_actions': full['operation_actions'],
        'advanced_panels': tuple(dict.fromkeys(tuple(full['advanced_panels']) + FIELD_WORKFORCE_UI_SURFACES)),
        'edge_case_queues': full['edge_case_queues'],
        'table_browsers': full['table_browsers'],
        'agent_tools': full['agent_tools'],
        'workforce_capability_surface': workforce,
    }
