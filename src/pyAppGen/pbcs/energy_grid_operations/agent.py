"""Agent metadata for the energy_grid_operations standalone package."""

from __future__ import annotations

from .runtime import ENERGY_GRID_OPERATIONS_OWNED_TABLES, PBC_KEY


def agent_skill_manifest() -> dict:
    skills = (
        {
            "name": f"{PBC_KEY}_guide_operator",
            "description": "Explain switching, dispatch, and outage workflows using package-local evidence.",
            "requires_confirmation_for_mutation": False,
        },
        {
            "name": f"{PBC_KEY}_simulate_switching",
            "description": "Prepare a switching-order preview with hold points and backfeed warnings.",
            "requires_confirmation_for_mutation": True,
        },
        {
            "name": f"{PBC_KEY}_summarize_outage",
            "description": "Summarize outage impact, restoration priority, and recommended operator actions.",
            "requires_confirmation_for_mutation": False,
        },
        {
            "name": f"{PBC_KEY}_governed_crud_preview",
            "description": "Generate owned-table create and update previews that require human confirmation before mutation.",
            "requires_confirmation_for_mutation": True,
        },
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "skills": skills,
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
            "switching_simulation_explanation",
            "outage_restoration_summary",
            "governed_datastore_crud",
            "mutation_preview",
        ),
        "side_effects": (),
    }


def document_instruction_plan(document: str, instruction: str, context: dict | None = None) -> dict:
    lowered = f"{document} {instruction}".lower()
    if "switch" in lowered:
        candidate_operations = ("review_switching_order", "record_grid_topology")
    elif "outage" in lowered or "restore" in lowered:
        candidate_operations = ("simulate_outage_event", "approve_dispatch_instruction")
    elif "dispatch" in lowered:
        candidate_operations = ("approve_dispatch_instruction",)
    else:
        candidate_operations = ("create_grid_asset", "record_load_forecast")
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": str(abs(hash(document))),
        "instruction": instruction,
        "candidate_operations": candidate_operations,
        "candidate_tables": ENERGY_GRID_OPERATIONS_OWNED_TABLES[:4],
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    target = table or ENERGY_GRID_OPERATIONS_OWNED_TABLES[0]
    if not str(target).startswith(f"{PBC_KEY}_"):
        return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "action": action,
        "table": target,
        "payload": dict(payload or {}),
        "requires_confirmation": action in {"create", "update", "delete"},
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def composed_agent_contribution() -> dict:
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (
            namespace,
            f"{PBC_KEY}_crud",
            f"{PBC_KEY}_documents",
            f"{PBC_KEY}_release_evidence",
        ),
        "side_effects": (),
    }


def standalone_agent_workspace_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "workspace_route": f"/assistant/pbc/{PBC_KEY}",
        "namespace": f"{PBC_KEY}_skills",
        "documents_supported": True,
        "governed_mutations": True,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document_instruction_plan("switching order", "simulate")["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"],
        "side_effects": (),
    }


def _appgen_source_audit_agent_contract() -> dict:
    """Expose canonical AppGen-X agent metadata for source package audits."""
    return {
        'ok': True,
        'pbc': 'energy_grid_operations',
        'stream_engine_picker_visible': False,
        'single_agent_skill_namespace': f'energy_grid_operations_skills',
        'document_instruction_support': True,
        'crud_datastore_mutation_support': True,
        'side_effects': (),
    }

# AppGen-X canonical composed-agent interface.
from .manifest import PBC_MANIFEST as _APPGEN_AGENT_MANIFEST


def _appgen_agent_owned_tables() -> tuple[str, ...]:
    tables = tuple(_APPGEN_AGENT_MANIFEST.get('tables', ()))
    return tuple(table if str(table).startswith('energy_grid_operations_') else f'energy_grid_operations_{table}' for table in tables) or (f'energy_grid_operations_record',)


def agent_skill_manifest() -> dict:
    skills = (
        {'name': f'energy_grid_operations_task_guidance', 'scope': 'energy_grid_operations', 'description': 'Guide users through domain tasks and release-safe workflows.', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False},
        {'name': f'energy_grid_operations_document_instruction_intake', 'scope': 'energy_grid_operations', 'description': 'Convert documents and instructions into governed mutation previews.', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False},
        {'name': f'energy_grid_operations_crud_datastore_mutation', 'scope': 'energy_grid_operations', 'description': 'Prepare owned-datastore CRUD plans with human confirmation for writes.', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False},
    )
    return {'ok': True, 'pbc': 'energy_grid_operations', 'skills': skills, 'stream_engine_picker_visible': False, 'side_effects': ()}


def chatbot_interface_contract() -> dict:
    return {'ok': True, 'pbc': 'energy_grid_operations', 'entrypoint': '/assistant/pbc/energy_grid_operations', 'single_agent_contribution': 'energy_grid_operations_skills', 'capabilities': ('task_guidance', 'document_instruction_intake', 'governed_datastore_crud', 'mutation_preview'), 'side_effects': ()}


def document_instruction_plan(document: str, instruction: str, context: dict | None = None) -> dict:
    tables = _appgen_agent_owned_tables()
    return {'ok': True, 'pbc': 'energy_grid_operations', 'document_digest': str(abs(hash(document)))[:12], 'instruction': instruction, 'context': dict(context or {}), 'requires_human_confirmation': True, 'candidate_tables': tables, 'crud_preview': {'action': 'create', 'table': tables[0], 'event_contract': 'AppGen-X'}, 'side_effects': ()}


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    tables = _appgen_agent_owned_tables()
    target = table or tables[0]
    if not str(target).startswith('energy_grid_operations_'):
        return {'ok': False, 'reason': 'foreign_table_rejected', 'table': target, 'side_effects': ()}
    return {'ok': action in {'create', 'read', 'update', 'delete'}, 'pbc': 'energy_grid_operations', 'action': action, 'table': target, 'payload': dict(payload or {}), 'requires_confirmation': action in {'create', 'update', 'delete'}, 'event_contract': 'AppGen-X', 'side_effects': ()}


def composed_agent_contribution() -> dict:
    namespace = 'energy_grid_operations_skills'
    return {'ok': True, 'pbc': 'energy_grid_operations', 'single_agent_skill_namespace': namespace, 'dsl_tools': (namespace, 'energy_grid_operations_crud', 'energy_grid_operations_documents'), 'side_effects': ()}


def smoke_test() -> dict:
    document = document_instruction_plan('release evidence document', 'create governed market record')
    read_plan = datastore_crud_plan('read')
    create_plan = datastore_crud_plan('create', payload={'status': 'draft'})
    rejected = datastore_crud_plan('update', table='foreign_operational_table')
    return {'ok': agent_skill_manifest()['ok'] and chatbot_interface_contract()['ok'] and document['ok'] and read_plan['ok'] and create_plan['ok'] and rejected['ok'] is False and composed_agent_contribution()['ok'], 'side_effects': ()}
