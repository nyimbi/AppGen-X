"""Agent and chatbot assistance for the sustainability_esg_reporting PBC."""
from __future__ import annotations

from .blueprint import BUSINESS_TABLES, PBC_KEY
from .slice_app import build_agent_contract, build_standalone_app


def agent_skill_manifest() -> dict:
    contract = build_agent_contract()
    return {'ok': contract['ok'], 'pbc': PBC_KEY, 'skills': contract['skills'], 'side_effects': ()}


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
            'board_pack_navigation',
            'regulator_filing_navigation',
        ),
        'side_effects': (),
    }


def document_instruction_plan(document: str, instruction: str) -> dict:
    app = build_standalone_app()
    return app.document_instruction_plan(document, instruction)


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    app = build_standalone_app()
    return app.datastore_crud_plan(action, table=table, payload=payload)


def composed_agent_contribution() -> dict:
    namespace = f'{PBC_KEY}_skills'
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'single_agent_skill_namespace': namespace,
        'dsl_tools': (namespace, f'{PBC_KEY}_crud', f'{PBC_KEY}_documents'),
        'owned_tables': BUSINESS_TABLES,
        'side_effects': (),
    }


def smoke_test() -> dict:
    manifest = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan('board narrative', 'preview updates for the renewable claim section')
    crud = datastore_crud_plan('create', table=BUSINESS_TABLES[0], payload={'status': 'draft'})
    rejected = datastore_crud_plan('update', table='foreign_table')
    return {'ok': manifest['ok'] and chatbot['ok'] and document['ok'] and crud['ok'] and rejected['ok'] is False, 'side_effects': ()}
