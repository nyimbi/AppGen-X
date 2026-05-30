from __future__ import annotations

from .slice_app import PBC_KEY, RUNTIME_TABLES, build_agent_contract, build_standalone_app

OWNED_TABLES = RUNTIME_TABLES
stream_engine_picker_visible = False


def agent_skill_manifest() -> dict:
    contract = build_agent_contract()
    skills = tuple({**skill, 'requires_confirmation_for_mutation': True, 'stream_engine_picker_visible': False} for skill in contract['skills'])
    return {
        'ok': contract['ok'],
        'pbc': PBC_KEY,
        'skills': skills,
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }


def chatbot_interface_contract() -> dict:
    contract = build_agent_contract()
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'entrypoint': f'/assistant/pbc/{PBC_KEY}',
        'single_agent_contribution': contract['namespace'],
        'capabilities': contract['capabilities'],
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }


def document_instruction_plan(document: str, instruction: str) -> dict:
    return build_standalone_app().document_instruction_plan(document, instruction)


def datastore_crud_plan(action: str, table=None, payload=None) -> dict:
    return build_standalone_app().datastore_crud_plan(action, table, payload)


def composed_agent_contribution() -> dict:
    namespace = f'{PBC_KEY}_skills'
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'single_agent_skill_namespace': namespace,
        'dsl_tools': (namespace, f'{PBC_KEY}_crud', f'{PBC_KEY}_documents'),
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }


def smoke_test() -> dict:
    return {
        'ok': agent_skill_manifest()['ok'] and chatbot_interface_contract()['ok'] and document_instruction_plan('doc', 'update')['ok'] and datastore_crud_plan('create')['ok'] and datastore_crud_plan('update', table='foreign_table')['ok'] is False and composed_agent_contribution()['ok'],
        'side_effects': (),
    }
