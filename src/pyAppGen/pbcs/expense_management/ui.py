"""UI fragments for the expense_management PBC."""
PBC_KEY = 'expense_management'
UI_FRAGMENTS = ('ExpenseManagementWorkbench', 'ExpenseManagementDetail', 'ExpenseManagementAssistantPanel')


def expense_management_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('expense_management.read', 'expense_management.create', 'expense_management.update', 'expense_management.approve', 'expense_management.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def expense_management_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('expense_management.read', 'expense_management.create', 'expense_management.update', 'expense_management.approve', 'expense_management.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': expense_management_ui_contract()['ok'] and expense_management_render_workbench()['ok'], 'side_effects': ()}
