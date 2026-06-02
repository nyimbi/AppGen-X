"""Agent contracts for the utility_outage_restoration PBC."""
from __future__ import annotations

import hashlib

from .models import STANDALONE_TABLE_KEYS, standalone_model_contract
from .routes import standalone_route_contracts
from .services import standalone_service_operation_contracts, service_operation_manifest
from .ui import (
    utility_outage_restoration_form_contracts,
    utility_outage_restoration_standalone_workbench_blueprint,
    utility_outage_restoration_wizard_contracts,
)

PBC_KEY = 'utility_outage_restoration'
OWNED_TABLES = (
    'utility_outage_restoration_outage_incident',
    'utility_outage_restoration_device_interruption',
    'utility_outage_restoration_switching_step',
    'utility_outage_restoration_crew_assignment',
    'utility_outage_restoration_restoration_estimate',
    'utility_outage_restoration_customer_impact',
    'utility_outage_restoration_reliability_metric',
    'utility_outage_restoration_utility_outage_restoration_policy_rule',
    'utility_outage_restoration_utility_outage_restoration_runtime_parameter',
    'utility_outage_restoration_utility_outage_restoration_schema_extension',
    'utility_outage_restoration_utility_outage_restoration_control_assertion',
    'utility_outage_restoration_utility_outage_restoration_governed_model',
    'utility_outage_restoration_appgen_outbox_event',
    'utility_outage_restoration_appgen_inbox_event',
    'utility_outage_restoration_appgen_dead_letter_event',
)
AGENT_NAME = 'UtilityOutageRestorationAgent'
_SKILL_NAMES = (
    f'{PBC_KEY}.triage_outage',
    f'{PBC_KEY}.governed_datastore_crud',
    f'{PBC_KEY}.dispatch_crew',
    f'{PBC_KEY}.author_switching_plan',
    f'{PBC_KEY}.coordinate_storm_mode',
    f'{PBC_KEY}.prepare_regulatory_indices',
    f'{PBC_KEY}.governed_assistance',
)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _standalone_operations() -> tuple[dict, ...]:
    return standalone_service_operation_contracts().get('contracts', ())


def standalone_agent_workspace_contract() -> dict:
    forms = utility_outage_restoration_form_contracts()['contracts']
    wizards = utility_outage_restoration_wizard_contracts()['contracts']
    routes = standalone_route_contracts()['routes']
    blueprint = utility_outage_restoration_standalone_workbench_blueprint()
    return {
        'format': 'appgen.utility-outage-restoration-standalone-agent-workspace.v1',
        'ok': bool(forms) and bool(wizards) and bool(routes) and blueprint['ok'],
        'pbc': PBC_KEY,
        'agent': AGENT_NAME,
        'forms': tuple(item['key'] for item in forms),
        'wizards': tuple(item['key'] for item in wizards),
        'routes': routes,
        'tables': STANDALONE_TABLE_KEYS,
        'side_effects': (),
    }


def agent_skill_manifest():
    service_manifest = service_operation_manifest()
    return {
        'ok': bool(_SKILL_NAMES) and bool(service_manifest.get('query_operations')),
        'pbc': PBC_KEY,
        'skills': tuple(
            {
                'name': skill,
                'scope': PBC_KEY,
                'description': f'{skill} for {PBC_KEY}',
                'requires_confirmation_for_mutation': True,
                'uses_appgen_event_contract': True,
                'stream_engine_picker_visible': False,
            }
            for skill in _SKILL_NAMES
        ),
        'query_operations': service_manifest.get('query_operations', ()),
        'command_operations': service_manifest.get('command_operations', ()),
        'side_effects': (),
    }


def chatbot_interface_contract():
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'entrypoint': f'/assistant/pbc/{PBC_KEY}',
        'single_agent_contribution': f'{PBC_KEY}_skills',
        'capabilities': ('task_guidance', 'document_instruction_intake', 'governed_datastore_crud', 'mutation_preview', 'storm_mode_coordination'),
        'side_effects': (),
    }


def document_instruction_plan(document, instruction):
    text = f'{document} {instruction}'.lower()
    wizards = utility_outage_restoration_wizard_contracts()['contracts']
    forms = utility_outage_restoration_form_contracts()['contracts']
    standalone_operations = _standalone_operations()
    wizard_candidates = tuple(item['key'] for item in wizards if any(keyword in text for keyword in item.get('keywords', ()))) or ('GovernedAssistanceWizard',)
    route_candidates = tuple(
        f"{item['method']} {item['path']}"
        for item in standalone_operations
        if item['operation_kind'] == 'command' and (item['wizard'] in wizard_candidates or item['operation'].replace('_', ' ') in text)
    )
    form_candidates = tuple(
        form['key']
        for form in forms
        if any(form['operation'] == item['operation'] for item in standalone_operations if f"{item['method']} {item['path']}" in route_candidates)
    ) or ('UtilityGovernedAssistanceForm',)
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'document_digest': _digest((document, instruction)),
        'instruction': instruction,
        'candidate_tables': OWNED_TABLES[:3],
        'standalone_tables': STANDALONE_TABLE_KEYS,
        'wizard_candidates': wizard_candidates,
        'form_candidates': form_candidates,
        'route_candidates': route_candidates,
        'requires_human_confirmation': True,
        'crud_preview': {'operation': 'create', 'event_contract': 'AppGen-X'},
        'side_effects': (),
    }


def datastore_crud_plan(action, table=None, payload=None):
    target = table or OWNED_TABLES[0]
    owned = OWNED_TABLES + STANDALONE_TABLE_KEYS
    if not str(target).startswith(f'{PBC_KEY}_') or target not in owned:
        return {'ok': False, 'reason': 'foreign_table_rejected', 'table': target, 'side_effects': ()}
    standalone_operations = _standalone_operations()
    route_candidates = tuple(
        f"{item['method']} {item['path']}"
        for item in standalone_operations
        if item['table'] == target and ((action == 'read' and item['operation_kind'] == 'query') or (action != 'read' and item['operation_kind'] == 'command'))
    )
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'action': action,
        'table': target,
        'payload': dict(payload or {}),
        'requires_confirmation': action in ('create', 'update', 'delete'),
        'event_contract': 'AppGen-X',
        'route_candidates': route_candidates,
        'side_effects': (),
    }


def composed_agent_contribution():
    namespace = f'{PBC_KEY}_skills'
    workspace = standalone_agent_workspace_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'single_agent_skill_namespace': namespace, 'dsl_tools': (namespace, f'{PBC_KEY}_crud', f'{PBC_KEY}_documents'), 'workspace': workspace, 'side_effects': ()}


def smoke_test():
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan('storm packet', 'dispatch crew and send customer update')
    read_plan = datastore_crud_plan('read')
    create_plan = datastore_crud_plan('create', payload={'status': 'draft'})
    rejected = datastore_crud_plan('update', table='foreign_table')
    contribution = composed_agent_contribution()
    workspace = standalone_agent_workspace_contract()
    return {
        'ok': skills['ok'] and chatbot['ok'] and document['ok'] and read_plan['ok'] and create_plan['ok'] and rejected['ok'] is False and contribution['ok'] and workspace['ok'],
        'side_effects': (),
    }
