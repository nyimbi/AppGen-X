"""UI fragments for the planning_budgeting_forecasting PBC."""
PBC_KEY = 'planning_budgeting_forecasting'
from .app_surface import single_pbc_planning_budgeting_forecasting_app_contract
UI_FRAGMENTS = ('PlanningBudgetingForecastingWorkbench', 'PlanningBudgetingForecastingDetail', 'PlanningBudgetingForecastingAssistantPanel')


def planning_budgeting_forecasting_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('planning_budgeting_forecasting.read', 'planning_budgeting_forecasting.create', 'planning_budgeting_forecasting.update', 'planning_budgeting_forecasting.approve', 'planning_budgeting_forecasting.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def planning_budgeting_forecasting_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('planning_budgeting_forecasting.read', 'planning_budgeting_forecasting.create', 'planning_budgeting_forecasting.update', 'planning_budgeting_forecasting.approve', 'planning_budgeting_forecasting.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': planning_budgeting_forecasting_ui_contract()['ok'] and planning_budgeting_forecasting_render_workbench()['ok'], 'side_effects': ()}

# Full UI capability surface bound to the world-class domain-depth contract.
from .domain_depth import ui_capability_surface_contract as planning_budgeting_forecasting_ui_capability_surface_contract
from .domain_depth import domain_capability_surface_contract as planning_budgeting_forecasting_domain_capability_surface_contract

_BASE_PLANNING_BUDGETING_FORECASTING_UI_CONTRACT = planning_budgeting_forecasting_ui_contract
_BASE_PLANNING_BUDGETING_FORECASTING_RENDER_WORKBENCH = planning_budgeting_forecasting_render_workbench


def planning_budgeting_forecasting_forms_contract():
    from .app_surface import planning_budgeting_forecasting_forms_contract as _forms
    return _forms()

def planning_budgeting_forecasting_wizards_contract():
    from .app_surface import planning_budgeting_forecasting_wizards_contract as _wizards
    return _wizards()

def planning_budgeting_forecasting_controls_contract():
    from .app_surface import planning_budgeting_forecasting_controls_contract as _controls
    return _controls()


def planning_budgeting_forecasting_ui_contract():
    base = dict(_BASE_PLANNING_BUDGETING_FORECASTING_UI_CONTRACT())
    full = planning_budgeting_forecasting_ui_capability_surface_contract()
    return {
        **base,
        'ok': base.get('ok') is True and full['ok'],
        'full_capability_surface': full,
        'operation_actions': full['operation_actions'],
        'rule_editors': full['rule_editors'],
        'parameter_editors': full['parameter_editors'],
        'advanced_panels': full['advanced_panels'],
        'edge_case_queues': full['edge_case_queues'],
        'table_browsers': full['table_browsers'],
        'navigation_sections': full['navigation_sections'], 'forms': planning_budgeting_forecasting_forms_contract()['forms'], 'wizards': planning_budgeting_forecasting_wizards_contract()['wizards'], 'controls': planning_budgeting_forecasting_controls_contract()['controls'], 'single_pbc_app': single_pbc_planning_budgeting_forecasting_app_contract(),
    }


def planning_budgeting_forecasting_render_workbench(state=None):
    base = dict(_BASE_PLANNING_BUDGETING_FORECASTING_RENDER_WORKBENCH(state=state))
    full = planning_budgeting_forecasting_ui_capability_surface_contract()
    return {
        **base,
        'ok': base.get('ok') is True and full['ok'],
        'panels': tuple(dict.fromkeys(tuple(base.get('panels', ())) + full['navigation_sections'])),
        'operation_actions': full['operation_actions'],
        'advanced_panels': full['advanced_panels'],
        'edge_case_queues': full['edge_case_queues'],
        'table_browsers': full['table_browsers'],
        'agent_tools': full['agent_tools'], 'forms': planning_budgeting_forecasting_forms_contract()['forms'], 'wizards': planning_budgeting_forecasting_wizards_contract()['wizards'], 'controls': planning_budgeting_forecasting_controls_contract()['controls'], 'single_pbc_app': single_pbc_planning_budgeting_forecasting_app_contract(),
    }


def standalone_ui_smoke_test():
    contract = planning_budgeting_forecasting_ui_contract()
    rendered = planning_budgeting_forecasting_render_workbench()
    return {'ok': contract['ok'] and rendered['ok'] and bool(contract['forms']) and bool(contract['wizards']) and bool(contract['controls']) and contract['single_pbc_app']['ok'], 'contract': contract, 'rendered': rendered, 'side_effects': ()}
