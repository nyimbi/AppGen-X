"""AI assistant and governed CRUD planning for agriculture_farm_operations."""

from __future__ import annotations

from .runtime import AGRICULTURE_FARM_OPERATIONS_BUSINESS_TABLES, PBC_KEY


def agent_skill_manifest() -> dict:
    skills = (
        {
            "name": f"{PBC_KEY}_agronomist_copilot",
            "scope": PBC_KEY,
            "description": "Summarize field history, planting-window risk, and readiness blockers.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_document_intake",
            "scope": PBC_KEY,
            "description": "Turn agronomy notes into reviewable crop-plan drafts.",
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
        {
            "name": f"{PBC_KEY}_compliance_packet_planner",
            "scope": PBC_KEY,
            "description": "Plan audit-ready evidence packets for fields and seasons.",
            "requires_confirmation_for_mutation": False,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "skills": skills, "side_effects": ()}


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
            "workflow_guidance",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document: str, instruction: str, context: dict | None = None) -> dict:
    from .runtime import agriculture_farm_operations_parse_document_instruction

    plan = agriculture_farm_operations_parse_document_instruction(document, instruction, context)
    return {
        "ok": plan["ok"],
        "pbc": PBC_KEY,
        "document_digest": plan["document_digest"],
        "instruction": instruction,
        "candidate_tables": plan["candidate_tables"],
        "requires_human_confirmation": plan["requires_human_confirmation"],
        "crud_preview": {
            "operation": "create",
            "target_table": "agriculture_farm_operations_crop_plan",
            "draft_preview": plan["draft_preview"],
            "event_contract": "AppGen-X",
        },
        "source_plan": plan,
        "side_effects": (),
    }


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    target = table or AGRICULTURE_FARM_OPERATIONS_BUSINESS_TABLES[0]
    if not str(target).startswith(f"{PBC_KEY}_"):
        return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "action": action,
        "table": target,
        "payload": dict(payload or {}),
        "requires_confirmation": action in ("create", "update", "delete"),
        "event_contract": "AppGen-X",
        "stages": ("validate", "preview", "confirm", "apply", "emit_event"),
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents"),
        "side_effects": (),
    }


def standalone_agent_workspace_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "assistant_entrypoint": f"/api/pbc/{PBC_KEY}/assistant",
        "document_entrypoint": f"/api/pbc/{PBC_KEY}/assistant/document-plan",
        "crud_entrypoint": f"/api/pbc/{PBC_KEY}/assistant/crud-plan",
        "governance": {
            "mutation_confirmation_required": True,
            "owned_table_boundary_only": True,
            "event_contract": "AppGen-X",
        },
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document_instruction_plan("doc", "create")["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"]
        and standalone_agent_workspace_contract()["ok"],
        "side_effects": (),
    }

# AppGen-X canonical composed-agent interface.
from .manifest import PBC_MANIFEST as _APPGEN_AGENT_MANIFEST


def _appgen_agent_owned_tables() -> tuple[str, ...]:
    tables = tuple(_APPGEN_AGENT_MANIFEST.get('tables', ()))
    return tuple(table if str(table).startswith('agriculture_farm_operations_') else f'agriculture_farm_operations_{table}' for table in tables) or (f'agriculture_farm_operations_record',)


def agent_skill_manifest() -> dict:
    skills = (
        {'name': f'agriculture_farm_operations_task_guidance', 'scope': 'agriculture_farm_operations', 'description': 'Guide users through domain tasks and release-safe workflows.', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False},
        {'name': f'agriculture_farm_operations_document_instruction_intake', 'scope': 'agriculture_farm_operations', 'description': 'Convert documents and instructions into governed mutation previews.', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False},
        {'name': f'agriculture_farm_operations_crud_datastore_mutation', 'scope': 'agriculture_farm_operations', 'description': 'Prepare owned-datastore CRUD plans with human confirmation for writes.', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False},
    )
    return {'ok': True, 'pbc': 'agriculture_farm_operations', 'skills': skills, 'stream_engine_picker_visible': False, 'side_effects': ()}


def chatbot_interface_contract() -> dict:
    return {'ok': True, 'pbc': 'agriculture_farm_operations', 'entrypoint': '/assistant/pbc/agriculture_farm_operations', 'single_agent_contribution': 'agriculture_farm_operations_skills', 'capabilities': ('task_guidance', 'document_instruction_intake', 'governed_datastore_crud', 'mutation_preview'), 'side_effects': ()}


def document_instruction_plan(document: str, instruction: str, context: dict | None = None) -> dict:
    tables = _appgen_agent_owned_tables()
    return {'ok': True, 'pbc': 'agriculture_farm_operations', 'document_digest': str(abs(hash(document)))[:12], 'instruction': instruction, 'context': dict(context or {}), 'requires_human_confirmation': True, 'candidate_tables': tables, 'crud_preview': {'action': 'create', 'table': tables[0], 'event_contract': 'AppGen-X'}, 'side_effects': ()}


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    tables = _appgen_agent_owned_tables()
    target = table or tables[0]
    if not str(target).startswith('agriculture_farm_operations_'):
        return {'ok': False, 'reason': 'foreign_table_rejected', 'table': target, 'side_effects': ()}
    return {'ok': action in {'create', 'read', 'update', 'delete'}, 'pbc': 'agriculture_farm_operations', 'action': action, 'table': target, 'payload': dict(payload or {}), 'requires_confirmation': action in {'create', 'update', 'delete'}, 'event_contract': 'AppGen-X', 'side_effects': ()}


def composed_agent_contribution() -> dict:
    namespace = 'agriculture_farm_operations_skills'
    return {'ok': True, 'pbc': 'agriculture_farm_operations', 'single_agent_skill_namespace': namespace, 'dsl_tools': (namespace, 'agriculture_farm_operations_crud', 'agriculture_farm_operations_documents'), 'side_effects': ()}


def smoke_test() -> dict:
    document = document_instruction_plan('release evidence document', 'create governed market record')
    read_plan = datastore_crud_plan('read')
    create_plan = datastore_crud_plan('create', payload={'status': 'draft'})
    rejected = datastore_crud_plan('update', table='foreign_operational_table')
    return {'ok': agent_skill_manifest()['ok'] and chatbot_interface_contract()['ok'] and document['ok'] and read_plan['ok'] and create_plan['ok'] and rejected['ok'] is False and composed_agent_contribution()['ok'], 'side_effects': ()}
