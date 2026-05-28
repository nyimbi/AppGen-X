PBC_KEY = 'trade_finance_operations'
OWNED_TABLES = ('trade_finance_operations_letter_of_credit',
 'trade_finance_operations_bank_guarantee',
 'trade_finance_operations_documentary_collection',
 'trade_finance_operations_trade_document',
 'trade_finance_operations_sanctions_check',
 'trade_finance_operations_shipment_evidence',
 'trade_finance_operations_trade_settlement',
 'trade_finance_operations_trade_finance_operations_policy_rule',
 'trade_finance_operations_trade_finance_operations_runtime_parameter',
 'trade_finance_operations_trade_finance_operations_schema_extension',
 'trade_finance_operations_trade_finance_operations_control_assertion',
 'trade_finance_operations_trade_finance_operations_governed_model',
 'trade_finance_operations_appgen_outbox_event',
 'trade_finance_operations_appgen_inbox_event',
 'trade_finance_operations_appgen_dead_letter_event')

def agent_skill_manifest():
    skills = tuple({'name': name, 'scope': PBC_KEY, 'description': f'{name} for {PBC_KEY}', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False} for name in (f'{PBC_KEY}_guide_user', f'{PBC_KEY}_read_records', f'{PBC_KEY}_create_record', f'{PBC_KEY}_update_record'))
    return {'ok': True, 'pbc': PBC_KEY, 'skills': skills, 'side_effects': ()}

def chatbot_interface_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'entrypoint': f'/assistant/pbc/{PBC_KEY}', 'single_agent_contribution': f'{PBC_KEY}_skills', 'capabilities': ('task_guidance','document_instruction_intake','governed_datastore_crud','mutation_preview'), 'side_effects': ()}

def document_instruction_plan(document, instruction):
    return {'ok': True, 'pbc': PBC_KEY, 'document_digest': str(abs(hash(document))), 'instruction': instruction, 'candidate_tables': OWNED_TABLES[:3], 'requires_human_confirmation': True, 'crud_preview': {'operation': 'create', 'event_contract': 'AppGen-X'}, 'side_effects': ()}

def datastore_crud_plan(action, table=None, payload=None):
    target = table or OWNED_TABLES[0]
    if not str(target).startswith(f'{PBC_KEY}_'):
        return {'ok': False, 'reason': 'foreign_table_rejected', 'table': target, 'side_effects': ()}
    return {'ok': True, 'pbc': PBC_KEY, 'action': action, 'table': target, 'payload': dict(payload or {}), 'requires_confirmation': action in ('create','update','delete'), 'event_contract': 'AppGen-X', 'side_effects': ()}

def composed_agent_contribution():
    namespace = f'{PBC_KEY}_skills'
    return {'ok': True, 'pbc': PBC_KEY, 'single_agent_skill_namespace': namespace, 'dsl_tools': (namespace, f'{PBC_KEY}_crud', f'{PBC_KEY}_documents'), 'side_effects': ()}

def smoke_test():
    return {'ok': agent_skill_manifest()['ok'] and chatbot_interface_contract()['ok'] and document_instruction_plan('doc','create')['ok'] and datastore_crud_plan('create')['ok'] and datastore_crud_plan('update', table='foreign_table')['ok'] is False and composed_agent_contribution()['ok'], 'side_effects': ()}
