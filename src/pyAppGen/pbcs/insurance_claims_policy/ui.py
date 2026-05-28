"""UI fragments for the insurance_claims_policy PBC."""
PBC_KEY = 'insurance_claims_policy'
UI_FRAGMENTS = ('InsuranceClaimsPolicyWorkbench', 'InsuranceClaimsPolicyDetail', 'InsuranceClaimsPolicyAssistantPanel')


def insurance_claims_policy_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('insurance_claims_policy.read', 'insurance_claims_policy.create', 'insurance_claims_policy.update', 'insurance_claims_policy.approve', 'insurance_claims_policy.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def insurance_claims_policy_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('insurance_claims_policy.read', 'insurance_claims_policy.create', 'insurance_claims_policy.update', 'insurance_claims_policy.approve', 'insurance_claims_policy.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': insurance_claims_policy_ui_contract()['ok'] and insurance_claims_policy_render_workbench()['ok'], 'side_effects': ()}

# Full UI capability surface bound to the world-class domain-depth contract.
from .domain_depth import ui_capability_surface_contract as insurance_claims_policy_ui_capability_surface_contract
from .domain_depth import domain_capability_surface_contract as insurance_claims_policy_domain_capability_surface_contract

_BASE_INSURANCE_CLAIMS_POLICY_UI_CONTRACT = insurance_claims_policy_ui_contract
_BASE_INSURANCE_CLAIMS_POLICY_RENDER_WORKBENCH = insurance_claims_policy_render_workbench


def insurance_claims_policy_ui_contract():
    base = dict(_BASE_INSURANCE_CLAIMS_POLICY_UI_CONTRACT())
    full = insurance_claims_policy_ui_capability_surface_contract()
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


def insurance_claims_policy_render_workbench(state=None):
    base = dict(_BASE_INSURANCE_CLAIMS_POLICY_RENDER_WORKBENCH(state=state))
    full = insurance_claims_policy_ui_capability_surface_contract()
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
