from __future__ import annotations

from .domain_depth import DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES
from .runtime import (
    rail_operations_management_parse_document_instruction,
    rail_operations_management_verify_owned_table_boundary,
)


PBC_KEY = 'rail_operations_management'
OWNED_TABLES = DOMAIN_OWNED_TABLES


def agent_skill_manifest():
    skills = (
        {
            'name': f'{PBC_KEY}_guide_user',
            'scope': PBC_KEY,
            'description': 'Explain dispatch, yard, terminal, incident, and analytics flows for rail control users.',
            'requires_confirmation_for_mutation': False,
            'uses_appgen_event_contract': True,
            'stream_engine_picker_visible': False,
        },
        {
            'name': f'{PBC_KEY}_preview_document_instruction',
            'scope': PBC_KEY,
            'description': 'Parse notices, circulars, and free-text instructions into governed mutation previews.',
            'requires_confirmation_for_mutation': True,
            'uses_appgen_event_contract': True,
            'stream_engine_picker_visible': False,
        },
        {
            'name': f'{PBC_KEY}_preview_crud',
            'scope': PBC_KEY,
            'description': 'Preview create, update, and delete actions against owned rail operations tables only.',
            'requires_confirmation_for_mutation': True,
            'uses_appgen_event_contract': True,
            'stream_engine_picker_visible': False,
        },
        {
            'name': f'{PBC_KEY}_analyze_recovery',
            'scope': PBC_KEY,
            'description': 'Summarize dispatch tradeoffs for passenger, freight, incident, and energy-aware recovery.',
            'requires_confirmation_for_mutation': False,
            'uses_appgen_event_contract': True,
            'stream_engine_picker_visible': False,
        },
    )
    return {'ok': True, 'pbc': PBC_KEY, 'skills': skills, 'side_effects': ()}


def chatbot_interface_contract():
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
            'dispatch_recovery_guidance',
            'shift_handover_support',
        ),
        'side_effects': (),
    }


def document_instruction_plan(document, instruction, state=None):
    parsed = rail_operations_management_parse_document_instruction(document, instruction, state=state)
    return {
        'ok': parsed['ok'],
        'pbc': PBC_KEY,
        'document_digest': parsed['document_digest'],
        'instruction': parsed['instruction'],
        'candidate_tables': parsed['candidate_tables'],
        'candidate_operations': parsed['candidate_operations'],
        'requires_human_confirmation': parsed['requires_human_confirmation'],
        'crud_preview': parsed['crud_preview'],
        'citations': parsed['citations'],
        'side_effects': (),
    }


def datastore_crud_plan(action, table=None, payload=None):
    target = table or OWNED_TABLES[0]
    boundary = rail_operations_management_verify_owned_table_boundary((target,))
    if not str(target).startswith(f'{PBC_KEY}_') or not boundary['ok']:
        return {'ok': False, 'reason': 'foreign_table_rejected', 'table': target, 'side_effects': ()}
    preview_operation = 'create' if action == 'create' else 'update' if action == 'update' else 'delete'
    candidate_operation = next((operation for operation in DOMAIN_OPERATIONS if target.endswith(operation.split('_', 1)[-1])), 'preview_document_instruction')
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'action': action,
        'table': target,
        'payload': dict(payload or {}),
        'requires_confirmation': action in ('create', 'update', 'delete'),
        'event_contract': 'AppGen-X',
        'preview': {
            'operation': preview_operation,
            'candidate_runtime_operation': candidate_operation,
            'fields': tuple(sorted((payload or {}).keys())),
        },
        'side_effects': (),
    }


def composed_agent_contribution():
    namespace = f'{PBC_KEY}_skills'
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'single_agent_skill_namespace': namespace,
        'dsl_tools': (namespace, f'{PBC_KEY}_crud', f'{PBC_KEY}_documents', f'{PBC_KEY}_dispatch'),
        'side_effects': (),
    }


def smoke_test():
    parsed = document_instruction_plan('Delay notice for train 1001 and crew relief at terminal.', 'Update train, crew, and terminal plans')
    return {
        'ok': agent_skill_manifest()['ok']
        and chatbot_interface_contract()['ok']
        and parsed['ok']
        and datastore_crud_plan('create')['ok']
        and datastore_crud_plan('update', table='foreign_table')['ok'] is False
        and composed_agent_contribution()['ok'],
        'side_effects': (),
    }
