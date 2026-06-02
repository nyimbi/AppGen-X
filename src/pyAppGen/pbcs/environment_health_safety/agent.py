from __future__ import annotations

from .standalone import AGENT_SKILLS, OWNED_TABLES, PBC_KEY, build_agent_contract, build_datastore_crud_plan, build_document_instruction_plan


def agent_skill_manifest():
    contract = build_agent_contract()
    return {"ok": True, "pbc": PBC_KEY, "skills": contract["skills"], "side_effects": ()}


def chatbot_interface_contract():
    contract = build_agent_contract()
    return {"ok": True, "pbc": PBC_KEY, "entrypoint": contract["entrypoint"], "single_agent_contribution": contract["single_agent_contribution"], "capabilities": contract["capabilities"], "side_effects": ()}


def document_instruction_plan(document, instruction):
    return build_document_instruction_plan(document, instruction)


def datastore_crud_plan(action, table=None, payload=None):
    return build_datastore_crud_plan(action, table=table, payload=payload)


def composed_agent_contribution():
    namespace = f"{PBC_KEY}_skills"
    return {"ok": True, "pbc": PBC_KEY, "single_agent_skill_namespace": namespace, "dsl_tools": tuple(skill["name"] for skill in AGENT_SKILLS) + (f"{PBC_KEY}_crud", f"{PBC_KEY}_documents"), "owned_tables": OWNED_TABLES, "side_effects": ()}


def smoke_test():
    return {"ok": agent_skill_manifest()["ok"] and chatbot_interface_contract()["ok"] and document_instruction_plan("permit package", "check permit conflict") ["ok"] and datastore_crud_plan("create")["ok"] and datastore_crud_plan("update", table="foreign_table")["ok"] is False and composed_agent_contribution()["ok"], "side_effects": ()}


def _appgen_source_audit_agent_contract() -> dict:
    """Expose canonical AppGen-X agent metadata for source package audits."""
    return {
        'ok': True,
        'pbc': 'environment_health_safety',
        'stream_engine_picker_visible': False,
        'single_agent_skill_namespace': f'environment_health_safety_skills',
        'document_instruction_support': True,
        'crud_datastore_mutation_support': True,
        'side_effects': (),
    }

# AppGen-X canonical composed-agent interface.
from .manifest import PBC_MANIFEST as _APPGEN_AGENT_MANIFEST


def _appgen_agent_owned_tables() -> tuple[str, ...]:
    tables = tuple(_APPGEN_AGENT_MANIFEST.get('tables', ()))
    return tuple(table if str(table).startswith('environment_health_safety_') else f'environment_health_safety_{table}' for table in tables) or (f'environment_health_safety_record',)


def agent_skill_manifest() -> dict:
    skills = (
        {'name': f'environment_health_safety_task_guidance', 'scope': 'environment_health_safety', 'description': 'Guide users through domain tasks and release-safe workflows.', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False},
        {'name': f'environment_health_safety_document_instruction_intake', 'scope': 'environment_health_safety', 'description': 'Convert documents and instructions into governed mutation previews.', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False},
        {'name': f'environment_health_safety_crud_datastore_mutation', 'scope': 'environment_health_safety', 'description': 'Prepare owned-datastore CRUD plans with human confirmation for writes.', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False},
    )
    return {'ok': True, 'pbc': 'environment_health_safety', 'skills': skills, 'stream_engine_picker_visible': False, 'side_effects': ()}


def chatbot_interface_contract() -> dict:
    return {'ok': True, 'pbc': 'environment_health_safety', 'entrypoint': '/assistant/pbc/environment_health_safety', 'single_agent_contribution': 'environment_health_safety_skills', 'capabilities': ('task_guidance', 'document_instruction_intake', 'governed_datastore_crud', 'mutation_preview'), 'side_effects': ()}


def document_instruction_plan(document: str, instruction: str, context: dict | None = None) -> dict:
    tables = _appgen_agent_owned_tables()
    return {'ok': True, 'pbc': 'environment_health_safety', 'document_digest': str(abs(hash(document)))[:12], 'instruction': instruction, 'context': dict(context or {}), 'requires_human_confirmation': True, 'candidate_tables': tables, 'crud_preview': {'action': 'create', 'table': tables[0], 'event_contract': 'AppGen-X'}, 'side_effects': ()}


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    tables = _appgen_agent_owned_tables()
    target = table or tables[0]
    if not str(target).startswith('environment_health_safety_'):
        return {'ok': False, 'reason': 'foreign_table_rejected', 'table': target, 'side_effects': ()}
    return {'ok': action in {'create', 'read', 'update', 'delete'}, 'pbc': 'environment_health_safety', 'action': action, 'table': target, 'payload': dict(payload or {}), 'requires_confirmation': action in {'create', 'update', 'delete'}, 'event_contract': 'AppGen-X', 'side_effects': ()}


def composed_agent_contribution() -> dict:
    namespace = 'environment_health_safety_skills'
    return {'ok': True, 'pbc': 'environment_health_safety', 'single_agent_skill_namespace': namespace, 'dsl_tools': (namespace, 'environment_health_safety_crud', 'environment_health_safety_documents'), 'side_effects': ()}


def smoke_test() -> dict:
    document = document_instruction_plan('release evidence document', 'create governed market record')
    read_plan = datastore_crud_plan('read')
    create_plan = datastore_crud_plan('create', payload={'status': 'draft'})
    rejected = datastore_crud_plan('update', table='foreign_operational_table')
    return {'ok': agent_skill_manifest()['ok'] and chatbot_interface_contract()['ok'] and document['ok'] and read_plan['ok'] and create_plan['ok'] and rejected['ok'] is False and composed_agent_contribution()['ok'], 'side_effects': ()}
