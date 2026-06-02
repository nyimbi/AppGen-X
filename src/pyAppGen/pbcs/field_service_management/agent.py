"""Agent and chatbot assistance for the field_service_management PBC."""
PBC_KEY = 'field_service_management'
from .app_surface import document_instruction_field_service_management_plan, single_pbc_field_service_management_app_contract

OWNED_TABLES = ('field_service_management_field_work_order', 'field_service_management_dispatch_assignment', 'field_service_management_technician_profile', 'field_service_management_mobile_task', 'field_service_management_parts_usage', 'field_service_management_service_sla', 'field_service_management_service_history', 'field_service_management_customer_service_update', 'field_service_management_appgen_outbox_event', 'field_service_management_appgen_inbox_event', 'field_service_management_appgen_dead_letter_event')


def agent_skill_manifest():
    skills = tuple({'name': name, 'scope': PBC_KEY, 'description': f'{name} for {PBC_KEY}', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False} for name in ('field_service_management_guide_user', 'field_service_management_read_records', 'field_service_management_create_record', 'field_service_management_update_record'))
    return {'ok': True, 'pbc': PBC_KEY, 'skills': skills, 'side_effects': ()}


def chatbot_interface_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'entrypoint': f'/assistant/pbc/{PBC_KEY}', 'single_agent_contribution': f'{PBC_KEY}_skills', 'capabilities': ('task_guidance','document_instruction_intake','governed_datastore_crud','mutation_preview'), 'side_effects': ()}


def document_instruction_plan(document, instruction):
    app_plan = document_instruction_field_service_management_plan(str(document or ''), str(instruction or ''))
    return {'ok': True, 'pbc': PBC_KEY, 'document_digest': str(abs(hash(document))), 'instruction': instruction, 'candidate_tables': OWNED_TABLES[:3], 'proposed_operation': app_plan['proposed_operation'], 'target_table': app_plan['target_table'], 'field_service_plan': app_plan, 'requires_human_confirmation': True, 'crud_preview': {'operation': 'create', 'event_contract': 'AppGen-X'}, 'side_effects': ()}


def datastore_crud_plan(action, table=None, payload=None):
    target = table or OWNED_TABLES[0]
    if not str(target).startswith(f'{PBC_KEY}_'):
        return {'ok': False, 'reason': 'foreign_table_rejected', 'table': target, 'side_effects': ()}
    mutation = action in ('create','update','delete')
    return {'ok': True, 'pbc': PBC_KEY, 'action': action, 'table': target, 'payload': dict(payload or {}), 'requires_confirmation': mutation, 'event_contract': 'AppGen-X', 'side_effects': ()}


def composed_agent_contribution():
    namespace = f'{PBC_KEY}_skills'
    return {'ok': True, 'pbc': PBC_KEY, 'single_agent_skill_namespace': namespace, 'dsl_tools': (namespace, f'{PBC_KEY}_crud', f'{PBC_KEY}_documents'), 'side_effects': ()}


def smoke_test():
    return {'ok': agent_skill_manifest()['ok'] and chatbot_interface_contract()['ok'] and document_instruction_plan('doc','create')['ok'] and datastore_crud_plan('create')['ok'] and datastore_crud_plan('update', table='foreign_table')['ok'] is False and composed_agent_contribution()['ok'], 'side_effects': ()}

# Advanced field-service assistant skills for dispatchers, supervisors, and
# mobile technicians.
from .field_operations import FIELD_WORKFORCE_OPERATIONS, field_service_management_workforce_capability_contract

_BASE_AGENT_SKILL_MANIFEST = agent_skill_manifest
_BASE_CHATBOT_INTERFACE_CONTRACT = chatbot_interface_contract
_BASE_COMPOSED_AGENT_CONTRIBUTION = composed_agent_contribution


def agent_skill_manifest():
    base = dict(_BASE_AGENT_SKILL_MANIFEST())
    workforce_skills = tuple(
        {
            'name': f'{PBC_KEY}_{operation}',
            'scope': PBC_KEY,
            'description': f'Guide, preview, and plan {operation} for {PBC_KEY}',
            'requires_confirmation_for_mutation': True,
            'uses_appgen_event_contract': True,
            'stream_engine_picker_visible': False,
        }
        for operation in FIELD_WORKFORCE_OPERATIONS
    )
    return {**base, 'ok': base['ok'], 'skills': tuple(base['skills']) + workforce_skills}


def chatbot_interface_contract():
    base = dict(_BASE_CHATBOT_INTERFACE_CONTRACT())
    return {
        **base,
        'capabilities': tuple(dict.fromkeys(tuple(base['capabilities']) + (
            'live_workforce_location_guidance',
            'route_optimization_guidance',
            'skill_based_assignment_recommendations',
            'job_tool_requirement_validation',
            'task_dependency_and_safety_gate_guidance',
        ))),
        'workforce_capability_surface': field_service_management_workforce_capability_contract(),
    }


def composed_agent_contribution():
    base = dict(_BASE_COMPOSED_AGENT_CONTRIBUTION())
    namespace = base['single_agent_skill_namespace']
    return {
        **base,
        'dsl_tools': tuple(dict.fromkeys(tuple(base['dsl_tools']) + tuple(f'{namespace}.{operation}' for operation in FIELD_WORKFORCE_OPERATIONS))),
        'standalone_app': single_pbc_field_service_management_app_contract(),
    }


def standalone_agent_smoke_test():
    document = document_instruction_plan('where are technicians', 'optimize route')
    contribution = composed_agent_contribution()
    return {'ok': document['target_table'].startswith(f'{PBC_KEY}_') and contribution['ok'] and contribution['standalone_app']['ok'], 'document': document, 'contribution': contribution, 'side_effects': ()}
