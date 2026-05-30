"""Governed assistant contribution for reinsurance_management."""

from __future__ import annotations

from .runtime import (
    PBC_KEY,
    REINSURANCE_MANAGEMENT_OWNED_TABLES,
    reinsurance_management_empty_state,
    reinsurance_management_parse_document_instruction,
)


def agent_skill_manifest() -> dict:
    skills = (
        {
            'name': f'{PBC_KEY}_guide_user',
            'scope': PBC_KEY,
            'description': 'Guide the operator through treaty, placement, and recovery workflows.',
            'requires_confirmation_for_mutation': True,
            'uses_appgen_event_contract': True,
            'stream_engine_picker_visible': False,
        },
        {
            'name': f'{PBC_KEY}_preview_document_ingest',
            'scope': PBC_KEY,
            'description': 'Preview treaty, bordereau, statement, and recovery document extraction.',
            'requires_confirmation_for_mutation': True,
            'uses_appgen_event_contract': True,
            'stream_engine_picker_visible': False,
        },
        {
            'name': f'{PBC_KEY}_preview_instruction_crud',
            'scope': PBC_KEY,
            'description': 'Preview governed CRUD mutations before any write is approved.',
            'requires_confirmation_for_mutation': True,
            'uses_appgen_event_contract': True,
            'stream_engine_picker_visible': False,
        },
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
            'recovery_triage',
            'cat_event_response_support',
        ),
        'side_effects': (),
    }


def document_instruction_plan(document: str, instruction: str, *, tenant: str = 'default') -> dict:
    preview = reinsurance_management_parse_document_instruction(
        reinsurance_management_empty_state(),
        document,
        instruction,
        tenant=tenant,
    )
    return {
        'ok': preview['ok'],
        'pbc': PBC_KEY,
        'document_digest': preview['record']['id'],
        'instruction': instruction,
        'candidate_tables': preview['record']['candidate_tables'],
        'requires_human_confirmation': preview['crud_preview']['requires_human_confirmation'],
        'crud_preview': preview['crud_preview'],
        'side_effects': (),
    }


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    target = table or REINSURANCE_MANAGEMENT_OWNED_TABLES[0]
    if not str(target).startswith(f'{PBC_KEY}_'):
        return {'ok': False, 'reason': 'foreign_table_rejected', 'table': target, 'side_effects': ()}
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'action': action,
        'table': target,
        'payload': dict(payload or {}),
        'requires_confirmation': action in {'create', 'update', 'delete'},
        'event_contract': 'AppGen-X',
        'side_effects': (),
    }


def composed_agent_contribution() -> dict:
    namespace = f'{PBC_KEY}_skills'
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'single_agent_skill_namespace': namespace,
        'dsl_tools': (namespace, f'{PBC_KEY}_crud', f'{PBC_KEY}_documents', f'{PBC_KEY}_recoveries'),
        'side_effects': (),
    }


def smoke_test() -> dict:
    return {
        'ok': agent_skill_manifest()['ok']
        and chatbot_interface_contract()['ok']
        and document_instruction_plan('loss bordereau', 'Create a claim recovery preview')['ok']
        and datastore_crud_plan('create')['ok']
        and datastore_crud_plan('update', table='foreign_table')['ok'] is False
        and composed_agent_contribution()['ok'],
        'side_effects': (),
    }
