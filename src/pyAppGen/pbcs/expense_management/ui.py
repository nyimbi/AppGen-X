"""UI fragments for the expense_management PBC."""
PBC_KEY = 'expense_management'
UI_FRAGMENTS = ('ExpenseManagementWorkbench', 'ExpenseManagementDetail', 'ExpenseManagementAssistantPanel')


def expense_management_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('expense_management.read', 'expense_management.create', 'expense_management.update', 'expense_management.approve', 'expense_management.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def expense_management_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('expense_management.read', 'expense_management.create', 'expense_management.update', 'expense_management.approve', 'expense_management.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': expense_management_ui_contract()['ok'] and expense_management_render_workbench()['ok'], 'side_effects': ()}

# Full UI capability surface bound to the world-class domain-depth contract.
from .domain_depth import ui_capability_surface_contract as expense_management_ui_capability_surface_contract
from .domain_depth import domain_capability_surface_contract as expense_management_domain_capability_surface_contract

_BASE_EXPENSE_MANAGEMENT_UI_CONTRACT = expense_management_ui_contract
_BASE_EXPENSE_MANAGEMENT_RENDER_WORKBENCH = expense_management_render_workbench


def expense_management_ui_contract():
    base = dict(_BASE_EXPENSE_MANAGEMENT_UI_CONTRACT())
    full = expense_management_ui_capability_surface_contract()
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


def expense_management_render_workbench(state=None):
    base = dict(_BASE_EXPENSE_MANAGEMENT_RENDER_WORKBENCH(state=state))
    full = expense_management_ui_capability_surface_contract()
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
