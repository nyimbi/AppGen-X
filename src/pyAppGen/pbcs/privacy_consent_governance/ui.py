"""UI contract and standalone workbench surface for the privacy_consent_governance PBC."""

from __future__ import annotations

from .domain_depth import ui_capability_surface_contract
from .permissions import ACTION_PERMISSIONS
from .runtime import (
    PRIVACY_CONSENT_GOVERNANCE_ALLOWED_DATABASE_BACKENDS,
    PRIVACY_CONSENT_GOVERNANCE_CONSUMED_EVENT_TYPES,
    PRIVACY_CONSENT_GOVERNANCE_EMITTED_EVENT_TYPES,
    PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES,
    PRIVACY_CONSENT_GOVERNANCE_REQUIRED_EVENT_TOPIC,
    PRIVACY_CONSENT_GOVERNANCE_RUNTIME_TABLES,
    privacy_consent_governance_build_workbench_view,
)

PBC_KEY = 'privacy_consent_governance'
UI_FRAGMENTS = (
    'PrivacyConsentGovernanceWorkbench',
    'PrivacyConsentGovernanceRightsCenter',
    'PrivacyConsentGovernanceReleaseBoard',
    'PrivacyConsentGovernanceAssistantPanel',
)
FORM_KEYS = (
    'consent_capture_form',
    'preference_center_form',
    'lawful_basis_form',
    'policy_version_form',
    'dsar_case_form',
    'erasure_case_form',
    'document_instruction_form',
)
WIZARD_KEYS = (
    'consent_capture_wizard',
    'dsar_resolution_wizard',
    'policy_publication_wizard',
)
CONTROL_KEYS = (
    'tenant_scope_picker',
    'purpose_basis_matrix',
    'preference_center_preview',
    'dsar_queue_board',
    'cross_border_banner',
    'audit_proof_drawer',
    'release_gate_banner',
)


def privacy_consent_governance_form_catalog() -> tuple[dict, ...]:
    return (
        {'key': 'consent_capture_form', 'title': 'Consent Capture', 'command': 'command_capture_consent', 'fields': ('data_subject_id', 'purpose_code', 'lawful_basis_code', 'channel', 'consent_state')},
        {'key': 'preference_center_form', 'title': 'Preference Center', 'command': 'command_manage_preference_center', 'fields': ('data_subject_id', 'channel', 'preference_state')},
        {'key': 'lawful_basis_form', 'title': 'Lawful Basis Registry', 'command': 'command_register_lawful_basis', 'fields': ('purpose_code', 'jurisdiction', 'basis_type')},
        {'key': 'policy_version_form', 'title': 'Policy Version', 'command': 'command_publish_policy_version', 'fields': ('notice_id', 'version_label', 'effective_from')},
        {'key': 'dsar_case_form', 'title': 'DSAR Intake', 'command': 'command_open_dsar', 'fields': ('data_subject_id', 'request_type', 'due_at')},
        {'key': 'erasure_case_form', 'title': 'Erasure Decision', 'command': 'command_approve_erasure', 'fields': ('data_subject_id', 'legal_hold_state', 'decision')},
        {'key': 'document_instruction_form', 'title': 'AI Document Planning', 'command': 'command_plan_ai_instruction', 'fields': ('document_intake_id', 'target_operation', 'confirmation_required')},
    )


def privacy_consent_governance_wizard_catalog() -> tuple[dict, ...]:
    return (
        {'key': 'consent_capture_wizard', 'steps': ('consent_capture_form', 'preference_center_form', 'lawful_basis_form'), 'goal': 'Capture consent with purpose and lawful basis evidence inside this package only.'},
        {'key': 'dsar_resolution_wizard', 'steps': ('dsar_case_form', 'erasure_case_form', 'document_instruction_form'), 'goal': 'Route one rights request through intake, erasure decisioning, and AI-assisted next actions.'},
        {'key': 'policy_publication_wizard', 'steps': ('policy_version_form', 'document_instruction_form'), 'goal': 'Publish a policy version with reviewable instruction planning and release evidence.'},
    )


def privacy_consent_governance_control_catalog() -> tuple[dict, ...]:
    return (
        {'key': 'tenant_scope_picker', 'type': 'selector', 'binds_to': 'tenant'},
        {'key': 'purpose_basis_matrix', 'type': 'matrix', 'binds_to': 'processing_purpose.lawful_basis_registry'},
        {'key': 'preference_center_preview', 'type': 'preview', 'binds_to': 'consent_preference'},
        {'key': 'dsar_queue_board', 'type': 'board', 'binds_to': 'dsar_case'},
        {'key': 'cross_border_banner', 'type': 'banner', 'binds_to': 'cross_border_restriction'},
        {'key': 'audit_proof_drawer', 'type': 'drawer', 'binds_to': 'audit_proof'},
        {'key': 'release_gate_banner', 'type': 'banner', 'binds_to': 'release_evidence'},
    )


def privacy_consent_governance_standalone_app_contract() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'app_id': 'privacy_consent_governance_one_pbc_app',
        'workbench_route': '/workbench/pbcs/privacy_consent_governance',
        'navigation': (
            {'key': 'overview', 'route': '/workbench/pbcs/privacy_consent_governance'},
            {'key': 'consents', 'route': '/workbench/pbcs/privacy_consent_governance/consents'},
            {'key': 'rights', 'route': '/workbench/pbcs/privacy_consent_governance/rights'},
            {'key': 'policy', 'route': '/workbench/pbcs/privacy_consent_governance/policy'},
            {'key': 'release', 'route': '/workbench/pbcs/privacy_consent_governance/release'},
        ),
        'forms': FORM_KEYS,
        'wizards': WIZARD_KEYS,
        'controls': CONTROL_KEYS,
        'single_agent_namespace': 'privacy_consent_governance_skills',
        'side_effects': (),
    }


def privacy_consent_governance_ui_contract() -> dict:
    coverage = ui_capability_surface_contract()
    return {
        'format': 'appgen.privacy-consent-governance-ui-contract.v2',
        'ok': coverage['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': 'src/pyAppGen/pbcs/privacy_consent_governance',
        'fragments': UI_FRAGMENTS,
        'routes': tuple(item['route'] for item in privacy_consent_governance_standalone_app_contract()['navigation']) + ('/workbench/pbcs/privacy_consent_governance',),
        'panels': (
            {'key': 'consents', 'fragment': 'PrivacyConsentGovernanceWorkbench', 'binds_to': ('privacy_consent_governance_consent_capture', 'privacy_consent_governance_consent_preference', 'privacy_consent_governance_consent_revocation'), 'commands': ('command_capture_consent', 'command_manage_preference_center', 'command_revoke_consent')},
            {'key': 'rights', 'fragment': 'PrivacyConsentGovernanceRightsCenter', 'binds_to': ('privacy_consent_governance_dsar_case', 'privacy_consent_governance_dsar_task', 'privacy_consent_governance_erasure_case'), 'commands': ('command_open_dsar', 'command_assign_dsar_task', 'command_approve_erasure')},
            {'key': 'policy', 'fragment': 'PrivacyConsentGovernanceReleaseBoard', 'binds_to': ('privacy_consent_governance_processing_purpose', 'privacy_consent_governance_lawful_basis_registry', 'privacy_consent_governance_policy_version'), 'commands': ('command_register_processing_purpose', 'command_register_lawful_basis', 'command_publish_policy_version')},
            {'key': 'release', 'fragment': 'PrivacyConsentGovernanceReleaseBoard', 'binds_to': PRIVACY_CONSENT_GOVERNANCE_RUNTIME_TABLES, 'commands': ('query_release_evidence', 'query_schema_contract', 'query_service_contract')},
            {'key': 'agent', 'fragment': 'PrivacyConsentGovernanceAssistantPanel', 'binds_to': ('privacy_consent_governance_ai_document_intake', 'privacy_consent_governance_ai_instruction_plan'), 'commands': ('command_intake_ai_document', 'command_plan_ai_instruction')},
        ),
        'forms': privacy_consent_governance_form_catalog(),
        'wizards': privacy_consent_governance_wizard_catalog(),
        'controls': privacy_consent_governance_control_catalog(),
        'standalone_app': privacy_consent_governance_standalone_app_contract(),
        'action_permissions': ACTION_PERMISSIONS,
        'configuration_editor': {
            'required_fields': ('database_backend', 'event_topic', 'retry_limit', 'default_policy_family', 'workbench_limit'),
            'allowed_database_backends': PRIVACY_CONSENT_GOVERNANCE_ALLOWED_DATABASE_BACKENDS,
            'required_event_topic': PRIVACY_CONSENT_GOVERNANCE_REQUIRED_EVENT_TOPIC,
            'event_contract': 'AppGen-X',
            'stream_engine_picker_visible': False,
            'user_eventing_choice': False,
        },
        'parameter_editor': {'numeric_parameters': ('dsar_sla_days', 'consent_reconfirmation_days', 'retention_review_days', 'cross_border_risk_threshold', 'auto_revocation_guard_days', 'workbench_limit'), 'bounded_supported_parameters': True},
        'rule_editor': {'rule_types': coverage['rule_editors'], 'required_fields': ('rule_id', 'scope', 'condition'), 'compiled_evidence_required': True},
        'event_surfaces': {
            'emits': PRIVACY_CONSENT_GOVERNANCE_EMITTED_EVENT_TYPES,
            'consumes': PRIVACY_CONSENT_GOVERNANCE_CONSUMED_EVENT_TYPES,
            'outbox_status': 'visible',
            'inbox_status': 'visible',
            'dead_letter_status': 'visible',
        },
        'binding_evidence': {
            'owned_tables': PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES,
            'runtime_tables': PRIVACY_CONSENT_GOVERNANCE_RUNTIME_TABLES,
            'shared_table_access': False,
            'event_contract': 'AppGen-X',
            'required_event_topic': PRIVACY_CONSENT_GOVERNANCE_REQUIRED_EVENT_TOPIC,
        },
        'full_capability_surface': coverage,
    }


def privacy_consent_governance_render_workbench(
    state: dict,
    *,
    tenant: str = 'tenant_demo',
    principal_permissions: tuple[str, ...] | None = None,
) -> dict:
    contract = privacy_consent_governance_ui_contract()
    shell = privacy_consent_governance_standalone_app_contract()
    snapshot = privacy_consent_governance_build_workbench_view(state, tenant=tenant)
    permissions = set(principal_permissions or tuple(sorted(set(contract['action_permissions'].values()))))
    visible_actions = tuple(
        action
        for action, required_permission in contract['action_permissions'].items()
        if required_permission in permissions
    )
    return {
        'format': 'appgen.privacy-consent-governance-workbench-render.v2',
        'ok': True,
        'tenant': tenant,
        'route': shell['workbench_route'],
        'shell': shell,
        'fragments': contract['fragments'],
        'navigation': shell['navigation'],
        'forms': contract['forms'],
        'wizards': contract['wizards'],
        'controls': contract['controls'],
        'workbench': snapshot,
        'cards': snapshot['cards'],
        'visible_actions': visible_actions,
        'locked_actions': tuple(action for action in contract['action_permissions'] if action not in visible_actions),
        'configuration_bound': snapshot['configuration_bound'],
        'configuration_hash': snapshot['configuration_hash'],
        'rules_bound': snapshot['rules_bound'],
        'parameters_bound': snapshot['parameters_bound'],
        'binding_evidence': {
            'owned_tables': snapshot['owned_tables'],
            'runtime_tables': PRIVACY_CONSENT_GOVERNANCE_RUNTIME_TABLES,
            'event_contract': snapshot['event_contract'],
        },
        'side_effects': (),
    }


def smoke_test() -> dict:
    rendered = privacy_consent_governance_render_workbench({}, tenant='tenant_smoke')
    contract = privacy_consent_governance_ui_contract()
    return {
        'ok': rendered['ok'] and contract['ok'] and bool(contract['forms']) and bool(contract['wizards']) and bool(contract['controls']),
        'rendered': rendered,
        'side_effects': (),
    }
