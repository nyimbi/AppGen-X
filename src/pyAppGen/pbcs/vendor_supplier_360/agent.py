"""Agent and chatbot assistance for the vendor_supplier_360 PBC."""
PBC_KEY = 'vendor_supplier_360'
OWNED_TABLES = ('vendor_supplier_360_supplier_profile', 'vendor_supplier_360_supplier_site', 'vendor_supplier_360_supplier_certification', 'vendor_supplier_360_supplier_bank_validation', 'vendor_supplier_360_supplier_risk_signal', 'vendor_supplier_360_supplier_esg_disclosure', 'vendor_supplier_360_supplier_scorecard', 'vendor_supplier_360_supplier_onboarding_case', 'vendor_supplier_360_appgen_outbox_event', 'vendor_supplier_360_appgen_inbox_event', 'vendor_supplier_360_appgen_dead_letter_event')


def agent_skill_manifest():
    skills = tuple({'name': name, 'scope': PBC_KEY, 'description': f'{name} for {PBC_KEY}', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False} for name in ('vendor_supplier_360_guide_user', 'vendor_supplier_360_read_records', 'vendor_supplier_360_create_record', 'vendor_supplier_360_update_record'))
    return {'ok': True, 'pbc': PBC_KEY, 'skills': skills, 'side_effects': ()}


def chatbot_interface_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'entrypoint': f'/assistant/pbc/{PBC_KEY}', 'single_agent_contribution': f'{PBC_KEY}_skills', 'capabilities': ('task_guidance','document_instruction_intake','governed_datastore_crud','mutation_preview'), 'side_effects': ()}


def document_instruction_plan(document, instruction):
    return {'ok': True, 'pbc': PBC_KEY, 'document_digest': str(abs(hash(document))), 'instruction': instruction, 'candidate_tables': OWNED_TABLES[:3], 'requires_human_confirmation': True, 'crud_preview': {'operation': 'create', 'event_contract': 'AppGen-X'}, 'side_effects': ()}


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
