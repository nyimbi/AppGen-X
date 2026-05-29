"""Executable runtime contract for the privacy_consent_governance PBC."""

from __future__ import annotations

from copy import deepcopy
import hashlib
from datetime import datetime, timezone

from .config import ALLOWED_DATABASE_BACKENDS, DOMAIN_PARAMETER_SCHEMA, DOMAIN_RULE_SCHEMA, REQUIRED_EVENT_TOPIC
from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_OPERATIONS,
    DOMAIN_PARAMETERS,
    DOMAIN_RULES,
    domain_depth_contract,
    domain_depth_smoke_test,
)
from .events import CONSUMED as PRIVACY_CONSENT_GOVERNANCE_CONSUMED_EVENT_TYPES
from .events import EMITTED as PRIVACY_CONSENT_GOVERNANCE_EMITTED_EVENT_TYPES
from .models import BUSINESS_TABLES, OWNED_TABLES, PBC_KEY, RUNTIME_TABLES

PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES = OWNED_TABLES
PRIVACY_CONSENT_GOVERNANCE_RUNTIME_TABLES = RUNTIME_TABLES
PRIVACY_CONSENT_GOVERNANCE_BUSINESS_TABLES = BUSINESS_TABLES
PRIVACY_CONSENT_GOVERNANCE_ALLOWED_DATABASE_BACKENDS = ALLOWED_DATABASE_BACKENDS
PRIVACY_CONSENT_GOVERNANCE_REQUIRED_EVENT_TOPIC = REQUIRED_EVENT_TOPIC
PRIVACY_CONSENT_GOVERNANCE_STANDARD_FEATURE_KEYS = (
    'configuration_schema',
    'rule_engine',
    'parameter_engine',
    'owned_schema_migrations_models',
    'appgen_x_outbox_inbox_eventing',
    'idempotent_handlers',
    'retry_dead_letter_evidence',
    'permissions',
    'seed_data',
    'workbench',
    'agentic_document_instruction_intake',
    'governed_datastore_crud',
    'ai_agent_task_assistance',
    'configuration_workbench',
    'continuous_release_assurance',
    'standalone_app_surface',
)
PRIVACY_CONSENT_GOVERNANCE_RUNTIME_CAPABILITY_KEYS = (
    'consent_capture',
    'purpose_registry',
    'lawful_basis_registry',
    'data_subject_rights',
    'preference_center',
    'policy_versioning',
    'retention_management',
    'cross_border_restrictions',
    'audit_proof_management',
    'agent_document_instruction_crud_planning',
    'standalone_routes_and_workbench',
    'release_audit_evidence',
)
PRIVACY_CONSENT_GOVERNANCE_UI_FRAGMENT_KEYS = (
    'PrivacyConsentGovernanceWorkbench',
    'PrivacyConsentGovernanceRightsCenter',
    'PrivacyConsentGovernanceReleaseBoard',
    'PrivacyConsentGovernanceAssistantPanel',
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _copy(state: dict) -> dict:
    copied = deepcopy(state)
    copied['idempotency_keys'] = set(state.get('idempotency_keys', set()))
    return copied


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _table_bucket(state: dict, table: str) -> dict:
    return state.setdefault('records', {}).setdefault(table, {})


def _append_event(state: dict, event_type: str, payload: dict, *, tenant: str) -> None:
    envelope = {
        'id': f'evt-{_digest((event_type, payload))[:12]}',
        'tenant': tenant,
        'event_type': event_type,
        'idempotency_key': f'{PBC_KEY}:{event_type}:{payload.get("id", payload.get("code", tenant))}',
        'payload': dict(payload),
        'created_at': _now(),
        'updated_at': _now(),
    }
    _table_bucket(state, f'{PBC_KEY}_appgen_outbox_event')[envelope['id']] = envelope
    state['outbox'].append(envelope)


def _upsert_record(state: dict, table: str, payload: dict, *, event_type: str | None = None) -> dict:
    next_state = _copy(state)
    bucket = _table_bucket(next_state, table)
    record_id = str(payload.get('id') or payload.get('code') or _digest((table, payload))[:12])
    record = {
        'id': record_id,
        'tenant': payload.get('tenant', 'tenant_demo'),
        'code': payload.get('code', record_id.upper()),
        'status': payload.get('status', 'active'),
        'payload': dict(payload),
        'created_at': payload.get('created_at', _now()),
        'updated_at': _now(),
    }
    for key, value in payload.items():
        if key not in record:
            record[key] = value
    bucket[record_id] = record
    if event_type:
        _append_event(next_state, event_type, record, tenant=record['tenant'])
    return {'ok': True, 'state': next_state, 'record': record, 'table': table, 'side_effects': ()}


def privacy_consent_governance_empty_state() -> dict:
    return {
        'records': {table: {} for table in PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES},
        'configuration': {},
        'parameters': {},
        'rules': {},
        'schema_extensions': {},
        'inbox': [],
        'outbox': [],
        'dead_letter': [],
        'idempotency_keys': set(),
    }


def privacy_consent_governance_configure_runtime(state: dict, config: dict) -> dict:
    next_state = _copy(state)
    ok = (
        config.get('database_backend') in PRIVACY_CONSENT_GOVERNANCE_ALLOWED_DATABASE_BACKENDS
        and config.get('event_topic', PRIVACY_CONSENT_GOVERNANCE_REQUIRED_EVENT_TOPIC)
        == PRIVACY_CONSENT_GOVERNANCE_REQUIRED_EVENT_TOPIC
    )
    next_state['configuration'] = {
        **dict(config),
        'ok': ok,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
    }
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}


def privacy_consent_governance_set_parameter(state: dict, name: str, value) -> dict:
    next_state = _copy(state)
    schema = next((item for item in DOMAIN_PARAMETER_SCHEMA if item['key'] == name), None)
    bounded = bool(schema) and schema['minimum'] <= value <= schema['maximum'] if isinstance(value, (int, float)) else bool(schema)
    next_state['parameters'][name] = {
        'name': name,
        'value': value,
        'scope': schema['scope'] if schema else None,
        'bounded': bounded,
    }
    return {'ok': bool(schema) and bounded, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}


def privacy_consent_governance_register_rule(state: dict, rule: dict) -> dict:
    next_state = _copy(state)
    rule_id = rule.get('rule_id', 'privacy_rule')
    known_rule = any(item['rule_id'] == rule_id for item in DOMAIN_RULE_SCHEMA)
    compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}
    next_state['rules'][rule_id] = compiled
    return {'ok': known_rule, 'state': next_state, 'rule': compiled, 'side_effects': ()}


def privacy_consent_governance_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    next_state = _copy(state)
    owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}


def privacy_consent_governance_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    next_state = _copy(state)
    idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if simulate_failure or event.get('event_type') not in PRIVACY_CONSENT_GOVERNANCE_CONSUMED_EVENT_TYPES:
        dead = {
            'id': event.get('event_id', f'dead-{len(next_state["dead_letter"])+1}'),
            'tenant': event.get('payload', {}).get('tenant', 'tenant_demo'),
            'event_type': event.get('event_type'),
            'idempotency_key': idem,
            'payload': dict(event.get('payload', {})),
            'reason': 'unsupported_event' if not simulate_failure else 'simulated_failure',
            'created_at': _now(),
            'updated_at': _now(),
        }
        _table_bucket(next_state, f'{PBC_KEY}_appgen_dead_letter_event')[dead['id']] = dead
        next_state['dead_letter'].append(dead)
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter': dead, 'side_effects': ()}
    inbox = {
        'id': event.get('event_id', f'inbox-{len(next_state["inbox"])+1}'),
        'tenant': event.get('payload', {}).get('tenant', 'tenant_demo'),
        'event_type': event.get('event_type'),
        'idempotency_key': idem,
        'payload': dict(event.get('payload', {})),
        'created_at': _now(),
        'updated_at': _now(),
    }
    _table_bucket(next_state, f'{PBC_KEY}_appgen_inbox_event')[inbox['id']] = inbox
    next_state['inbox'].append(inbox)
    return {'ok': True, 'duplicate': False, 'state': next_state, 'inbox_event': inbox, 'side_effects': ()}


def privacy_consent_governance_register_data_subject(state: dict, payload: dict) -> dict:
    return _upsert_record(state, f'{PBC_KEY}_data_subject', payload)


def privacy_consent_governance_capture_consent(state: dict, payload: dict) -> dict:
    payload = {**dict(payload), 'consent_state': payload.get('consent_state', 'granted')}
    return _upsert_record(state, f'{PBC_KEY}_consent_capture', payload, event_type='ConsentCaptured')


def privacy_consent_governance_manage_preference_center(state: dict, payload: dict) -> dict:
    return _upsert_record(state, f'{PBC_KEY}_consent_preference', payload)


def privacy_consent_governance_revoke_consent(state: dict, payload: dict) -> dict:
    result = _upsert_record(state, f'{PBC_KEY}_consent_revocation', payload, event_type='ConsentRevoked')
    next_state = result['state']
    capture_id = payload.get('consent_capture_id')
    if capture_id and capture_id in _table_bucket(next_state, f'{PBC_KEY}_consent_capture'):
        _table_bucket(next_state, f'{PBC_KEY}_consent_capture')[capture_id]['consent_state'] = 'revoked'
        _table_bucket(next_state, f'{PBC_KEY}_consent_capture')[capture_id]['updated_at'] = _now()
    return {**result, 'state': next_state}


def privacy_consent_governance_register_processing_purpose(state: dict, payload: dict) -> dict:
    return _upsert_record(state, f'{PBC_KEY}_processing_purpose', payload)


def privacy_consent_governance_register_lawful_basis(state: dict, payload: dict) -> dict:
    return _upsert_record(state, f'{PBC_KEY}_lawful_basis_registry', payload)


def privacy_consent_governance_publish_policy_version(state: dict, payload: dict) -> dict:
    next_state = _copy(state)
    notice_payload = {
        'id': payload.get('notice_id', f'notice-{payload.get("id", payload.get("code", "policy"))}'),
        'tenant': payload.get('tenant', 'tenant_demo'),
        'code': payload.get('notice_code', payload.get('code', 'NOTICE')),
        'notice_family': payload.get('notice_family', 'privacy-policy'),
        'locale': payload.get('locale', 'en-KE'),
    }
    notice_result = _upsert_record(next_state, f'{PBC_KEY}_privacy_notice', notice_payload)
    return _upsert_record(notice_result['state'], f'{PBC_KEY}_policy_version', payload, event_type='PolicyVersionPublished')


def privacy_consent_governance_open_dsar(state: dict, payload: dict) -> dict:
    payload = {**dict(payload), 'status': payload.get('status', 'open')}
    return _upsert_record(state, f'{PBC_KEY}_dsar_case', payload, event_type='DsarOpened')


def privacy_consent_governance_assign_dsar_task(state: dict, payload: dict) -> dict:
    payload = {**dict(payload), 'status': payload.get('status', 'assigned')}
    return _upsert_record(state, f'{PBC_KEY}_dsar_task', payload)


def privacy_consent_governance_approve_erasure(state: dict, payload: dict) -> dict:
    payload = {**dict(payload), 'decision': payload.get('decision', 'approved')}
    return _upsert_record(state, f'{PBC_KEY}_erasure_case', payload, event_type='ErasureApproved')


def privacy_consent_governance_register_retention_schedule(state: dict, payload: dict) -> dict:
    return _upsert_record(state, f'{PBC_KEY}_retention_schedule', payload)


def privacy_consent_governance_record_retention_decision(state: dict, payload: dict) -> dict:
    return _upsert_record(state, f'{PBC_KEY}_retention_decision', payload)


def privacy_consent_governance_register_cross_border_restriction(state: dict, payload: dict) -> dict:
    return _upsert_record(state, f'{PBC_KEY}_cross_border_restriction', payload)


def privacy_consent_governance_record_disclosure_event(state: dict, payload: dict) -> dict:
    return _upsert_record(state, f'{PBC_KEY}_disclosure_event', payload)


def privacy_consent_governance_record_audit_proof(state: dict, payload: dict) -> dict:
    return _upsert_record(state, f'{PBC_KEY}_audit_proof', payload, event_type='AuditProofRecorded')


def privacy_consent_governance_intake_ai_document(state: dict, payload: dict) -> dict:
    return _upsert_record(state, f'{PBC_KEY}_ai_document_intake', payload)


def privacy_consent_governance_plan_ai_instruction(state: dict, payload: dict) -> dict:
    payload = {**dict(payload), 'confirmation_required': payload.get('confirmation_required', True)}
    return _upsert_record(state, f'{PBC_KEY}_ai_instruction_plan', payload, event_type='AIInstructionPlanned')


def privacy_consent_governance_command_data_subject_profile(state: dict, payload: dict) -> dict:
    return privacy_consent_governance_register_data_subject(state, payload)


def privacy_consent_governance_parse_document_instruction(document: str, instruction: str) -> dict:
    document_text = f'{document} {instruction}'.lower()
    table_hints = []
    operation_hints = []
    keyword_map = (
        ('consent', f'{PBC_KEY}_consent_capture', 'capture_consent'),
        ('revocation', f'{PBC_KEY}_consent_revocation', 'revoke_consent'),
        ('preference', f'{PBC_KEY}_consent_preference', 'manage_preference_center'),
        ('lawful basis', f'{PBC_KEY}_lawful_basis_registry', 'register_lawful_basis'),
        ('policy', f'{PBC_KEY}_policy_version', 'publish_policy_version'),
        ('dsar', f'{PBC_KEY}_dsar_case', 'open_dsar'),
        ('erasure', f'{PBC_KEY}_erasure_case', 'approve_erasure'),
        ('retention', f'{PBC_KEY}_retention_schedule', 'register_retention_schedule'),
        ('cross-border', f'{PBC_KEY}_cross_border_restriction', 'register_cross_border_restriction'),
        ('audit', f'{PBC_KEY}_audit_proof', 'record_audit_proof'),
    )
    for keyword, table, operation in keyword_map:
        if keyword in document_text:
            table_hints.append(table)
            operation_hints.append(operation)
    if not table_hints:
        table_hints.extend((f'{PBC_KEY}_ai_document_intake', f'{PBC_KEY}_ai_instruction_plan'))
        operation_hints.append('plan_ai_instruction')
    return {
        'ok': True,
        'candidate_tables': tuple(dict.fromkeys(table_hints)),
        'candidate_operations': tuple(dict.fromkeys(operation_hints)),
        'instruction': instruction,
        'document_digest': _digest(document),
        'requires_human_confirmation': True,
        'side_effects': (),
    }


def privacy_consent_governance_run_advanced_assessment(state: dict, payload: dict | None = None) -> dict:
    snapshot = privacy_consent_governance_build_workbench_view(state, tenant=(payload or {}).get('tenant', 'tenant_demo'))
    risk_score = round(
        min(1.0, 0.45 + 0.05 * snapshot['cards'][2]['value'] + 0.03 * snapshot['cards'][6]['value']),
        4,
    )
    return {
        'ok': True,
        'score': risk_score,
        'explanations': (
            'policy_versioning_bound',
            'cross_border_guardrail_visible',
            'audit_proof_surface_ready',
        ),
        'advanced_capabilities': DOMAIN_ADVANCED_CAPABILITIES,
        'payload': dict(payload or {}),
        'side_effects': (),
    }


def privacy_consent_governance_query_workbench(state: dict, filters: dict | None = None) -> dict:
    tenant = (filters or {}).get('tenant', 'tenant_demo')
    return {
        'ok': True,
        'filters': dict(filters or {}),
        'workbench': privacy_consent_governance_build_workbench_view(state, tenant=tenant),
        'side_effects': (),
    }


def privacy_consent_governance_permissions_contract() -> dict:
    from .permissions import permission_manifest

    return permission_manifest()


def privacy_consent_governance_build_workbench_view(state: dict | None = None, tenant: str = 'tenant_demo') -> dict:
    state = state or privacy_consent_governance_empty_state()
    counts = {
        'data_subjects': len(_table_bucket(state, f'{PBC_KEY}_data_subject')),
        'consents': len(_table_bucket(state, f'{PBC_KEY}_consent_capture')),
        'revocations': len(_table_bucket(state, f'{PBC_KEY}_consent_revocation')),
        'policy_versions': len(_table_bucket(state, f'{PBC_KEY}_policy_version')),
        'dsars': len(_table_bucket(state, f'{PBC_KEY}_dsar_case')),
        'erasures': len(_table_bucket(state, f'{PBC_KEY}_erasure_case')),
        'restrictions': len(_table_bucket(state, f'{PBC_KEY}_cross_border_restriction')),
        'audit_proofs': len(_table_bucket(state, f'{PBC_KEY}_audit_proof')),
        'instruction_plans': len(_table_bucket(state, f'{PBC_KEY}_ai_instruction_plan')),
        'events': len(state.get('outbox', ())) + len(state.get('inbox', ())),
    }
    configuration_hash = _digest(state.get('configuration', {})) if state.get('configuration') else None
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'tenant': tenant,
        'cards': (
            {'key': 'consents', 'value': counts['consents'], 'fragment': 'PrivacyConsentGovernanceWorkbench'},
            {'key': 'revocations', 'value': counts['revocations'], 'fragment': 'PrivacyConsentGovernanceRightsCenter'},
            {'key': 'dsars', 'value': counts['dsars'], 'fragment': 'PrivacyConsentGovernanceRightsCenter'},
            {'key': 'policy_versions', 'value': counts['policy_versions'], 'fragment': 'PrivacyConsentGovernanceReleaseBoard'},
            {'key': 'restrictions', 'value': counts['restrictions'], 'fragment': 'PrivacyConsentGovernanceReleaseBoard'},
            {'key': 'audit_proofs', 'value': counts['audit_proofs'], 'fragment': 'PrivacyConsentGovernanceReleaseBoard'},
            {'key': 'instruction_plans', 'value': counts['instruction_plans'], 'fragment': 'PrivacyConsentGovernanceAssistantPanel'},
            {'key': 'events', 'value': counts['events'], 'fragment': 'PrivacyConsentGovernanceReleaseBoard'},
        ),
        'queues': {
            'open_dsars': tuple(_table_bucket(state, f'{PBC_KEY}_dsar_case').values()),
            'erasure_cases': tuple(_table_bucket(state, f'{PBC_KEY}_erasure_case').values()),
            'cross_border_restrictions': tuple(_table_bucket(state, f'{PBC_KEY}_cross_border_restriction').values()),
        },
        'configuration_bound': bool(state.get('configuration')),
        'configuration_hash': configuration_hash,
        'rules_bound': tuple(sorted(state.get('rules', {}))),
        'parameters_bound': tuple(sorted(state.get('parameters', {}))),
        'owned_tables': PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }


def privacy_consent_governance_verify_owned_table_boundary(references: tuple[str, ...] | list[str]) -> dict:
    allowed = set(PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES) | {'api_dependency', 'projection_dependency'}
    foreign = tuple(ref for ref in references if ref not in allowed and not str(ref).startswith(f'{PBC_KEY}_'))
    return {
        'ok': not foreign,
        'foreign_references': foreign,
        'allowed_dependency_modes': ('api', 'event', 'projection'),
        'side_effects': (),
    }


def privacy_consent_governance_build_schema_contract() -> dict:
    from .schema_contract import build_schema_contract

    return build_schema_contract()


def privacy_consent_governance_build_service_contract() -> dict:
    from .service_contract import build_service_contract

    return build_service_contract()


def privacy_consent_governance_build_api_contract() -> dict:
    from .routes import api_route_contracts

    return api_route_contracts()


def privacy_consent_governance_build_release_evidence() -> dict:
    from .release_evidence import build_release_evidence

    return build_release_evidence()


def privacy_consent_governance_runtime_smoke() -> dict:
    state = privacy_consent_governance_empty_state()
    configured = privacy_consent_governance_configure_runtime(
        state,
        {
            'database_backend': 'postgresql',
            'event_topic': PRIVACY_CONSENT_GOVERNANCE_REQUIRED_EVENT_TOPIC,
            'retry_limit': 5,
            'default_policy_family': 'global-privacy',
        },
    )
    state = configured['state']
    parameter = privacy_consent_governance_set_parameter(state, 'workbench_limit', 100)
    state = parameter['state']
    rule = privacy_consent_governance_register_rule(state, {'rule_id': 'lawful_basis_required', 'scope': 'consent'})
    state = rule['state']
    subject = privacy_consent_governance_register_data_subject(
        state,
        {
            'id': 'subject-smoke',
            'tenant': 'tenant-smoke',
            'code': 'SUBJECT-SMOKE',
            'subject_identifier': 'customer-smoke',
            'region': 'KE',
        },
    )
    state = subject['state']
    consent = privacy_consent_governance_capture_consent(
        state,
        {
            'id': 'consent-smoke',
            'tenant': 'tenant-smoke',
            'code': 'CONSENT-SMOKE',
            'data_subject_id': 'subject-smoke',
            'purpose_code': 'MARKETING_EMAIL',
            'lawful_basis_code': 'CONSENT',
            'channel': 'email',
        },
    )
    state = consent['state']
    dsar = privacy_consent_governance_open_dsar(
        state,
        {
            'id': 'dsar-smoke',
            'tenant': 'tenant-smoke',
            'code': 'DSAR-SMOKE',
            'data_subject_id': 'subject-smoke',
            'request_type': 'access',
            'due_at': '2026-06-30T00:00:00Z',
        },
    )
    state = dsar['state']
    received = privacy_consent_governance_receive_event(
        state,
        {'event_type': PRIVACY_CONSENT_GOVERNANCE_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1', 'payload': {'tenant': 'tenant-smoke'}},
    )
    duplicate = privacy_consent_governance_receive_event(
        received['state'],
        {'event_type': PRIVACY_CONSENT_GOVERNANCE_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1', 'payload': {'tenant': 'tenant-smoke'}},
    )
    dead = privacy_consent_governance_receive_event(
        duplicate['state'],
        {'event_type': 'UnexpectedEvent', 'event_id': 'evt-bad', 'payload': {'tenant': 'tenant-smoke'}},
    )
    parsed = privacy_consent_governance_parse_document_instruction('Consent revocation form', 'Plan revocation and audit proof updates')
    workbench = privacy_consent_governance_build_workbench_view(dead['state'], tenant='tenant-smoke')
    advanced = privacy_consent_governance_run_advanced_assessment(dead['state'], {'tenant': 'tenant-smoke'})
    boundary = privacy_consent_governance_verify_owned_table_boundary(PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES + ('foreign_table',))
    return {
        'format': 'appgen.privacy-consent-governance-runtime-smoke.v2',
        'ok': configured['ok']
        and parameter['ok']
        and rule['ok']
        and subject['ok']
        and consent['ok']
        and dsar['ok']
        and received['ok']
        and duplicate.get('duplicate') is True
        and dead['ok'] is False
        and parsed['ok']
        and workbench['ok']
        and advanced['ok']
        and boundary['ok'] is False,
        'state': dead['state'],
        'workbench': workbench,
        'advanced': advanced,
        'blocking_gaps': (),
        'side_effects': (),
    }


def privacy_consent_governance_runtime_capabilities() -> dict:
    smoke = privacy_consent_governance_runtime_smoke()
    domain = domain_depth_contract()
    domain_smoke = domain_depth_smoke_test()
    operations = (
        'configure_runtime',
        'set_parameter',
        'register_rule',
        'register_schema_extension',
        'receive_event',
        'build_workbench_view',
        'build_schema_contract',
        'build_service_contract',
        'build_api_contract',
        'build_release_evidence',
        'permissions_contract',
        'verify_owned_table_boundary',
        'command_data_subject_profile',
        'parse_document_instruction',
        'run_advanced_assessment',
        *DOMAIN_OPERATIONS,
    )
    return {
        'format': 'appgen.privacy-consent-governance-runtime-capabilities.v2',
        'ok': smoke['ok'] and domain_smoke['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': 'src/pyAppGen/pbcs/privacy_consent_governance',
        'owned_tables': PRIVACY_CONSENT_GOVERNANCE_OWNED_TABLES,
        'runtime_tables': PRIVACY_CONSENT_GOVERNANCE_RUNTIME_TABLES,
        'allowed_database_backends': PRIVACY_CONSENT_GOVERNANCE_ALLOWED_DATABASE_BACKENDS,
        'capabilities': PRIVACY_CONSENT_GOVERNANCE_RUNTIME_CAPABILITY_KEYS,
        'standard_features': PRIVACY_CONSENT_GOVERNANCE_STANDARD_FEATURE_KEYS,
        'advanced_capabilities': tuple(DOMAIN_ADVANCED_CAPABILITIES),
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'domain_depth_smoke': domain_smoke,
        'side_effects': (),
    }
