"""UI fragments for the contract_lifecycle PBC."""
PBC_KEY = 'contract_lifecycle'
UI_FRAGMENTS = ('ContractLifecycleWorkbench', 'ContractLifecycleDetail', 'ContractLifecycleAssistantPanel')


def contract_lifecycle_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('contract_lifecycle.read', 'contract_lifecycle.create', 'contract_lifecycle.update', 'contract_lifecycle.approve', 'contract_lifecycle.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def contract_lifecycle_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('contract_lifecycle.read', 'contract_lifecycle.create', 'contract_lifecycle.update', 'contract_lifecycle.approve', 'contract_lifecycle.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': contract_lifecycle_ui_contract()['ok'] and contract_lifecycle_render_workbench()['ok'], 'side_effects': ()}
