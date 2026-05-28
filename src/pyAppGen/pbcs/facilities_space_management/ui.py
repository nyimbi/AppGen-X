"""UI fragments for the facilities_space_management PBC."""
PBC_KEY = 'facilities_space_management'
UI_FRAGMENTS = ('FacilitiesSpaceManagementWorkbench', 'FacilitiesSpaceManagementDetail', 'FacilitiesSpaceManagementAssistantPanel')


def facilities_space_management_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('facilities_space_management.read', 'facilities_space_management.create', 'facilities_space_management.update', 'facilities_space_management.approve', 'facilities_space_management.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def facilities_space_management_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('facilities_space_management.read', 'facilities_space_management.create', 'facilities_space_management.update', 'facilities_space_management.approve', 'facilities_space_management.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': facilities_space_management_ui_contract()['ok'] and facilities_space_management_render_workbench()['ok'], 'side_effects': ()}
