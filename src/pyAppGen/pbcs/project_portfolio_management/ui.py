"""UI fragments for the project_portfolio_management PBC."""
PBC_KEY = 'project_portfolio_management'
UI_FRAGMENTS = ('ProjectPortfolioManagementWorkbench', 'ProjectPortfolioManagementDetail', 'ProjectPortfolioManagementAssistantPanel')


def project_portfolio_management_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('project_portfolio_management.read', 'project_portfolio_management.create', 'project_portfolio_management.update', 'project_portfolio_management.approve', 'project_portfolio_management.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def project_portfolio_management_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('project_portfolio_management.read', 'project_portfolio_management.create', 'project_portfolio_management.update', 'project_portfolio_management.approve', 'project_portfolio_management.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': project_portfolio_management_ui_contract()['ok'] and project_portfolio_management_render_workbench()['ok'], 'side_effects': ()}
