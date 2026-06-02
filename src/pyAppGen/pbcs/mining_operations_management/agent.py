PBC_KEY = 'mining_operations_management'
OWNED_TABLES = ('mining_operations_management_mine_plan',
 'mining_operations_management_pit_block',
 'mining_operations_management_extraction_shift',
 'mining_operations_management_haulage_cycle',
 'mining_operations_management_fleet_asset',
 'mining_operations_management_ore_quality',
 'mining_operations_management_stockpile',
 'mining_operations_management_mining_operations_management_policy_rule',
 'mining_operations_management_mining_operations_management_runtime_parameter',
 'mining_operations_management_mining_operations_management_schema_extension',
 'mining_operations_management_mining_operations_management_control_assertion',
 'mining_operations_management_mining_operations_management_governed_model',
 'mining_operations_management_appgen_outbox_event',
 'mining_operations_management_appgen_inbox_event',
 'mining_operations_management_appgen_dead_letter_event')


def _standalone_form_helpers():
    from .forms import mining_operations_management_form_catalog
    from .wizards import mining_operations_management_wizard_catalog

    forms = mining_operations_management_form_catalog()
    wizards = mining_operations_management_wizard_catalog()
    route_candidates = tuple(form['route'] for form in forms['forms'])
    return forms['form_ids'], wizards['wizard_ids'], route_candidates


def agent_skill_manifest():
    skills = tuple({'name': name, 'scope': PBC_KEY, 'description': f'{name} for {PBC_KEY}', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False} for name in (f'{PBC_KEY}_guide_user', f'{PBC_KEY}_read_records', f'{PBC_KEY}_create_record', f'{PBC_KEY}_update_record'))
    return {'ok': True, 'pbc': PBC_KEY, 'skills': skills, 'side_effects': ()}


def chatbot_interface_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'entrypoint': f'/assistant/pbc/{PBC_KEY}', 'single_agent_contribution': f'{PBC_KEY}_skills', 'capabilities': ('task_guidance','document_instruction_intake','governed_datastore_crud','mutation_preview'), 'side_effects': ()}


def document_instruction_plan(document, instruction):
    form_candidates, wizard_candidates, route_candidates = _standalone_form_helpers()
    return {'ok': True, 'pbc': PBC_KEY, 'document_digest': str(abs(hash(document))), 'instruction': instruction, 'candidate_tables': OWNED_TABLES[:3], 'requires_human_confirmation': True, 'crud_preview': {'operation': 'create', 'event_contract': 'AppGen-X'}, 'form_candidates': form_candidates[:4], 'wizard_candidates': wizard_candidates, 'route_candidates': route_candidates[:4], 'side_effects': ()}


def datastore_crud_plan(action, table=None, payload=None):
    target = table or OWNED_TABLES[0]
    if not str(target).startswith(f'{PBC_KEY}_'):
        return {'ok': False, 'reason': 'foreign_table_rejected', 'table': target, 'side_effects': ()}
    _, _, route_candidates = _standalone_form_helpers()
    return {'ok': True, 'pbc': PBC_KEY, 'action': action, 'table': target, 'payload': dict(payload or {}), 'requires_confirmation': action in ('create','update','delete'), 'event_contract': 'AppGen-X', 'route_candidates': route_candidates[:4], 'side_effects': ()}


def composed_agent_contribution():
    namespace = f'{PBC_KEY}_skills'
    return {'ok': True, 'pbc': PBC_KEY, 'single_agent_skill_namespace': namespace, 'dsl_tools': (namespace, f'{PBC_KEY}_crud', f'{PBC_KEY}_documents'), 'side_effects': ()}


def smoke_test():
    return {'ok': agent_skill_manifest()['ok'] and chatbot_interface_contract()['ok'] and document_instruction_plan('doc','create')['ok'] and datastore_crud_plan('create')['ok'] and datastore_crud_plan('update', table='foreign_table')['ok'] is False and composed_agent_contribution()['ok'], 'side_effects': ()}
