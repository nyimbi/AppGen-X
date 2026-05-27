"""AI agent and chatbot skills for the multi_sided_market PBC."""
from __future__ import annotations
import hashlib
from .manifest import PBC_MANIFEST
from . import services

PBC_KEY = 'multi_sided_market'
AGENT_NAME = 'MultiSidedMarketAgent'
DOCUMENT_ACTIONS = ('summarize', 'extract_fields', 'validate_against_rules', 'draft_crud_plan', 'draft_listing_or_exchange')
CRUD_ACTIONS = ('create', 'read', 'update', 'delete')
SKILL_NAMES = tuple(f'{PBC_KEY}.{name}' for name in ('task_guidance','document_instruction_intake','governed_create','governed_read','governed_update','governed_delete','exchange_advisor','workbench_navigation'))


def _owned_tables():
    return tuple(f'{PBC_KEY}_{table}' for table in PBC_MANIFEST.get('tables', ()))


def agent_skill_manifest():
    service_manifest = services.service_operation_manifest()
    return {'ok': bool(SKILL_NAMES) and bool(_owned_tables()) and bool(service_manifest.get('query_operations')), 'pbc': PBC_KEY, 'agent': AGENT_NAME, 'skills': tuple({'name': skill, 'scope': PBC_KEY, 'owned_tables': _owned_tables(), 'allowed_crud_actions': CRUD_ACTIONS, 'document_actions': DOCUMENT_ACTIONS, 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False} for skill in SKILL_NAMES), 'query_operations': service_manifest.get('query_operations', ()), 'command_operations': service_manifest.get('command_operations', ()), 'side_effects': ()}


def chatbot_interface_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'agent': AGENT_NAME, 'entrypoint': f'/assistant/pbc/{PBC_KEY}', 'single_agent_contribution': f'{PBC_KEY}_skills', 'capabilities': ('market_task_guidance','document_and_instruction_intake','governed_datastore_crud','exchange_recommendation','policy_and_permission_explanation','workbench_navigation'), 'professional_controls': ('citation_required_for_document_facts','mutation_preview_before_commit','permission_check_before_mutation','owned_table_boundary_check','audit_event_plan'), 'side_effects': ()}


def document_instruction_plan(document=None, instructions=None):
    digest = hashlib.sha256(f'{PBC_KEY}:{document or ""}:{instructions or ""}'.encode('utf-8')).hexdigest()
    return {'ok': bool(document or instructions), 'pbc': PBC_KEY, 'document_digest': digest, 'document_actions': DOCUMENT_ACTIONS, 'candidate_tables': _owned_tables(), 'candidate_operations': services.service_operation_manifest().get('command_operations', ()) + services.service_operation_manifest().get('query_operations', ()), 'requires_human_confirmation': True, 'side_effects': ()}


def datastore_crud_plan(action='read', table=None, payload=None):
    normalized_action = str(action).lower()
    owned_tables = _owned_tables()
    selected_table = table or owned_tables[0]
    operation_pool = services.service_operation_manifest().get('query_operations', ()) if normalized_action == 'read' else services.service_operation_manifest().get('command_operations', ())
    allowed = normalized_action in CRUD_ACTIONS and selected_table in owned_tables
    return {'ok': allowed and bool(operation_pool), 'pbc': PBC_KEY, 'action': normalized_action, 'table': selected_table, 'payload_keys': tuple(sorted(dict(payload or {}))), 'owned_tables': owned_tables, 'candidate_operations': operation_pool, 'requires_confirmation': normalized_action != 'read', 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'side_effects': ()}


def composed_agent_contribution():
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    return {'ok': skills['ok'] and chatbot['ok'], 'pbc': PBC_KEY, 'agent': AGENT_NAME, 'single_agent_skill_namespace': f'{PBC_KEY}_skills', 'dsl_tools': (f'{PBC_KEY}_skills', f'{PBC_KEY}_documents', f'{PBC_KEY}_crud'), 'skills': tuple(item['name'] for item in skills['skills']), 'chatbot': chatbot, 'side_effects': ()}


def smoke_test():
    skills = agent_skill_manifest(); chatbot = chatbot_interface_contract(); document = document_instruction_plan('market listing document', 'create a rental listing'); read_plan = datastore_crud_plan('read'); create_plan = datastore_crud_plan('create', payload={'status': 'draft'}); contribution = composed_agent_contribution()
    return {'ok': skills['ok'] and chatbot['ok'] and document['ok'] and read_plan['ok'] and create_plan['ok'] and contribution['ok'], 'skills': skills, 'chatbot': chatbot, 'document': document, 'read_plan': read_plan, 'create_plan': create_plan, 'contribution': contribution, 'side_effects': ()}
