"""Command and query service layer for the privacy_consent_governance PBC."""

from __future__ import annotations

from .events import EVENT_CONTRACT
from .permissions import ACTION_PERMISSIONS
from . import runtime

_COMMAND_OPERATION_SPECS = (
    {'operation': 'command_configure_runtime', 'method': 'POST', 'path': '/api/pbc/privacy_consent_governance/runtime/configuration', 'owned_tables': (), 'handler': 'command_configure_runtime', 'emitted_event': None},
    {'operation': 'command_set_parameter', 'method': 'POST', 'path': '/api/pbc/privacy_consent_governance/runtime/parameters', 'owned_tables': (), 'handler': 'command_set_parameter', 'emitted_event': None},
    {'operation': 'command_register_rule', 'method': 'POST', 'path': '/api/pbc/privacy_consent_governance/runtime/rules', 'owned_tables': (), 'handler': 'command_register_rule', 'emitted_event': None},
    {'operation': 'command_receive_event', 'method': 'POST', 'path': '/api/pbc/privacy_consent_governance/events/inbox', 'owned_tables': (f'{runtime.PBC_KEY}_appgen_inbox_event', f'{runtime.PBC_KEY}_appgen_dead_letter_event'), 'handler': 'command_receive_event', 'emitted_event': None},
    {'operation': 'command_register_data_subject', 'method': 'POST', 'path': '/api/pbc/privacy_consent_governance/data-subjects', 'owned_tables': (f'{runtime.PBC_KEY}_data_subject',), 'handler': 'command_register_data_subject', 'emitted_event': None},
    {'operation': 'command_capture_consent', 'method': 'POST', 'path': '/api/pbc/privacy_consent_governance/consents/capture', 'owned_tables': (f'{runtime.PBC_KEY}_consent_capture', f'{runtime.PBC_KEY}_appgen_outbox_event'), 'handler': 'command_capture_consent', 'emitted_event': 'ConsentCaptured'},
    {'operation': 'command_manage_preference_center', 'method': 'POST', 'path': '/api/pbc/privacy_consent_governance/preferences', 'owned_tables': (f'{runtime.PBC_KEY}_consent_preference',), 'handler': 'command_manage_preference_center', 'emitted_event': None},
    {'operation': 'command_revoke_consent', 'method': 'POST', 'path': '/api/pbc/privacy_consent_governance/consents/revoke', 'owned_tables': (f'{runtime.PBC_KEY}_consent_revocation', f'{runtime.PBC_KEY}_consent_capture', f'{runtime.PBC_KEY}_appgen_outbox_event'), 'handler': 'command_revoke_consent', 'emitted_event': 'ConsentRevoked'},
    {'operation': 'command_register_processing_purpose', 'method': 'POST', 'path': '/api/pbc/privacy_consent_governance/processing-purposes', 'owned_tables': (f'{runtime.PBC_KEY}_processing_purpose',), 'handler': 'command_register_processing_purpose', 'emitted_event': None},
    {'operation': 'command_register_lawful_basis', 'method': 'POST', 'path': '/api/pbc/privacy_consent_governance/lawful-bases', 'owned_tables': (f'{runtime.PBC_KEY}_lawful_basis_registry',), 'handler': 'command_register_lawful_basis', 'emitted_event': None},
    {'operation': 'command_publish_policy_version', 'method': 'POST', 'path': '/api/pbc/privacy_consent_governance/policy-versions', 'owned_tables': (f'{runtime.PBC_KEY}_privacy_notice', f'{runtime.PBC_KEY}_policy_version', f'{runtime.PBC_KEY}_appgen_outbox_event'), 'handler': 'command_publish_policy_version', 'emitted_event': 'PolicyVersionPublished'},
    {'operation': 'command_open_dsar', 'method': 'POST', 'path': '/api/pbc/privacy_consent_governance/dsars', 'owned_tables': (f'{runtime.PBC_KEY}_dsar_case', f'{runtime.PBC_KEY}_appgen_outbox_event'), 'handler': 'command_open_dsar', 'emitted_event': 'DsarOpened'},
    {'operation': 'command_assign_dsar_task', 'method': 'POST', 'path': '/api/pbc/privacy_consent_governance/dsar-tasks', 'owned_tables': (f'{runtime.PBC_KEY}_dsar_task',), 'handler': 'command_assign_dsar_task', 'emitted_event': None},
    {'operation': 'command_approve_erasure', 'method': 'POST', 'path': '/api/pbc/privacy_consent_governance/erasures', 'owned_tables': (f'{runtime.PBC_KEY}_erasure_case', f'{runtime.PBC_KEY}_appgen_outbox_event'), 'handler': 'command_approve_erasure', 'emitted_event': 'ErasureApproved'},
    {'operation': 'command_register_retention_schedule', 'method': 'POST', 'path': '/api/pbc/privacy_consent_governance/retention-schedules', 'owned_tables': (f'{runtime.PBC_KEY}_retention_schedule',), 'handler': 'command_register_retention_schedule', 'emitted_event': None},
    {'operation': 'command_record_retention_decision', 'method': 'POST', 'path': '/api/pbc/privacy_consent_governance/retention-decisions', 'owned_tables': (f'{runtime.PBC_KEY}_retention_decision',), 'handler': 'command_record_retention_decision', 'emitted_event': None},
    {'operation': 'command_register_cross_border_restriction', 'method': 'POST', 'path': '/api/pbc/privacy_consent_governance/cross-border-restrictions', 'owned_tables': (f'{runtime.PBC_KEY}_cross_border_restriction',), 'handler': 'command_register_cross_border_restriction', 'emitted_event': None},
    {'operation': 'command_record_disclosure_event', 'method': 'POST', 'path': '/api/pbc/privacy_consent_governance/disclosures', 'owned_tables': (f'{runtime.PBC_KEY}_disclosure_event',), 'handler': 'command_record_disclosure_event', 'emitted_event': None},
    {'operation': 'command_record_audit_proof', 'method': 'POST', 'path': '/api/pbc/privacy_consent_governance/audit-proofs', 'owned_tables': (f'{runtime.PBC_KEY}_audit_proof', f'{runtime.PBC_KEY}_appgen_outbox_event'), 'handler': 'command_record_audit_proof', 'emitted_event': 'AuditProofRecorded'},
    {'operation': 'command_intake_ai_document', 'method': 'POST', 'path': '/api/pbc/privacy_consent_governance/documents', 'owned_tables': (f'{runtime.PBC_KEY}_ai_document_intake',), 'handler': 'command_intake_ai_document', 'emitted_event': None},
    {'operation': 'command_plan_ai_instruction', 'method': 'POST', 'path': '/api/pbc/privacy_consent_governance/instructions/plan', 'owned_tables': (f'{runtime.PBC_KEY}_ai_instruction_plan', f'{runtime.PBC_KEY}_appgen_outbox_event'), 'handler': 'command_plan_ai_instruction', 'emitted_event': 'AIInstructionPlanned'},
)
_QUERY_OPERATION_SPECS = (
    {'operation': 'query_workbench', 'method': 'GET', 'path': '/api/pbc/privacy_consent_governance/workbench', 'read_tables': runtime.PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES},
    {'operation': 'query_api_contract', 'method': 'GET', 'path': '/api/pbc/privacy_consent_governance/api-contract', 'read_tables': runtime.PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES},
    {'operation': 'query_schema_contract', 'method': 'GET', 'path': '/api/pbc/privacy_consent_governance/schema-contract', 'read_tables': runtime.PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES},
    {'operation': 'query_service_contract', 'method': 'GET', 'path': '/api/pbc/privacy_consent_governance/service-contract', 'read_tables': runtime.PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES},
    {'operation': 'query_release_evidence', 'method': 'GET', 'path': '/api/pbc/privacy_consent_governance/release-evidence', 'read_tables': runtime.PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES},
    {'operation': 'query_permissions_contract', 'method': 'GET', 'path': '/api/pbc/privacy_consent_governance/permissions', 'read_tables': runtime.PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES},
    {'operation': 'query_agent_surface', 'method': 'GET', 'path': '/api/pbc/privacy_consent_governance/agent', 'read_tables': runtime.PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES},
)
OPERATION_CONTRACTS = tuple(
    {
        **spec,
        'permission': ACTION_PERMISSIONS[spec['operation']],
        'operation_kind': 'command',
        'read_tables': (),
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'event_contract': 'AppGen-X',
        'idempotency_key': f'privacy_consent_governance:{spec["operation"]}:idempotency_key',
    }
    for spec in _COMMAND_OPERATION_SPECS
) + tuple(
    {
        **spec,
        'permission': ACTION_PERMISSIONS[spec['operation']],
        'operation_kind': 'query',
        'owned_tables': (),
        'handler': spec['operation'],
        'emitted_event': None,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'event_contract': 'AppGen-X',
        'idempotency_key': None,
    }
    for spec in _QUERY_OPERATION_SPECS
)


def service_operation_contracts() -> dict:
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item['operation_kind'] == 'command')
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item['operation_kind'] == 'query')
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS)
        and all(not item['read_tables'] for item in command_contracts)
        and all(not item['owned_tables'] for item in query_contracts),
        'pbc': runtime.PBC_KEY,
        'operations': tuple(item['operation'] for item in OPERATION_CONTRACTS),
        'command_operations': tuple(item['operation'] for item in command_contracts),
        'query_operations': tuple(item['operation'] for item in query_contracts),
        'contracts': OPERATION_CONTRACTS,
        'side_effects': (),
    }


def operation_plan(operation_name: str, payload: dict | None = None) -> dict:
    contract = next((item for item in OPERATION_CONTRACTS if item['operation'] == operation_name), None)
    if contract is None:
        return {'ok': False, 'reason': 'unknown_operation', 'operation': operation_name, 'side_effects': ()}
    supplied = dict(payload or {})
    return {
        'ok': True,
        'pbc': runtime.PBC_KEY,
        'operation': operation_name,
        'operation_kind': contract['operation_kind'],
        'route': {'method': contract['method'], 'path': contract['path']},
        'permission': contract['permission'],
        'owned_tables': contract['owned_tables'],
        'read_tables': contract['read_tables'],
        'emitted_event': contract['emitted_event'],
        'payload_keys': tuple(sorted(supplied)),
        'transaction_boundary': contract['transaction_boundary'],
        'event_contract': contract['event_contract'],
        'idempotency_key': contract['idempotency_key'],
        'side_effects': (),
    }


class PrivacyConsentGovernanceService:
    def __init__(self, state: dict | None = None):
        self.state = state or runtime.privacy_consent_governance_empty_state()

    def __getattr__(self, name: str):
        if name in service_operation_contracts()['command_operations']:
            return lambda payload=None, _name=name: self._command(_name, payload)
        if name in service_operation_contracts()['query_operations']:
            return lambda payload=None, _name=name: self._query(_name, payload)
        raise AttributeError(name)

    def _command(self, operation_name: str, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        plan = operation_plan(operation_name, payload)
        if not plan['ok']:
            return plan
        result = self._apply_command(operation_name, payload)
        if 'state' in result:
            self.state = result['state']
        return {
            'ok': result.get('ok') is True,
            'pbc': runtime.PBC_KEY,
            'operation': operation_name,
            'operation_kind': 'command',
            'payload': payload,
            'operation_contract': plan,
            'transaction_boundary': plan['transaction_boundary'],
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (plan['emitted_event'],) if plan['emitted_event'] else (),
            'result': result,
            'state': self.state,
            'side_effects': (),
        }

    def _query(self, operation_name: str, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        plan = operation_plan(operation_name, payload)
        if not plan['ok']:
            return plan
        result = self._apply_query(operation_name, payload)
        return {
            'ok': result.get('ok') is True,
            'pbc': runtime.PBC_KEY,
            'operation': operation_name,
            'operation_kind': 'query',
            'payload': payload,
            'operation_contract': plan,
            'transaction_boundary': plan['transaction_boundary'],
            'emits': (),
            'result': result,
            'state': self.state,
            'side_effects': (),
        }

    def _apply_command(self, operation_name: str, payload: dict) -> dict:
        record = payload.get('record', payload)
        command_handlers = {
            'command_configure_runtime': lambda: runtime.privacy_consent_governance_configure_runtime(self.state, payload['configuration']),
            'command_set_parameter': lambda: runtime.privacy_consent_governance_set_parameter(self.state, payload['name'], payload['value']),
            'command_register_rule': lambda: runtime.privacy_consent_governance_register_rule(self.state, payload['rule']),
            'command_receive_event': lambda: runtime.privacy_consent_governance_receive_event(self.state, payload['envelope'], simulate_failure=payload.get('simulate_failure', False)),
            'command_register_data_subject': lambda: runtime.privacy_consent_governance_register_data_subject(self.state, record),
            'command_capture_consent': lambda: runtime.privacy_consent_governance_capture_consent(self.state, record),
            'command_manage_preference_center': lambda: runtime.privacy_consent_governance_manage_preference_center(self.state, record),
            'command_revoke_consent': lambda: runtime.privacy_consent_governance_revoke_consent(self.state, record),
            'command_register_processing_purpose': lambda: runtime.privacy_consent_governance_register_processing_purpose(self.state, record),
            'command_register_lawful_basis': lambda: runtime.privacy_consent_governance_register_lawful_basis(self.state, record),
            'command_publish_policy_version': lambda: runtime.privacy_consent_governance_publish_policy_version(self.state, record),
            'command_open_dsar': lambda: runtime.privacy_consent_governance_open_dsar(self.state, record),
            'command_assign_dsar_task': lambda: runtime.privacy_consent_governance_assign_dsar_task(self.state, record),
            'command_approve_erasure': lambda: runtime.privacy_consent_governance_approve_erasure(self.state, record),
            'command_register_retention_schedule': lambda: runtime.privacy_consent_governance_register_retention_schedule(self.state, record),
            'command_record_retention_decision': lambda: runtime.privacy_consent_governance_record_retention_decision(self.state, record),
            'command_register_cross_border_restriction': lambda: runtime.privacy_consent_governance_register_cross_border_restriction(self.state, record),
            'command_record_disclosure_event': lambda: runtime.privacy_consent_governance_record_disclosure_event(self.state, record),
            'command_record_audit_proof': lambda: runtime.privacy_consent_governance_record_audit_proof(self.state, record),
            'command_intake_ai_document': lambda: runtime.privacy_consent_governance_intake_ai_document(self.state, record),
            'command_plan_ai_instruction': lambda: runtime.privacy_consent_governance_plan_ai_instruction(self.state, record),
        }
        if operation_name not in command_handlers:
            raise ValueError(f'Unsupported Privacy Consent Governance command: {operation_name}')
        return command_handlers[operation_name]()

    def _apply_query(self, operation_name: str, payload: dict) -> dict:
        if operation_name == 'query_workbench':
            return runtime.privacy_consent_governance_build_workbench_view(self.state, tenant=payload.get('tenant', 'tenant_demo'))
        if operation_name == 'query_api_contract':
            from .routes import api_route_contracts

            return api_route_contracts()
        if operation_name == 'query_schema_contract':
            from .schema_contract import build_schema_contract

            return build_schema_contract()
        if operation_name == 'query_service_contract':
            from .service_contract import build_service_contract

            return build_service_contract()
        if operation_name == 'query_release_evidence':
            from .release_evidence import build_release_evidence

            return build_release_evidence()
        if operation_name == 'query_permissions_contract':
            from .permissions import permission_manifest

            return permission_manifest()
        if operation_name == 'query_agent_surface':
            from .agent import composed_agent_contribution

            return composed_agent_contribution()
        raise ValueError(f'Unsupported Privacy Consent Governance query: {operation_name}')


def smoke_test() -> dict:
    service = PrivacyConsentGovernanceService()
    service.command_configure_runtime(
        {
            'configuration': {
                'database_backend': 'postgresql',
                'event_topic': 'appgen.privacy_consent_governance.events',
                'retry_limit': 5,
                'default_policy_family': 'global-privacy',
            }
        }
    )
    command = service.command_capture_consent(
        {
            'record': {
                'id': 'consent-service-smoke',
                'tenant': 'tenant-smoke',
                'code': 'CONSENT-SERVICE-SMOKE',
                'data_subject_id': 'subject-smoke',
                'purpose_code': 'MARKETING_EMAIL',
                'lawful_basis_code': 'CONSENT',
                'channel': 'email',
            }
        }
    )
    query = service.query_workbench({'tenant': 'tenant-smoke'})
    return {
        'ok': command['ok'] and query['ok'] and service_operation_contracts()['ok'],
        'command': command,
        'query': query,
        'side_effects': (),
    }
