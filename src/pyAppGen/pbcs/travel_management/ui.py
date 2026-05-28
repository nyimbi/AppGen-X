"""UI fragments for the travel_management PBC."""
PBC_KEY = 'travel_management'
UI_FRAGMENTS = ('TravelManagementWorkbench', 'TravelManagementDetail', 'TravelManagementAssistantPanel')


def travel_management_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('travel_management.read', 'travel_management.create', 'travel_management.update', 'travel_management.approve', 'travel_management.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def travel_management_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('travel_management.read', 'travel_management.create', 'travel_management.update', 'travel_management.approve', 'travel_management.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': travel_management_ui_contract()['ok'] and travel_management_render_workbench()['ok'], 'side_effects': ()}
