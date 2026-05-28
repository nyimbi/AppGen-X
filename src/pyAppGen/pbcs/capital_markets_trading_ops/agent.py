PBC_KEY = 'capital_markets_trading_ops'
OWNED_TABLES = ('capital_markets_trading_ops_trade_order',
 'capital_markets_trading_ops_execution',
 'capital_markets_trading_ops_allocation',
 'capital_markets_trading_ops_confirmation',
 'capital_markets_trading_ops_settlement_instruction',
 'capital_markets_trading_ops_trade_break',
 'capital_markets_trading_ops_position_snapshot',
 'capital_markets_trading_ops_capital_markets_trading_ops_policy_rule',
 'capital_markets_trading_ops_capital_markets_trading_ops_runtime_parameter',
 'capital_markets_trading_ops_capital_markets_trading_ops_schema_extension',
 'capital_markets_trading_ops_capital_markets_trading_ops_control_assertion',
 'capital_markets_trading_ops_capital_markets_trading_ops_governed_model',
 'capital_markets_trading_ops_appgen_outbox_event',
 'capital_markets_trading_ops_appgen_inbox_event',
 'capital_markets_trading_ops_appgen_dead_letter_event')

def agent_skill_manifest():
    skills = tuple({'name': name, 'scope': PBC_KEY, 'description': f'{name} for {PBC_KEY}', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False} for name in (f'{PBC_KEY}_guide_user', f'{PBC_KEY}_read_records', f'{PBC_KEY}_create_record', f'{PBC_KEY}_update_record', f'{PBC_KEY}_triage_trade_order'))
    return {'ok': True, 'pbc': PBC_KEY, 'skills': skills, 'side_effects': ()}

def chatbot_interface_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'entrypoint': f'/assistant/pbc/{PBC_KEY}', 'single_agent_contribution': f'{PBC_KEY}_skills', 'capabilities': ('task_guidance','document_instruction_intake','governed_datastore_crud','mutation_preview','operator_help'), 'side_effects': ()}


def assistant_help_manifest():
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'topics': (
            'trade_order_intake_form',
            'trade_order_release_wizard',
            'reference_data_controls',
            'risk_gate_panel',
            'trade_order_exception_triage',
        ),
        'suggested_prompts': (
            'Explain why this trade order is blocked',
            'Show the next remediation step for this order',
            'Summarize the pre-trade controls for release',
        ),
        'requires_confirmation_for_mutation': True,
        'event_contract': 'AppGen-X',
        'side_effects': (),
    }


def build_operator_guidance(record=None):
    record = dict(record or {})
    validation = dict(record.get('validation', {}))
    remediation = tuple(record.get('actionable_remediation', ()) or validation.get('actionable_remediation', ()))
    if remediation:
        summary = 'Order requires remediation before release.'
    elif record.get('release_ready'):
        summary = 'Order is ready for supervised release.'
    else:
        summary = 'Order intake is available for review.'
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'summary': summary,
        'next_actions': remediation or ('Review the release decision card.',),
        'topics': assistant_help_manifest()['topics'],
        'record_id': record.get('id'),
        'side_effects': (),
    }

def document_instruction_plan(document, instruction):
    return {'ok': True, 'pbc': PBC_KEY, 'document_digest': str(abs(hash(document))), 'instruction': instruction, 'candidate_tables': OWNED_TABLES[:3], 'requires_human_confirmation': True, 'crud_preview': {'operation': 'create', 'event_contract': 'AppGen-X'}, 'side_effects': ()}

def datastore_crud_plan(action, table=None, payload=None):
    target = table or OWNED_TABLES[0]
    if not str(target).startswith(f'{PBC_KEY}_'):
        return {'ok': False, 'reason': 'foreign_table_rejected', 'table': target, 'side_effects': ()}
    return {'ok': True, 'pbc': PBC_KEY, 'action': action, 'table': target, 'payload': dict(payload or {}), 'requires_confirmation': action in ('create','update','delete'), 'event_contract': 'AppGen-X', 'side_effects': ()}

def composed_agent_contribution():
    namespace = f'{PBC_KEY}_skills'
    return {'ok': True, 'pbc': PBC_KEY, 'single_agent_skill_namespace': namespace, 'dsl_tools': (namespace, f'{PBC_KEY}_crud', f'{PBC_KEY}_documents', f'{PBC_KEY}_operator_help'), 'side_effects': ()}

def smoke_test():
    return {'ok': agent_skill_manifest()['ok'] and chatbot_interface_contract()['ok'] and assistant_help_manifest()['ok'] and build_operator_guidance({'id': 'test', 'actionable_remediation': ('Populate missing field: broker',)})['ok'] and document_instruction_plan('doc','create')['ok'] and datastore_crud_plan('create')['ok'] and datastore_crud_plan('update', table='foreign_table')['ok'] is False and composed_agent_contribution()['ok'], 'side_effects': ()}
