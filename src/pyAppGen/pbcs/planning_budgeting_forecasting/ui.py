"""UI fragments for the planning_budgeting_forecasting PBC."""
PBC_KEY = 'planning_budgeting_forecasting'
UI_FRAGMENTS = ('PlanningBudgetingForecastingWorkbench', 'PlanningBudgetingForecastingDetail', 'PlanningBudgetingForecastingAssistantPanel')


def planning_budgeting_forecasting_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('planning_budgeting_forecasting.read', 'planning_budgeting_forecasting.create', 'planning_budgeting_forecasting.update', 'planning_budgeting_forecasting.approve', 'planning_budgeting_forecasting.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def planning_budgeting_forecasting_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('planning_budgeting_forecasting.read', 'planning_budgeting_forecasting.create', 'planning_budgeting_forecasting.update', 'planning_budgeting_forecasting.approve', 'planning_budgeting_forecasting.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': planning_budgeting_forecasting_ui_contract()['ok'] and planning_budgeting_forecasting_render_workbench()['ok'], 'side_effects': ()}
