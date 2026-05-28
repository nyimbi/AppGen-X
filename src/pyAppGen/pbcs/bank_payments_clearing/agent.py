PBC_KEY = 'bank_payments_clearing'
OWNED_TABLES = ('bank_payments_clearing_payment_instruction',
 'bank_payments_clearing_clearing_batch',
 'bank_payments_clearing_settlement_file',
 'bank_payments_clearing_return_item',
 'bank_payments_clearing_exception_case',
 'bank_payments_clearing_bank_reconciliation',
 'bank_payments_clearing_participant_bank',
 'bank_payments_clearing_bank_payments_clearing_policy_rule',
 'bank_payments_clearing_bank_payments_clearing_runtime_parameter',
 'bank_payments_clearing_bank_payments_clearing_schema_extension',
 'bank_payments_clearing_bank_payments_clearing_control_assertion',
 'bank_payments_clearing_bank_payments_clearing_governed_model',
 'bank_payments_clearing_appgen_outbox_event',
 'bank_payments_clearing_appgen_inbox_event',
 'bank_payments_clearing_appgen_dead_letter_event')

def agent_skill_manifest():
    domain_skills = (
        f'{PBC_KEY}_validate_payment_instruction',
        f'{PBC_KEY}_prepare_release_decision',
        f'{PBC_KEY}_assemble_clearing_batch',
        f'{PBC_KEY}_explain_settlement_acknowledgement',
        f'{PBC_KEY}_triage_return_or_reconciliation_break',
    )
    skills = tuple({'name': name, 'scope': PBC_KEY, 'description': f'{name} for {PBC_KEY}', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False} for name in (f'{PBC_KEY}_guide_user', f'{PBC_KEY}_read_records', f'{PBC_KEY}_create_record', f'{PBC_KEY}_update_record') + domain_skills)
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
    return {'ok': True, 'pbc': PBC_KEY, 'single_agent_skill_namespace': namespace, 'dsl_tools': (namespace, f'{PBC_KEY}_crud', f'{PBC_KEY}_documents', f'{PBC_KEY}_payment_release'), 'execution_operations': ('register_participant_bank','create_validated_payment_instruction','release_payment_instruction','assemble_clearing_batch','generate_settlement_file','handle_settlement_acknowledgement','process_return_item','reconcile_bank_statement'), 'side_effects': ()}

def smoke_test():
    return {'ok': agent_skill_manifest()['ok'] and chatbot_interface_contract()['ok'] and document_instruction_plan('doc','create')['ok'] and datastore_crud_plan('create')['ok'] and datastore_crud_plan('update', table='foreign_table')['ok'] is False and composed_agent_contribution()['ok'], 'side_effects': ()}
