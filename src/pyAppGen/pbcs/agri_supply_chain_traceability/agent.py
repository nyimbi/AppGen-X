PBC_KEY = 'agri_supply_chain_traceability'
OWNED_TABLES = ('agri_supply_chain_traceability_farm_lot',
 'agri_supply_chain_traceability_input_batch',
 'agri_supply_chain_traceability_certification',
 'agri_supply_chain_traceability_storage_event',
 'agri_supply_chain_traceability_transport_leg',
 'agri_supply_chain_traceability_recall_link',
 'agri_supply_chain_traceability_provenance_proof',
 'agri_supply_chain_traceability_agri_supply_chain_traceability_policy_rule',
 'agri_supply_chain_traceability_agri_supply_chain_traceability_runtime_parameter',
 'agri_supply_chain_traceability_agri_supply_chain_traceability_schema_extension',
 'agri_supply_chain_traceability_agri_supply_chain_traceability_control_assertion',
 'agri_supply_chain_traceability_agri_supply_chain_traceability_governed_model',
 'agri_supply_chain_traceability_appgen_outbox_event',
 'agri_supply_chain_traceability_appgen_inbox_event',
 'agri_supply_chain_traceability_appgen_dead_letter_event')

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
