from .compatibility import explain_gate_assignment_decision

PBC_KEY = 'airport_operations_management'
OWNED_TABLES = ('airport_operations_management_gate_assignment',
 'airport_operations_management_stand_allocation',
 'airport_operations_management_slot',
 'airport_operations_management_turndown_task',
 'airport_operations_management_baggage_belt',
 'airport_operations_management_passenger_flow',
 'airport_operations_management_airport_disruption',
 'airport_operations_management_airport_operations_management_policy_rule',
 'airport_operations_management_airport_operations_management_runtime_parameter',
 'airport_operations_management_airport_operations_management_schema_extension',
 'airport_operations_management_airport_operations_management_control_assertion',
 'airport_operations_management_airport_operations_management_governed_model',
 'airport_operations_management_appgen_outbox_event',
 'airport_operations_management_appgen_inbox_event',
 'airport_operations_management_appgen_dead_letter_event')

def agent_skill_manifest():
    skills = tuple({'name': name, 'scope': PBC_KEY, 'description': f'{name} for {PBC_KEY}', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False} for name in (f'{PBC_KEY}_guide_user', f'{PBC_KEY}_read_records', f'{PBC_KEY}_create_record', f'{PBC_KEY}_update_record', f'{PBC_KEY}_explain_gate_assignment_decision'))
    return {'ok': True, 'pbc': PBC_KEY, 'skills': skills, 'side_effects': ()}

def chatbot_interface_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'entrypoint': f'/assistant/pbc/{PBC_KEY}', 'single_agent_contribution': f'{PBC_KEY}_skills', 'capabilities': ('task_guidance','document_instruction_intake','governed_datastore_crud','mutation_preview','gate_assignment_decision_rationale'), 'side_effects': ()}

def document_instruction_plan(document, instruction):
    from .standalone import assistant_document_plan
    return assistant_document_plan(document, instruction)

def datastore_crud_plan(action, table=None, payload=None):
    target = table or OWNED_TABLES[0]
    if not str(target).startswith(f'{PBC_KEY}_'):
        return {'ok': False, 'reason': 'foreign_table_rejected', 'table': target, 'side_effects': ()}
    return {'ok': True, 'pbc': PBC_KEY, 'action': action, 'table': target, 'payload': dict(payload or {}), 'requires_confirmation': action in ('create','update','delete'), 'event_contract': 'AppGen-X', 'side_effects': ()}

def gate_assignment_decision_rationale(request, candidate_stands=None, occupied_stands=()):
    explanation = explain_gate_assignment_decision(request, candidate_stands, occupied_stands)
    return {'ok': True, 'pbc': PBC_KEY, 'summary': explanation['summary'], 'recommendation': explanation['recommendation'], 'blocked_options': explanation['blocked_options'], 'event_contract': 'AppGen-X', 'side_effects': ()}

def composed_agent_contribution():
    from .standalone import single_pbc_app_contract
    namespace = f'{PBC_KEY}_skills'
    app = single_pbc_app_contract()
    return {'ok': True and app['ok'], 'pbc': PBC_KEY, 'single_agent_skill_namespace': namespace, 'dsl_tools': (namespace, f'{PBC_KEY}_crud', f'{PBC_KEY}_documents'), 'standalone_app': app['dsl_exposure'], 'side_effects': ()}

def smoke_test():
    rationale = gate_assignment_decision_rationale({'flight_number': 'AOM-SMOKE'})
    return {'ok': agent_skill_manifest()['ok'] and chatbot_interface_contract()['ok'] and document_instruction_plan('doc','create')['ok'] and datastore_crud_plan('create')['ok'] and datastore_crud_plan('update', table='foreign_table')['ok'] is False and rationale['ok'] and composed_agent_contribution()['ok'], 'side_effects': ()}
