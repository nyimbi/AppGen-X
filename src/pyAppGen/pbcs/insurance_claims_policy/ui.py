"""UI fragments for the insurance_claims_policy PBC."""
PBC_KEY = 'insurance_claims_policy'
UI_FRAGMENTS = ('InsuranceClaimsPolicyWorkbench', 'InsuranceClaimsPolicyDetail', 'InsuranceClaimsPolicyAssistantPanel')


def insurance_claims_policy_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('insurance_claims_policy.read', 'insurance_claims_policy.create', 'insurance_claims_policy.update', 'insurance_claims_policy.approve', 'insurance_claims_policy.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def insurance_claims_policy_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('insurance_claims_policy.read', 'insurance_claims_policy.create', 'insurance_claims_policy.update', 'insurance_claims_policy.approve', 'insurance_claims_policy.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': insurance_claims_policy_ui_contract()['ok'] and insurance_claims_policy_render_workbench()['ok'], 'side_effects': ()}
