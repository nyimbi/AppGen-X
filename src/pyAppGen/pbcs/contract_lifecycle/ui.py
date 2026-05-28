"""UI fragments for the contract_lifecycle PBC."""
PBC_KEY = 'contract_lifecycle'
UI_FRAGMENTS = ('ContractLifecycleWorkbench', 'ContractLifecycleDetail', 'ContractLifecycleAssistantPanel')


def contract_lifecycle_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('contract_lifecycle.read', 'contract_lifecycle.create', 'contract_lifecycle.update', 'contract_lifecycle.approve', 'contract_lifecycle.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def contract_lifecycle_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('contract_lifecycle.read', 'contract_lifecycle.create', 'contract_lifecycle.update', 'contract_lifecycle.approve', 'contract_lifecycle.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': contract_lifecycle_ui_contract()['ok'] and contract_lifecycle_render_workbench()['ok'], 'side_effects': ()}

# Full UI capability surface bound to the world-class domain-depth contract.
from .domain_depth import ui_capability_surface_contract as contract_lifecycle_ui_capability_surface_contract
from .domain_depth import domain_capability_surface_contract as contract_lifecycle_domain_capability_surface_contract

_BASE_CONTRACT_LIFECYCLE_UI_CONTRACT = contract_lifecycle_ui_contract
_BASE_CONTRACT_LIFECYCLE_RENDER_WORKBENCH = contract_lifecycle_render_workbench


def contract_lifecycle_ui_contract():
    base = dict(_BASE_CONTRACT_LIFECYCLE_UI_CONTRACT())
    full = contract_lifecycle_ui_capability_surface_contract()
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


def contract_lifecycle_render_workbench(state=None):
    base = dict(_BASE_CONTRACT_LIFECYCLE_RENDER_WORKBENCH(state=state))
    full = contract_lifecycle_ui_capability_surface_contract()
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
