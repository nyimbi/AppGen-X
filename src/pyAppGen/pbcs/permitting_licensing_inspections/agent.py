"""Agent and chatbot contracts for permitting_licensing_inspections."""
from __future__ import annotations

from .runtime import (
    PERMITTING_LICENSING_INSPECTIONS_BUSINESS_TABLES,
    permitting_licensing_inspections_build_agent_help_contract,
    permitting_licensing_inspections_build_controls_contract,
    permitting_licensing_inspections_build_forms_contract,
    permitting_licensing_inspections_build_wizards_contract,
    permitting_licensing_inspections_parse_document_instruction,
)

PBC_KEY = 'permitting_licensing_inspections'
OWNED_TABLES = PERMITTING_LICENSING_INSPECTIONS_BUSINESS_TABLES


def agent_skill_manifest():
    forms = permitting_licensing_inspections_build_forms_contract()
    wizards = permitting_licensing_inspections_build_wizards_contract()
    controls = permitting_licensing_inspections_build_controls_contract()
    skills = tuple(
        {
            'name': name,
            'scope': PBC_KEY,
            'description': f'{name} for {PBC_KEY}',
            'requires_confirmation_for_mutation': True,
            'uses_appgen_event_contract': True,
            'stream_engine_picker_visible': False,
            'suggested_forms': tuple(form['name'] for form in forms['forms']),
            'suggested_wizards': tuple(wizard['name'] for wizard in wizards['wizards']),
            'suggested_controls': tuple(control['name'] for control in controls['controls']),
        }
        for name in (
            f'{PBC_KEY}_guide_user',
            f'{PBC_KEY}_read_records',
            f'{PBC_KEY}_create_record',
            f'{PBC_KEY}_update_record',
            f'{PBC_KEY}_triage_case_hold',
        )
    )
    return {'ok': True, 'pbc': PBC_KEY, 'skills': skills, 'side_effects': ()}


def chatbot_interface_contract():
    help_contract = permitting_licensing_inspections_build_agent_help_contract()
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
            'case_hold_triage',
        ),
        'help_contract': help_contract,
        'side_effects': (),
    }


def document_instruction_plan(document, instruction):
    parsed = permitting_licensing_inspections_parse_document_instruction(document, instruction)
    return {
        'ok': parsed['ok'],
        'pbc': PBC_KEY,
        'document_digest': parsed['document_digest'],
        'instruction': instruction,
        'candidate_tables': parsed['candidate_tables'],
        'candidate_forms': parsed['candidate_forms'],
        'candidate_wizards': parsed['candidate_wizards'],
        'requires_human_confirmation': parsed['requires_human_confirmation'],
        'domain_plan': parsed['domain_plan'],
        'crud_preview': {
            'operation': 'create',
            'event_contract': 'AppGen-X',
            'target_table': parsed['candidate_tables'][0],
        },
        'side_effects': (),
    }


def datastore_crud_plan(action, table=None, payload=None):
    target = table or OWNED_TABLES[0]
    if not str(target).startswith(f'{PBC_KEY}_'):
        return {'ok': False, 'reason': 'foreign_table_rejected', 'table': target, 'side_effects': ()}
    permission_map = {
        'read': f'{PBC_KEY}.read',
        'create': f'{PBC_KEY}.create',
        'update': f'{PBC_KEY}.update',
        'delete': f'{PBC_KEY}.admin',
    }
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'action': action,
        'table': target,
        'payload': dict(payload or {}),
        'required_permission': permission_map.get(action, f'{PBC_KEY}.update'),
        'requires_confirmation': action in ('create', 'update', 'delete'),
        'event_contract': 'AppGen-X',
        'side_effects': (),
    }


def composed_agent_contribution():
    namespace = f'{PBC_KEY}_skills'
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'single_agent_skill_namespace': namespace,
        'dsl_tools': (namespace, f'{PBC_KEY}_crud', f'{PBC_KEY}_documents'),
        'assistant_help': permitting_licensing_inspections_build_agent_help_contract(),
        'side_effects': (),
    }


def smoke_test():
    return {
        'ok': agent_skill_manifest()['ok']
        and chatbot_interface_contract()['ok']
        and document_instruction_plan('hearing notice and plan resubmittal', 'prepare operator draft')['ok']
        and datastore_crud_plan('create')['ok']
        and datastore_crud_plan('update', table='foreign_table')['ok'] is False
        and composed_agent_contribution()['ok'],
        'side_effects': (),
    }
