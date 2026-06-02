"""Permission descriptors for the privacy_consent_governance PBC."""

from __future__ import annotations

PBC_KEY = 'privacy_consent_governance'
PERMISSIONS = (
    'privacy_consent_governance.read',
    'privacy_consent_governance.create',
    'privacy_consent_governance.update',
    'privacy_consent_governance.approve',
    'privacy_consent_governance.admin',
)
ACTION_PERMISSIONS = {
    'query_workbench': 'privacy_consent_governance.read',
    'query_api_contract': 'privacy_consent_governance.read',
    'query_schema_contract': 'privacy_consent_governance.read',
    'query_service_contract': 'privacy_consent_governance.read',
    'query_release_evidence': 'privacy_consent_governance.read',
    'query_permissions_contract': 'privacy_consent_governance.read',
    'query_agent_surface': 'privacy_consent_governance.read',
    'command_configure_runtime': 'privacy_consent_governance.admin',
    'command_set_parameter': 'privacy_consent_governance.admin',
    'command_register_rule': 'privacy_consent_governance.admin',
    'command_receive_event': 'privacy_consent_governance.admin',
    'command_register_data_subject': 'privacy_consent_governance.create',
    'command_capture_consent': 'privacy_consent_governance.create',
    'command_manage_preference_center': 'privacy_consent_governance.update',
    'command_revoke_consent': 'privacy_consent_governance.update',
    'command_register_processing_purpose': 'privacy_consent_governance.update',
    'command_register_lawful_basis': 'privacy_consent_governance.update',
    'command_publish_policy_version': 'privacy_consent_governance.approve',
    'command_open_dsar': 'privacy_consent_governance.create',
    'command_assign_dsar_task': 'privacy_consent_governance.update',
    'command_approve_erasure': 'privacy_consent_governance.approve',
    'command_register_retention_schedule': 'privacy_consent_governance.update',
    'command_record_retention_decision': 'privacy_consent_governance.approve',
    'command_register_cross_border_restriction': 'privacy_consent_governance.approve',
    'command_record_disclosure_event': 'privacy_consent_governance.update',
    'command_record_audit_proof': 'privacy_consent_governance.admin',
    'command_intake_ai_document': 'privacy_consent_governance.update',
    'command_plan_ai_instruction': 'privacy_consent_governance.update',
}


def permission_manifest() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'permissions': PERMISSIONS,
        'rbac_roles': ('reader', 'operator', 'approver', 'admin'),
        'action_permissions': ACTION_PERMISSIONS,
        'side_effects': (),
    }


def authorize(actor: str, permission: str) -> dict:
    allowed = permission in PERMISSIONS
    return {
        'ok': allowed,
        'allowed': allowed,
        'actor': actor,
        'permission': permission,
        'side_effects': (),
    }


def smoke_test() -> dict:
    return {
        'ok': permission_manifest()['ok'] and authorize('system', PERMISSIONS[0])['allowed'],
        'side_effects': (),
    }
