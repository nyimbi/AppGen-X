"""UI fragments for the grant_fund_accounting PBC."""
PBC_KEY = 'grant_fund_accounting'
UI_FRAGMENTS = ('GrantFundAccountingWorkbench', 'GrantFundAccountingDetail', 'GrantFundAccountingAssistantPanel')


def grant_fund_accounting_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('grant_fund_accounting.read', 'grant_fund_accounting.create', 'grant_fund_accounting.update', 'grant_fund_accounting.approve', 'grant_fund_accounting.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def grant_fund_accounting_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('grant_fund_accounting.read', 'grant_fund_accounting.create', 'grant_fund_accounting.update', 'grant_fund_accounting.approve', 'grant_fund_accounting.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': grant_fund_accounting_ui_contract()['ok'] and grant_fund_accounting_render_workbench()['ok'], 'side_effects': ()}
