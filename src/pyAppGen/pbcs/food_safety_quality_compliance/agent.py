from .slice_app import chatbot_interface_contract as _chatbot_interface_contract
from .slice_app import composed_agent_contribution as _composed_agent_contribution
from .slice_app import datastore_crud_plan as _datastore_crud_plan
from .slice_app import document_instruction_plan as _document_instruction_plan
from .slice_app import agent_skill_manifest as _agent_skill_manifest
from .slice_app import PBC_KEY

OWNED_TABLES = (
    "food_safety_quality_compliance_haccp_plan",
    "food_safety_quality_compliance_critical_control_point",
    "food_safety_quality_compliance_inspection",
    "food_safety_quality_compliance_nonconformance",
    "food_safety_quality_compliance_recall_event",
    "food_safety_quality_compliance_supplier_audit",
    "food_safety_quality_compliance_quality_hold",
    "food_safety_quality_compliance_food_safety_quality_compliance_policy_rule",
    "food_safety_quality_compliance_food_safety_quality_compliance_runtime_parameter",
    "food_safety_quality_compliance_food_safety_quality_compliance_schema_extension",
    "food_safety_quality_compliance_food_safety_quality_compliance_control_assertion",
    "food_safety_quality_compliance_food_safety_quality_compliance_governed_model",
    "food_safety_quality_compliance_appgen_outbox_event",
    "food_safety_quality_compliance_appgen_inbox_event",
    "food_safety_quality_compliance_appgen_dead_letter_event",
)


def smoke_test():
    return {
        "ok": agent_skill_manifest()["ok"]
        and chatbot_interface_contract()["ok"]
        and document_instruction_plan("doc", "create")["ok"]
        and datastore_crud_plan("create")["ok"]
        and datastore_crud_plan("update", table="foreign_table")["ok"] is False
        and composed_agent_contribution()["ok"],
        "side_effects": (),
    }


def _appgen_source_audit_agent_contract() -> dict:
    """Expose canonical AppGen-X agent metadata for source package audits."""
    return {
        'ok': True,
        'pbc': 'food_safety_quality_compliance',
        'stream_engine_picker_visible': False,
        'single_agent_skill_namespace': f'food_safety_quality_compliance_skills',
        'document_instruction_support': True,
        'crud_datastore_mutation_support': True,
        'side_effects': (),
    }


def agent_skill_manifest() -> dict:
    manifest = _agent_skill_manifest()
    skills = tuple({**skill, 'stream_engine_picker_visible': False} for skill in manifest['skills'])
    return {**manifest, 'skills': skills, 'stream_engine_picker_visible': False, 'side_effects': ()}


def chatbot_interface_contract() -> dict:
    contract = _chatbot_interface_contract()
    return {**contract, 'stream_engine_picker_visible': False, 'side_effects': ()}


def document_instruction_plan(document: str, instruction: str, context: dict | None = None) -> dict:
    return _document_instruction_plan(document, instruction)


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    return _datastore_crud_plan(action, table=table, payload=payload)


def composed_agent_contribution() -> dict:
    contribution = _composed_agent_contribution()
    return {**contribution, 'single_agent_skill_namespace': f'{PBC_KEY}_skills', 'side_effects': ()}

# AppGen-X canonical composed-agent interface.
from .manifest import PBC_MANIFEST as _APPGEN_AGENT_MANIFEST


def _appgen_agent_owned_tables() -> tuple[str, ...]:
    tables = tuple(_APPGEN_AGENT_MANIFEST.get('tables', ()))
    return tuple(table if str(table).startswith('food_safety_quality_compliance_') else f'food_safety_quality_compliance_{table}' for table in tables) or (f'food_safety_quality_compliance_record',)


def agent_skill_manifest() -> dict:
    skills = (
        {'name': f'food_safety_quality_compliance_task_guidance', 'scope': 'food_safety_quality_compliance', 'description': 'Guide users through domain tasks and release-safe workflows.', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False},
        {'name': f'food_safety_quality_compliance_document_instruction_intake', 'scope': 'food_safety_quality_compliance', 'description': 'Convert documents and instructions into governed mutation previews.', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False},
        {'name': f'food_safety_quality_compliance_crud_datastore_mutation', 'scope': 'food_safety_quality_compliance', 'description': 'Prepare owned-datastore CRUD plans with human confirmation for writes.', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False},
    )
    return {'ok': True, 'pbc': 'food_safety_quality_compliance', 'skills': skills, 'stream_engine_picker_visible': False, 'side_effects': ()}


def chatbot_interface_contract() -> dict:
    return {'ok': True, 'pbc': 'food_safety_quality_compliance', 'entrypoint': '/assistant/pbc/food_safety_quality_compliance', 'single_agent_contribution': 'food_safety_quality_compliance_skills', 'capabilities': ('task_guidance', 'document_instruction_intake', 'governed_datastore_crud', 'mutation_preview'), 'side_effects': ()}


def document_instruction_plan(document: str, instruction: str, context: dict | None = None) -> dict:
    tables = _appgen_agent_owned_tables()
    return {'ok': True, 'pbc': 'food_safety_quality_compliance', 'document_digest': str(abs(hash(document)))[:12], 'instruction': instruction, 'context': dict(context or {}), 'requires_human_confirmation': True, 'candidate_tables': tables, 'crud_preview': {'action': 'create', 'table': tables[0], 'event_contract': 'AppGen-X'}, 'side_effects': ()}


def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict:
    tables = _appgen_agent_owned_tables()
    target = table or tables[0]
    if not str(target).startswith('food_safety_quality_compliance_'):
        return {'ok': False, 'reason': 'foreign_table_rejected', 'table': target, 'side_effects': ()}
    return {'ok': action in {'create', 'read', 'update', 'delete'}, 'pbc': 'food_safety_quality_compliance', 'action': action, 'table': target, 'payload': dict(payload or {}), 'requires_confirmation': action in {'create', 'update', 'delete'}, 'event_contract': 'AppGen-X', 'side_effects': ()}


def composed_agent_contribution() -> dict:
    namespace = 'food_safety_quality_compliance_skills'
    return {'ok': True, 'pbc': 'food_safety_quality_compliance', 'single_agent_skill_namespace': namespace, 'dsl_tools': (namespace, 'food_safety_quality_compliance_crud', 'food_safety_quality_compliance_documents'), 'side_effects': ()}


def smoke_test() -> dict:
    document = document_instruction_plan('release evidence document', 'create governed market record')
    read_plan = datastore_crud_plan('read')
    create_plan = datastore_crud_plan('create', payload={'status': 'draft'})
    rejected = datastore_crud_plan('update', table='foreign_operational_table')
    return {'ok': agent_skill_manifest()['ok'] and chatbot_interface_contract()['ok'] and document['ok'] and read_plan['ok'] and create_plan['ok'] and rejected['ok'] is False and composed_agent_contribution()['ok'], 'side_effects': ()}
