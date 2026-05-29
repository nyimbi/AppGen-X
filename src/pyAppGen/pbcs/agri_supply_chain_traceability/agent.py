"""Agent planning helpers for agri_supply_chain_traceability."""
from __future__ import annotations

import hashlib

from . import runtime


PBC_KEY = 'agri_supply_chain_traceability'
OWNED_TABLES = runtime.AGRI_SUPPLY_CHAIN_TRACEABILITY_OWNED_TABLES
_TABLE_ROUTE_MAP = {
    f'{PBC_KEY}_farm_lot': {
        'operation': 'command_farm_lot',
        'route': '/api/pbc/agri_supply_chain_traceability/farm-lots',
        'permission': f'{PBC_KEY}.create',
    },
    f'{PBC_KEY}_input_batch': {
        'operation': 'record_input_batch',
        'route': '/api/pbc/agri_supply_chain_traceability/input-batches',
        'permission': f'{PBC_KEY}.create',
    },
    f'{PBC_KEY}_certification': {
        'operation': 'record_certification',
        'route': '/api/pbc/agri_supply_chain_traceability/certifications',
        'permission': f'{PBC_KEY}.create',
    },
    f'{PBC_KEY}_storage_event': {
        'operation': 'record_storage_event',
        'route': '/api/pbc/agri_supply_chain_traceability/storage-events',
        'permission': f'{PBC_KEY}.update',
    },
    f'{PBC_KEY}_transport_leg': {
        'operation': 'record_transport_leg',
        'route': '/api/pbc/agri_supply_chain_traceability/transport-legs',
        'permission': f'{PBC_KEY}.update',
    },
    f'{PBC_KEY}_recall_link': {
        'operation': 'record_recall_link',
        'route': '/api/pbc/agri_supply_chain_traceability/recall-links',
        'permission': f'{PBC_KEY}.update',
    },
    f'{PBC_KEY}_provenance_proof': {
        'operation': 'record_provenance_proof',
        'route': '/api/pbc/agri_supply_chain_traceability/provenance-proofs',
        'permission': f'{PBC_KEY}.approve',
    },
}
_KEYWORD_TABLES = (
    ('release', f'{PBC_KEY}_provenance_proof'),
    ('shipment', f'{PBC_KEY}_provenance_proof'),
    ('dispatch', f'{PBC_KEY}_provenance_proof'),
    ('certificate', f'{PBC_KEY}_certification'),
    ('cold chain', f'{PBC_KEY}_storage_event'),
    ('storage', f'{PBC_KEY}_storage_event'),
    ('transport', f'{PBC_KEY}_transport_leg'),
    ('truck', f'{PBC_KEY}_transport_leg'),
    ('input', f'{PBC_KEY}_input_batch'),
    ('fertilizer', f'{PBC_KEY}_input_batch'),
    ('lot', f'{PBC_KEY}_farm_lot'),
    ('farm', f'{PBC_KEY}_farm_lot'),
    ('recall', f'{PBC_KEY}_recall_link'),
    ('provenance', f'{PBC_KEY}_provenance_proof'),
)


def _digest(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()[:16]


def _candidate_tables(text: str) -> tuple[str, ...]:
    lowered = text.lower()
    tables: list[str] = []
    for keyword, table in _KEYWORD_TABLES:
        if keyword in lowered and table not in tables:
            tables.append(table)
    return tuple(tables or OWNED_TABLES[:4])


def _mutation_preview(table: str) -> dict:
    preview = dict(
        _TABLE_ROUTE_MAP.get(
            table,
            {
                'operation': 'query_workbench',
                'route': '/api/pbc/agri_supply_chain_traceability/workbench',
                'permission': f'{PBC_KEY}.read',
            },
        )
    )
    preview['table'] = table
    preview['event_contract'] = 'AppGen-X'
    preview['requires_confirmation'] = preview['permission'] != f'{PBC_KEY}.read'
    return preview


def agent_skill_manifest() -> dict:
    skills = (
        {
            'name': f'{PBC_KEY}_document_intake',
            'scope': PBC_KEY,
            'description': 'Extract farm-lot, certification, storage, transport, and provenance candidates from uploaded documents.',
            'requires_confirmation_for_mutation': True,
            'uses_appgen_event_contract': True,
            'stream_engine_picker_visible': False,
        },
        {
            'name': f'{PBC_KEY}_release_gate_review',
            'scope': PBC_KEY,
            'description': 'Prepare a release-readiness preview grounded in package-local records.',
            'requires_confirmation_for_mutation': False,
            'uses_appgen_event_contract': True,
            'stream_engine_picker_visible': False,
        },
        {
            'name': f'{PBC_KEY}_assess_release_readiness',
            'scope': PBC_KEY,
            'description': 'Run or preview the package-local release gate for a shipment candidate.',
            'requires_confirmation_for_mutation': False,
            'uses_appgen_event_contract': True,
            'stream_engine_picker_visible': False,
        },
        {
            'name': f'{PBC_KEY}_recall_investigation',
            'scope': PBC_KEY,
            'description': 'Assemble recall lineage, evidence, and blocked release actions for review.',
            'requires_confirmation_for_mutation': True,
            'uses_appgen_event_contract': True,
            'stream_engine_picker_visible': False,
        },
        {
            'name': f'{PBC_KEY}_crud_planner',
            'scope': PBC_KEY,
            'description': 'Plan governed CRUD mutations against owned agri traceability tables.',
            'requires_confirmation_for_mutation': True,
            'uses_appgen_event_contract': True,
            'stream_engine_picker_visible': False,
        },
    )
    return {'ok': True, 'pbc': PBC_KEY, 'skills': skills, 'side_effects': ()}


def standalone_agent_workspace_contract() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'namespace': f'{PBC_KEY}_skills',
        'allowed_tables': OWNED_TABLES[:7],
        'document_plan_route': '/api/pbc/agri_supply_chain_traceability/assistant/document-plans',
        'release_gate_route': '/api/pbc/agri_supply_chain_traceability/release-gates',
        'requires_human_confirmation_for_mutations': True,
        'side_effects': (),
    }


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
            'release_readiness_guidance',
            'release_gate_preview',
            'recall_investigation_planning',
        ),
        'workspace': standalone_agent_workspace_contract(),
        'side_effects': (),
    }


def document_instruction_plan(document, instruction):
    document_text = str(document or '')
    instruction_text = str(instruction or '')
    combined = f'{document_text}\n{instruction_text}'
    candidate_tables = _candidate_tables(combined)
    primary = candidate_tables[0]
    preview = _mutation_preview(primary)
    release_gate_hint = any(
        token in instruction_text.lower()
        for token in ('release', 'ship', 'dispatch', 'quarantine')
    )
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'document_digest': _digest(document_text),
        'instruction': instruction_text,
        'candidate_tables': candidate_tables,
        'primary_table': primary,
        'requires_human_confirmation': True,
        'mutation_preview': preview,
        'field_hints': {
            'farm_lot': ('id', 'site_id', 'commodity', 'season'),
            'input_batch': ('supplier', 'applied_at', 'farm_lot_id'),
            'certification': (
                'covered_farm_lot_ids',
                'covered_commodities',
                'valid_from',
                'valid_to',
            ),
            'storage_event': ('subject_ids', 'temperature_breach', 'quarantine_state'),
            'transport_leg': ('subject_ids', 'seal_state', 'receiving_confirmed'),
            'provenance_proof': ('subject_ids', 'source_farm_lot_ids'),
        },
        'source_citations': (
            {
                'document_digest': _digest(document_text),
                'table': primary,
                'route': preview['route'],
            },
        ),
        'release_gate_preview': {
            'suggested': release_gate_hint,
            'operation': 'assess_release_readiness',
            'route': '/api/pbc/agri_supply_chain_traceability/release-gates',
            'required_tables': OWNED_TABLES[:7],
        }
        if release_gate_hint
        else None,
        'side_effects': (),
    }


def datastore_crud_plan(action, table=None, payload=None):
    target = table or OWNED_TABLES[0]
    if not str(target).startswith(f'{PBC_KEY}_'):
        return {
            'ok': False,
            'reason': 'foreign_table_rejected',
            'table': target,
            'side_effects': (),
        }
    preview = _mutation_preview(target)
    permission = preview['permission']
    if action == 'read':
        permission = f'{PBC_KEY}.read'
    elif action == 'delete':
        permission = f'{PBC_KEY}.admin'
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'action': action,
        'table': target,
        'payload': dict(payload or {}),
        'route': preview['route'],
        'operation': preview['operation'],
        'permission': permission,
        'requires_confirmation': action in ('create', 'update', 'delete'),
        'idempotency_key': f"{PBC_KEY}:{action}:{target}:{_digest(repr(payload or {}))}",
        'event_contract': 'AppGen-X',
        'side_effects': (),
    }


def composed_agent_contribution() -> dict:
    namespace = f'{PBC_KEY}_skills'
    workspace = standalone_agent_workspace_contract()
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'single_agent_skill_namespace': namespace,
        'workspace': workspace,
        'dsl_tools': (
            namespace,
            f'{PBC_KEY}_crud',
            f'{PBC_KEY}_documents',
            f'{PBC_KEY}_release_gate',
            f'{PBC_KEY}_recall',
        ),
        'side_effects': (),
    }


def smoke_test() -> dict:
    document_plan = document_instruction_plan(
        'Certificate for lot LOT-1',
        'prepare release review',
    )
    crud_plan = datastore_crud_plan(
        'create',
        table=f'{PBC_KEY}_farm_lot',
        payload={'id': 'LOT-1'},
    )
    rejected = datastore_crud_plan('update', table='foreign_table')
    return {
        'ok': agent_skill_manifest()['ok']
        and chatbot_interface_contract()['ok']
        and composed_agent_contribution()['ok']
        and document_plan['ok']
        and crud_plan['ok']
        and rejected['ok'] is False,
        'document_plan': document_plan,
        'crud_plan': crud_plan,
        'rejected': rejected,
        'side_effects': (),
    }
