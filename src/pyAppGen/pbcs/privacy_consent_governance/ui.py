"""UI fragments for the privacy_consent_governance PBC."""
PBC_KEY = 'privacy_consent_governance'
UI_FRAGMENTS = ('PrivacyConsentGovernanceWorkbench', 'PrivacyConsentGovernanceDetail', 'PrivacyConsentGovernanceAssistantPanel')


def privacy_consent_governance_ui_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': UI_FRAGMENTS, 'workbench_view': UI_FRAGMENTS[0], 'configuration_editor': True, 'action_permissions': ('privacy_consent_governance.read', 'privacy_consent_governance.create', 'privacy_consent_governance.update', 'privacy_consent_governance.approve', 'privacy_consent_governance.admin'), 'stream_engine_picker_visible': False, 'side_effects': ()}


def privacy_consent_governance_render_workbench(state=None):
    return {'ok': True, 'pbc': PBC_KEY, 'view': UI_FRAGMENTS[0], 'panels': ('overview','records','rules','agent'), 'configuration_editor': True, 'action_permissions': ('privacy_consent_governance.read', 'privacy_consent_governance.create', 'privacy_consent_governance.update', 'privacy_consent_governance.approve', 'privacy_consent_governance.admin'), 'side_effects': ()}


def smoke_test():
    return {'ok': privacy_consent_governance_ui_contract()['ok'] and privacy_consent_governance_render_workbench()['ok'], 'side_effects': ()}

# Full UI capability surface bound to the world-class domain-depth contract.
from .domain_depth import ui_capability_surface_contract as privacy_consent_governance_ui_capability_surface_contract
from .domain_depth import domain_capability_surface_contract as privacy_consent_governance_domain_capability_surface_contract

_BASE_PRIVACY_CONSENT_GOVERNANCE_UI_CONTRACT = privacy_consent_governance_ui_contract
_BASE_PRIVACY_CONSENT_GOVERNANCE_RENDER_WORKBENCH = privacy_consent_governance_render_workbench


def privacy_consent_governance_ui_contract():
    base = dict(_BASE_PRIVACY_CONSENT_GOVERNANCE_UI_CONTRACT())
    full = privacy_consent_governance_ui_capability_surface_contract()
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


def privacy_consent_governance_render_workbench(state=None):
    base = dict(_BASE_PRIVACY_CONSENT_GOVERNANCE_RENDER_WORKBENCH(state=state))
    full = privacy_consent_governance_ui_capability_surface_contract()
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
