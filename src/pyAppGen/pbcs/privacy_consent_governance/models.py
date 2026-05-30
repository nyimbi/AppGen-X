"""Owned model metadata for the privacy_consent_governance PBC."""

from __future__ import annotations

PBC_KEY = 'privacy_consent_governance'


def _field(name: str, field_type: str, **kwargs) -> dict:
    return {'name': name, 'type': field_type, **kwargs}


def _base_fields(*extra_fields: dict) -> tuple[dict, ...]:
    return (
        _field('id', 'text', primary_key=True, nullable=False),
        _field('tenant', 'text', required=True),
        _field('code', 'text', required=True, searchable=True),
        *extra_fields,
        _field('status', 'text', required=True, default='draft'),
        _field('payload', 'json', required=False),
        _field('created_at', 'datetime', required=True),
        _field('updated_at', 'datetime', required=True),
    )


TABLE_DEFINITIONS = (
    {
        'logical_table': 'data_subject',
        'table': f'{PBC_KEY}_data_subject',
        'title': 'Data Subject Registry',
        'fields': _base_fields(
            _field('subject_identifier', 'text', required=True),
            _field('region', 'text', required=True),
            _field('email', 'text', required=False),
        ),
        'relationships': (),
    },
    {
        'logical_table': 'consent_capture',
        'table': f'{PBC_KEY}_consent_capture',
        'title': 'Consent Capture Ledger',
        'fields': _base_fields(
            _field('data_subject_id', 'text', required=True, references=f'{PBC_KEY}_data_subject.id'),
            _field('purpose_code', 'text', required=True),
            _field('lawful_basis_code', 'text', required=True),
            _field('channel', 'text', required=True),
            _field('consent_state', 'text', required=True),
        ),
        'relationships': ({'field': 'data_subject_id', 'target_table': f'{PBC_KEY}_data_subject', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},),
    },
    {
        'logical_table': 'consent_preference',
        'table': f'{PBC_KEY}_consent_preference',
        'title': 'Preference Center State',
        'fields': _base_fields(
            _field('data_subject_id', 'text', required=True, references=f'{PBC_KEY}_data_subject.id'),
            _field('channel', 'text', required=True),
            _field('preference_state', 'text', required=True),
        ),
        'relationships': ({'field': 'data_subject_id', 'target_table': f'{PBC_KEY}_data_subject', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},),
    },
    {
        'logical_table': 'consent_revocation',
        'table': f'{PBC_KEY}_consent_revocation',
        'title': 'Consent Revocation Ledger',
        'fields': _base_fields(
            _field('consent_capture_id', 'text', required=True, references=f'{PBC_KEY}_consent_capture.id'),
            _field('revocation_reason', 'text', required=True),
        ),
        'relationships': ({'field': 'consent_capture_id', 'target_table': f'{PBC_KEY}_consent_capture', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},),
    },
    {
        'logical_table': 'processing_purpose',
        'table': f'{PBC_KEY}_processing_purpose',
        'title': 'Processing Purpose Registry',
        'fields': _base_fields(
            _field('data_category', 'text', required=True),
            _field('purpose_owner', 'text', required=True),
        ),
        'relationships': (),
    },
    {
        'logical_table': 'lawful_basis_registry',
        'table': f'{PBC_KEY}_lawful_basis_registry',
        'title': 'Lawful Basis Registry',
        'fields': _base_fields(
            _field('purpose_code', 'text', required=True),
            _field('jurisdiction', 'text', required=True),
            _field('basis_type', 'text', required=True),
        ),
        'relationships': (),
    },
    {
        'logical_table': 'privacy_notice',
        'table': f'{PBC_KEY}_privacy_notice',
        'title': 'Privacy Notice Catalog',
        'fields': _base_fields(
            _field('notice_family', 'text', required=True),
            _field('locale', 'text', required=True),
        ),
        'relationships': (),
    },
    {
        'logical_table': 'policy_version',
        'table': f'{PBC_KEY}_policy_version',
        'title': 'Policy Version Register',
        'fields': _base_fields(
            _field('notice_id', 'text', required=True, references=f'{PBC_KEY}_privacy_notice.id'),
            _field('version_label', 'text', required=True),
            _field('effective_from', 'datetime', required=True),
        ),
        'relationships': ({'field': 'notice_id', 'target_table': f'{PBC_KEY}_privacy_notice', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},),
    },
    {
        'logical_table': 'dsar_case',
        'table': f'{PBC_KEY}_dsar_case',
        'title': 'Data Subject Request Case',
        'fields': _base_fields(
            _field('data_subject_id', 'text', required=True, references=f'{PBC_KEY}_data_subject.id'),
            _field('request_type', 'text', required=True),
            _field('due_at', 'datetime', required=True),
        ),
        'relationships': ({'field': 'data_subject_id', 'target_table': f'{PBC_KEY}_data_subject', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},),
    },
    {
        'logical_table': 'dsar_task',
        'table': f'{PBC_KEY}_dsar_task',
        'title': 'DSAR Work Queue',
        'fields': _base_fields(
            _field('dsar_case_id', 'text', required=True, references=f'{PBC_KEY}_dsar_case.id'),
            _field('owner', 'text', required=True),
            _field('task_type', 'text', required=True),
        ),
        'relationships': ({'field': 'dsar_case_id', 'target_table': f'{PBC_KEY}_dsar_case', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},),
    },
    {
        'logical_table': 'erasure_case',
        'table': f'{PBC_KEY}_erasure_case',
        'title': 'Erasure Approval Case',
        'fields': _base_fields(
            _field('data_subject_id', 'text', required=True, references=f'{PBC_KEY}_data_subject.id'),
            _field('legal_hold_state', 'text', required=True),
            _field('decision', 'text', required=True),
        ),
        'relationships': ({'field': 'data_subject_id', 'target_table': f'{PBC_KEY}_data_subject', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},),
    },
    {
        'logical_table': 'retention_schedule',
        'table': f'{PBC_KEY}_retention_schedule',
        'title': 'Retention Schedule Register',
        'fields': _base_fields(
            _field('data_category', 'text', required=True),
            _field('retention_days', 'integer', required=True),
            _field('legal_basis', 'text', required=True),
        ),
        'relationships': (),
    },
    {
        'logical_table': 'retention_decision',
        'table': f'{PBC_KEY}_retention_decision',
        'title': 'Retention Decision Ledger',
        'fields': _base_fields(
            _field('retention_schedule_id', 'text', required=True, references=f'{PBC_KEY}_retention_schedule.id'),
            _field('decision', 'text', required=True),
        ),
        'relationships': ({'field': 'retention_schedule_id', 'target_table': f'{PBC_KEY}_retention_schedule', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},),
    },
    {
        'logical_table': 'cross_border_restriction',
        'table': f'{PBC_KEY}_cross_border_restriction',
        'title': 'Cross-Border Restriction Matrix',
        'fields': _base_fields(
            _field('destination_country', 'text', required=True),
            _field('transfer_mechanism', 'text', required=True),
            _field('restriction_level', 'text', required=True),
        ),
        'relationships': (),
    },
    {
        'logical_table': 'disclosure_event',
        'table': f'{PBC_KEY}_disclosure_event',
        'title': 'Third-Party Disclosure Ledger',
        'fields': _base_fields(
            _field('data_subject_id', 'text', required=True, references=f'{PBC_KEY}_data_subject.id'),
            _field('recipient', 'text', required=True),
            _field('jurisdiction', 'text', required=True),
        ),
        'relationships': ({'field': 'data_subject_id', 'target_table': f'{PBC_KEY}_data_subject', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},),
    },
    {
        'logical_table': 'audit_proof',
        'table': f'{PBC_KEY}_audit_proof',
        'title': 'Audit Proof Catalog',
        'fields': _base_fields(
            _field('control_name', 'text', required=True),
            _field('proof_hash', 'text', required=True),
            _field('proof_scope', 'text', required=True),
        ),
        'relationships': (),
    },
    {
        'logical_table': 'ai_document_intake',
        'table': f'{PBC_KEY}_ai_document_intake',
        'title': 'AI Document Intake',
        'fields': _base_fields(
            _field('document_digest', 'text', required=True),
            _field('document_kind', 'text', required=True),
        ),
        'relationships': (),
    },
    {
        'logical_table': 'ai_instruction_plan',
        'table': f'{PBC_KEY}_ai_instruction_plan',
        'title': 'AI Instruction Plan',
        'fields': _base_fields(
            _field('document_intake_id', 'text', required=True, references=f'{PBC_KEY}_ai_document_intake.id'),
            _field('target_operation', 'text', required=True),
            _field('confirmation_required', 'boolean', required=True),
        ),
        'relationships': ({'field': 'document_intake_id', 'target_table': f'{PBC_KEY}_ai_document_intake', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},),
    },
    {
        'logical_table': 'appgen_outbox_event',
        'table': f'{PBC_KEY}_appgen_outbox_event',
        'title': 'AppGen-X Outbox Event',
        'fields': (
            _field('id', 'text', primary_key=True, nullable=False),
            _field('tenant', 'text', required=True),
            _field('event_type', 'text', required=True),
            _field('idempotency_key', 'text', required=True),
            _field('payload', 'json', required=True),
            _field('created_at', 'datetime', required=True),
            _field('updated_at', 'datetime', required=True),
        ),
        'relationships': (),
    },
    {
        'logical_table': 'appgen_inbox_event',
        'table': f'{PBC_KEY}_appgen_inbox_event',
        'title': 'AppGen-X Inbox Event',
        'fields': (
            _field('id', 'text', primary_key=True, nullable=False),
            _field('tenant', 'text', required=True),
            _field('event_type', 'text', required=True),
            _field('idempotency_key', 'text', required=True),
            _field('payload', 'json', required=True),
            _field('created_at', 'datetime', required=True),
            _field('updated_at', 'datetime', required=True),
        ),
        'relationships': (),
    },
    {
        'logical_table': 'appgen_dead_letter_event',
        'table': f'{PBC_KEY}_appgen_dead_letter_event',
        'title': 'Dead Letter Evidence',
        'fields': (
            _field('id', 'text', primary_key=True, nullable=False),
            _field('tenant', 'text', required=True),
            _field('event_type', 'text', required=True),
            _field('idempotency_key', 'text', required=True),
            _field('payload', 'json', required=True),
            _field('reason', 'text', required=True),
            _field('created_at', 'datetime', required=True),
            _field('updated_at', 'datetime', required=True),
        ),
        'relationships': (),
    },
)

OWNED_TABLES = tuple(table['table'] for table in TABLE_DEFINITIONS)
BUSINESS_TABLES = tuple(table['table'] for table in TABLE_DEFINITIONS if 'appgen_' not in table['logical_table'])
RUNTIME_TABLES = tuple(table for table in OWNED_TABLES if 'appgen_' in table)
MODELS = tuple(
    {
        'class_name': ''.join(part.capitalize() for part in table['logical_table'].split('_')),
        'table': table['table'],
        'fields': table['fields'],
        'relationships': table['relationships'],
    }
    for table in TABLE_DEFINITIONS
)


def owned_table_index() -> dict[str, dict]:
    return {table['table']: table for table in TABLE_DEFINITIONS}


def database_model_contract() -> dict:
    return {
        'format': 'appgen.privacy-consent-governance-model-contract.v2',
        'ok': True,
        'pbc': PBC_KEY,
        'owned_tables': OWNED_TABLES,
        'business_tables': BUSINESS_TABLES,
        'runtime_tables': RUNTIME_TABLES,
        'models': MODELS,
        'shared_table_access': False,
        'side_effects': (),
    }


def model_manifest() -> dict:
    schema_tables = tuple(table['table'] for table in TABLE_DEFINITIONS)
    model_tables = tuple(model['table'] for model in MODELS)
    missing_models = tuple(table for table in schema_tables if table not in model_tables)
    external_models = tuple(table for table in model_tables if not table.startswith(f'{PBC_KEY}_'))
    relationship_targets = tuple(
        rel.get('target_table')
        for table in TABLE_DEFINITIONS
        for rel in table.get('relationships', ())
        if rel.get('target_table')
    )
    cross_pbc_relationships = tuple(target for target in relationship_targets if not target.startswith(f'{PBC_KEY}_'))
    return {
        'ok': bool(schema_tables)
        and bool(model_tables)
        and not missing_models
        and not external_models
        and not cross_pbc_relationships,
        'pbc': PBC_KEY,
        'schema_tables': schema_tables,
        'model_tables': model_tables,
        'missing_models': missing_models,
        'external_models': external_models,
        'cross_pbc_relationships': cross_pbc_relationships,
        'relationship_targets': relationship_targets,
        'side_effects': (),
    }


def instantiate_model(table_name: str, values: dict | None = None) -> dict:
    table = owned_table_index().get(table_name)
    if table is None:
        return {'ok': False, 'reason': 'unknown_model', 'table': table_name, 'side_effects': ()}
    supplied = dict(values or {})
    field_names = tuple(field['name'] for field in table['fields'])
    return {
        'ok': table_name.startswith(f'{PBC_KEY}_') and bool(field_names),
        'pbc': PBC_KEY,
        'model': ''.join(part.capitalize() for part in table['logical_table'].split('_')),
        'table': table_name,
        'fields': field_names,
        'payload': {field: supplied.get(field) for field in field_names},
        'side_effects': (),
    }


def smoke_test() -> dict:
    manifest = model_manifest()
    first_table = manifest['model_tables'][0] if manifest['model_tables'] else None
    instance = instantiate_model(first_table, {'id': '1'}) if first_table else {'ok': False}
    return {
        'ok': manifest['ok'] and instance.get('ok') is True,
        'manifest': manifest,
        'instance': instance,
        'side_effects': (),
    }
