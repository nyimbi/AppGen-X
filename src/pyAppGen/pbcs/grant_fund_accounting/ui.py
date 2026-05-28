"""UI fragments for the grant_fund_accounting PBC."""
PBC_KEY = 'grant_fund_accounting'
UI_FRAGMENTS = ('GrantFundAccountingWorkbench', 'GrantFundAccountingDetail', 'GrantFundAccountingAssistantPanel')


def grant_fund_accounting_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('grant_fund_accounting.read', 'grant_fund_accounting.create', 'grant_fund_accounting.update', 'grant_fund_accounting.approve', 'grant_fund_accounting.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def grant_fund_accounting_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('grant_fund_accounting.read', 'grant_fund_accounting.create', 'grant_fund_accounting.update', 'grant_fund_accounting.approve', 'grant_fund_accounting.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': grant_fund_accounting_ui_contract()['ok'] and grant_fund_accounting_render_workbench()['ok'], 'side_effects': ()}

# Full UI capability surface bound to the world-class domain-depth contract.
from .domain_depth import ui_capability_surface_contract as grant_fund_accounting_ui_capability_surface_contract
from .domain_depth import domain_capability_surface_contract as grant_fund_accounting_domain_capability_surface_contract

_BASE_GRANT_FUND_ACCOUNTING_UI_CONTRACT = grant_fund_accounting_ui_contract
_BASE_GRANT_FUND_ACCOUNTING_RENDER_WORKBENCH = grant_fund_accounting_render_workbench


def grant_fund_accounting_ui_contract():
    base = dict(_BASE_GRANT_FUND_ACCOUNTING_UI_CONTRACT())
    full = grant_fund_accounting_ui_capability_surface_contract()
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
        'navigation_sections': full['navigation_sections'],
    }


def grant_fund_accounting_render_workbench(state=None):
    base = dict(_BASE_GRANT_FUND_ACCOUNTING_RENDER_WORKBENCH(state=state))
    full = grant_fund_accounting_ui_capability_surface_contract()
    return {
        **base,
        'ok': base.get('ok') is True and full['ok'],
        'panels': tuple(dict.fromkeys(tuple(base.get('panels', ())) + full['navigation_sections'])),
        'operation_actions': full['operation_actions'],
        'advanced_panels': full['advanced_panels'],
        'edge_case_queues': full['edge_case_queues'],
        'table_browsers': full['table_browsers'],
        'agent_tools': full['agent_tools'],
    }
