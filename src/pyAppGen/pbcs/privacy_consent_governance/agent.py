"""Agent and chatbot assistance for the privacy_consent_governance PBC."""

from __future__ import annotations

import hashlib

from .domain_depth import DOMAIN_OPERATIONS
from .models import BUSINESS_TABLES, OWNED_TABLES, PBC_KEY

AI_TABLES = (f'{PBC_KEY}_ai_document_intake', f'{PBC_KEY}_ai_instruction_plan')


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _candidate_tables_and_operations(document: str, instruction: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    document_text = f'{document} {instruction}'.lower()
    matches = []
    operations = []
    keyword_map = (
        ('consent', f'{PBC_KEY}_consent_capture', 'capture_consent'),
        ('revoke', f'{PBC_KEY}_consent_revocation', 'revoke_consent'),
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
            matches.append(table)
            operations.append(operation)
    if not matches:
        matches.extend(AI_TABLES)
        operations.append('plan_ai_instruction')
    return tuple(dict.fromkeys(matches)), tuple(dict.fromkeys(operations))


def agent_skill_manifest() -> dict:
    skills = tuple(
        {
            'name': name,
            'scope': PBC_KEY,
            'description': f'{name} for privacy consent governance',
            'requires_confirmation_for_mutation': True,
            'uses_appgen_event_contract': True,
            'stream_engine_picker_visible': False,
        }
        for name in (
            'privacy_consent_governance_guide_user',
            'privacy_consent_governance_plan_crud',
            'privacy_consent_governance_read_records',
            'privacy_consent_governance_mutation_preview',
        )
    )
    return {'ok': True, 'pbc': PBC_KEY, 'skills': skills, 'side_effects': ()}


def chatbot_interface_contract() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'entrypoint': f'/assistant/pbc/{PBC_KEY}',
        'single_agent_contribution': f'{PBC_KEY}_skills',
        'capabilities': (
            'task_guidance',
            'document_instruction_intake',
            'governed_datastore_crud',
            'mutation_preview',
            'privacy_plan_generation',
        ),
        'side_effects': (),
    }


def document_instruction_plan(document: str, instruction: str) -> dict:
    candidate_tables, candidate_operations = _candidate_tables_and_operations(document, instruction)
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'document_digest': _digest(document),
        'instruction': instruction,
        'candidate_tables': candidate_tables,
        'candidate_operations': candidate_operations,
        'requires_human_confirmation': True,
        'crud_preview': {
            'create': AI_TABLES,
            'update': candidate_tables[:2],
            'delete': (),
            'event_contract': 'AppGen-X',
        },
        'side_effects': (),
    }


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    target = table or OWNED_TABLES[0]
    if not str(target).startswith(f'{PBC_KEY}_'):
        return {'ok': False, 'reason': 'foreign_table_rejected', 'table': target, 'side_effects': ()}
    mutation = action in ('create', 'update', 'delete')
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'action': action,
        'table': target,
        'payload': dict(payload or {}),
        'requires_confirmation': mutation,
        'event_contract': 'AppGen-X',
        'side_effects': (),
    }


def instruction_crud_plan(document: str, instruction: str) -> dict:
    plan = document_instruction_plan(document, instruction)
    mutations = tuple(datastore_crud_plan('create', table=table) for table in plan['candidate_tables'][:2])
    return {
        'ok': plan['ok'] and all(item['ok'] for item in mutations),
        'plan': plan,
        'mutations': mutations,
        'side_effects': (),
    }


def composed_agent_contribution() -> dict:
    namespace = f'{PBC_KEY}_skills'
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'single_agent_skill_namespace': namespace,
        'dsl_tools': (namespace, f'{PBC_KEY}_crud', f'{PBC_KEY}_documents', f'{PBC_KEY}_planning'),
        'operations': DOMAIN_OPERATIONS,
        'owned_tables': BUSINESS_TABLES,
        'side_effects': (),
    }


def smoke_test() -> dict:
    plan = document_instruction_plan('Consent policy redline', 'Publish a new consent policy version and attach audit proof')
    crud = datastore_crud_plan('create')
    foreign = datastore_crud_plan('update', table='foreign_table')
    return {
        'ok': agent_skill_manifest()['ok']
        and chatbot_interface_contract()['ok']
        and plan['ok']
        and crud['ok']
        and foreign['ok'] is False
        and instruction_crud_plan('Consent', 'Update preference center')['ok']
        and composed_agent_contribution()['ok'],
        'side_effects': (),
    }
