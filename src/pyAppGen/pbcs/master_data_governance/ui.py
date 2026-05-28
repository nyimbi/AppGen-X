"""UI fragments for the master_data_governance PBC."""
PBC_KEY = 'master_data_governance'
UI_FRAGMENTS = ('MasterDataGovernanceWorkbench', 'MasterDataGovernanceDetail', 'MasterDataGovernanceAssistantPanel')


def master_data_governance_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('master_data_governance.read', 'master_data_governance.create', 'master_data_governance.update', 'master_data_governance.approve', 'master_data_governance.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def master_data_governance_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('master_data_governance.read', 'master_data_governance.create', 'master_data_governance.update', 'master_data_governance.approve', 'master_data_governance.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': master_data_governance_ui_contract()['ok'] and master_data_governance_render_workbench()['ok'], 'side_effects': ()}

# Full UI capability surface bound to the world-class domain-depth contract.
from .domain_depth import ui_capability_surface_contract as master_data_governance_ui_capability_surface_contract
from .domain_depth import domain_capability_surface_contract as master_data_governance_domain_capability_surface_contract

_BASE_MASTER_DATA_GOVERNANCE_UI_CONTRACT = master_data_governance_ui_contract
_BASE_MASTER_DATA_GOVERNANCE_RENDER_WORKBENCH = master_data_governance_render_workbench


def master_data_governance_ui_contract():
    base = dict(_BASE_MASTER_DATA_GOVERNANCE_UI_CONTRACT())
    full = master_data_governance_ui_capability_surface_contract()
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


def master_data_governance_render_workbench(state=None):
    base = dict(_BASE_MASTER_DATA_GOVERNANCE_RENDER_WORKBENCH(state=state))
    full = master_data_governance_ui_capability_surface_contract()
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
