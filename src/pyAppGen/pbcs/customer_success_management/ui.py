"""UI fragments for the customer_success_management PBC."""
PBC_KEY = 'customer_success_management'
UI_FRAGMENTS = ('CustomerSuccessManagementWorkbench', 'CustomerSuccessManagementDetail', 'CustomerSuccessManagementAssistantPanel')


def customer_success_management_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('customer_success_management.read', 'customer_success_management.create', 'customer_success_management.update', 'customer_success_management.approve', 'customer_success_management.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def customer_success_management_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('customer_success_management.read', 'customer_success_management.create', 'customer_success_management.update', 'customer_success_management.approve', 'customer_success_management.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': customer_success_management_ui_contract()['ok'] and customer_success_management_render_workbench()['ok'], 'side_effects': ()}
