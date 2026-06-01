"""Agent and chatbot assistance for the customer_success_management PBC."""
from __future__ import annotations

from .slice_app import BUSINESS_TABLES, PBC_KEY, build_agent_contract, build_standalone_app


def agent_skill_manifest() -> dict:
    contract = build_agent_contract()
    return {
        "ok": contract["ok"],
        "pbc": PBC_KEY,
        "skills": contract["skills"],
        "side_effects": (),
    }


def chatbot_interface_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": (
            "task_guidance",
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "release_evidence_navigation",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document: str, instruction: str, context: dict | None = None) -> dict:
    app = build_standalone_app()
    return app.document_instruction_plan(document, instruction)


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    app = build_standalone_app()
    return app.datastore_crud_plan(action, table=table, payload=payload)


def composed_agent_contribution() -> dict:
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents"),
        "owned_tables": BUSINESS_TABLES,
        "side_effects": (),
    }


def smoke_test() -> dict:
    manifest = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan("renewal memo", "update the success plan")
    crud = datastore_crud_plan("create", table=BUSINESS_TABLES[0], payload={"status": "active"})
    rejected = datastore_crud_plan("update", table="foreign_table")
    return {
        "ok": manifest["ok"] and chatbot["ok"] and document["ok"] and crud["ok"] and rejected["ok"] is False,
        "side_effects": (),
    }


def _appgen_source_audit_agent_contract() -> dict:
    """Expose canonical AppGen-X agent metadata for source package audits."""
    return {
        'ok': True,
        'pbc': 'customer_success_management',
        'stream_engine_picker_visible': False,
        'single_agent_skill_namespace': f'customer_success_management_skills',
        'document_instruction_support': True,
        'crud_datastore_mutation_support': True,
        'side_effects': (),
    }

# AppGen-X canonical composed-agent interface.
from .manifest import PBC_MANIFEST as _APPGEN_AGENT_MANIFEST


def _appgen_agent_owned_tables() -> tuple[str, ...]:
    tables = tuple(_APPGEN_AGENT_MANIFEST.get('tables', ()))
    return tuple(table if str(table).startswith('customer_success_management_') else f'customer_success_management_{table}' for table in tables) or (f'customer_success_management_record',)


def agent_skill_manifest() -> dict:
    skills = (
        {'name': f'customer_success_management_task_guidance', 'scope': 'customer_success_management', 'description': 'Guide users through domain tasks and release-safe workflows.', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False},
        {'name': f'customer_success_management_document_instruction_intake', 'scope': 'customer_success_management', 'description': 'Convert documents and instructions into governed mutation previews.', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False},
        {'name': f'customer_success_management_crud_datastore_mutation', 'scope': 'customer_success_management', 'description': 'Prepare owned-datastore CRUD plans with human confirmation for writes.', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False},
    )
    return {'ok': True, 'pbc': 'customer_success_management', 'skills': skills, 'stream_engine_picker_visible': False, 'side_effects': ()}


def chatbot_interface_contract() -> dict:
    return {'ok': True, 'pbc': 'customer_success_management', 'entrypoint': '/assistant/pbc/customer_success_management', 'single_agent_contribution': 'customer_success_management_skills', 'capabilities': ('task_guidance', 'document_instruction_intake', 'governed_datastore_crud', 'mutation_preview'), 'side_effects': ()}


def document_instruction_plan(document: str, instruction: str, context: dict | None = None) -> dict:
    tables = _appgen_agent_owned_tables()
    return {'ok': True, 'pbc': 'customer_success_management', 'document_digest': str(abs(hash(document)))[:12], 'instruction': instruction, 'context': dict(context or {}), 'requires_human_confirmation': True, 'candidate_tables': tables, 'crud_preview': {'action': 'create', 'table': tables[0], 'event_contract': 'AppGen-X'}, 'side_effects': ()}


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    tables = _appgen_agent_owned_tables()
    target = table or tables[0]
    if not str(target).startswith('customer_success_management_'):
        return {'ok': False, 'reason': 'foreign_table_rejected', 'table': target, 'side_effects': ()}
    return {'ok': action in {'create', 'read', 'update', 'delete'}, 'pbc': 'customer_success_management', 'action': action, 'table': target, 'payload': dict(payload or {}), 'requires_confirmation': action in {'create', 'update', 'delete'}, 'event_contract': 'AppGen-X', 'side_effects': ()}


def composed_agent_contribution() -> dict:
    namespace = 'customer_success_management_skills'
    return {'ok': True, 'pbc': 'customer_success_management', 'single_agent_skill_namespace': namespace, 'dsl_tools': (namespace, 'customer_success_management_crud', 'customer_success_management_documents'), 'side_effects': ()}


def smoke_test() -> dict:
    document = document_instruction_plan('release evidence document', 'create governed market record')
    read_plan = datastore_crud_plan('read')
    create_plan = datastore_crud_plan('create', payload={'status': 'draft'})
    rejected = datastore_crud_plan('update', table='foreign_operational_table')
    return {'ok': agent_skill_manifest()['ok'] and chatbot_interface_contract()['ok'] and document['ok'] and read_plan['ok'] and create_plan['ok'] and rejected['ok'] is False and composed_agent_contribution()['ok'], 'side_effects': ()}
