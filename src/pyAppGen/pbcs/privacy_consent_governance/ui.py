"""UI fragments for the privacy_consent_governance PBC."""
PBC_KEY = 'privacy_consent_governance'
UI_FRAGMENTS = ('PrivacyConsentGovernanceWorkbench', 'PrivacyConsentGovernanceDetail', 'PrivacyConsentGovernanceAssistantPanel')


def privacy_consent_governance_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('privacy_consent_governance.read', 'privacy_consent_governance.create', 'privacy_consent_governance.update', 'privacy_consent_governance.approve', 'privacy_consent_governance.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def privacy_consent_governance_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('privacy_consent_governance.read', 'privacy_consent_governance.create', 'privacy_consent_governance.update', 'privacy_consent_governance.approve', 'privacy_consent_governance.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': privacy_consent_governance_ui_contract()['ok'] and privacy_consent_governance_render_workbench()['ok'], 'side_effects': ()}
