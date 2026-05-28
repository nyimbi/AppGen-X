"""UI fragments for the legal_matter_management PBC."""
PBC_KEY = 'legal_matter_management'
UI_FRAGMENTS = ('LegalMatterManagementWorkbench', 'LegalMatterManagementDetail', 'LegalMatterManagementAssistantPanel')


def legal_matter_management_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('legal_matter_management.read', 'legal_matter_management.create', 'legal_matter_management.update', 'legal_matter_management.approve', 'legal_matter_management.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def legal_matter_management_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('legal_matter_management.read', 'legal_matter_management.create', 'legal_matter_management.update', 'legal_matter_management.approve', 'legal_matter_management.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': legal_matter_management_ui_contract()['ok'] and legal_matter_management_render_workbench()['ok'], 'side_effects': ()}
