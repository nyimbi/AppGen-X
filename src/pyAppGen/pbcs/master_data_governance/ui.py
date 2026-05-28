"""UI fragments for the master_data_governance PBC."""
PBC_KEY = 'master_data_governance'
UI_FRAGMENTS = ('MasterDataGovernanceWorkbench', 'MasterDataGovernanceDetail', 'MasterDataGovernanceAssistantPanel')


def master_data_governance_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('master_data_governance.read', 'master_data_governance.create', 'master_data_governance.update', 'master_data_governance.approve', 'master_data_governance.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def master_data_governance_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('master_data_governance.read', 'master_data_governance.create', 'master_data_governance.update', 'master_data_governance.approve', 'master_data_governance.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': master_data_governance_ui_contract()['ok'] and master_data_governance_render_workbench()['ok'], 'side_effects': ()}
