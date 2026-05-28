from .campaign_planning import build_campaign_plan, review_launch_readiness

PBC_KEY = 'advertising_campaign_operations'
OWNED_TABLES = ('advertising_campaign_operations_ad_campaign',
 'advertising_campaign_operations_audience_segment',
 'advertising_campaign_operations_media_placement',
 'advertising_campaign_operations_creative_asset',
 'advertising_campaign_operations_campaign_budget',
 'advertising_campaign_operations_performance_result',
 'advertising_campaign_operations_billing_event',
 'advertising_campaign_operations_advertising_campaign_operations_policy_rule',
 'advertising_campaign_operations_advertising_campaign_operations_runtime_parameter',
 'advertising_campaign_operations_advertising_campaign_operations_schema_extension',
 'advertising_campaign_operations_advertising_campaign_operations_control_assertion',
 'advertising_campaign_operations_advertising_campaign_operations_governed_model',
 'advertising_campaign_operations_appgen_outbox_event',
 'advertising_campaign_operations_appgen_inbox_event',
 'advertising_campaign_operations_appgen_dead_letter_event')

def agent_skill_manifest():
    skills = tuple({'name': name, 'scope': PBC_KEY, 'description': f'{name} for {PBC_KEY}', 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False} for name in (f'{PBC_KEY}_guide_user', f'{PBC_KEY}_read_records', f'{PBC_KEY}_create_record', f'{PBC_KEY}_update_record', f'{PBC_KEY}_preview_campaign_brief', f'{PBC_KEY}_review_launch_readiness'))
    return {'ok': True, 'pbc': PBC_KEY, 'skills': skills, 'side_effects': ()}

def chatbot_interface_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'entrypoint': f'/assistant/pbc/{PBC_KEY}', 'single_agent_contribution': f'{PBC_KEY}_skills', 'capabilities': ('task_guidance','document_instruction_intake','governed_datastore_crud','mutation_preview','campaign_brief_preview','launch_readiness_review'), 'side_effects': ()}

def document_instruction_plan(document, instruction):
    return {'ok': True, 'pbc': PBC_KEY, 'document_digest': str(abs(hash(document))), 'instruction': instruction, 'candidate_tables': OWNED_TABLES[:3], 'requires_human_confirmation': True, 'crud_preview': {'operation': 'create', 'event_contract': 'AppGen-X'}, 'side_effects': ()}

def campaign_brief_preview(payload=None):
    plan = build_campaign_plan(payload or {})
    return {'ok': plan['ok'], 'pbc': PBC_KEY, 'campaign_plan': plan.get('campaign_plan'), 'missing_fields': plan.get('missing_fields', ()), 'event_contract': 'AppGen-X', 'side_effects': ()}

def launch_readiness_preview(payload=None):
    review = review_launch_readiness(payload or {})
    return {'ok': review['ok'], 'pbc': PBC_KEY, 'launch_report': review['launch_report'], 'event_contract': 'AppGen-X', 'side_effects': ()}

def datastore_crud_plan(action, table=None, payload=None):
    target = table or OWNED_TABLES[0]
    if not str(target).startswith(f'{PBC_KEY}_'):
        return {'ok': False, 'reason': 'foreign_table_rejected', 'table': target, 'side_effects': ()}
    return {'ok': True, 'pbc': PBC_KEY, 'action': action, 'table': target, 'payload': dict(payload or {}), 'requires_confirmation': action in ('create','update','delete'), 'event_contract': 'AppGen-X', 'side_effects': ()}

def composed_agent_contribution():
    namespace = f'{PBC_KEY}_skills'
    return {'ok': True, 'pbc': PBC_KEY, 'single_agent_skill_namespace': namespace, 'dsl_tools': (namespace, f'{PBC_KEY}_crud', f'{PBC_KEY}_documents'), 'side_effects': ()}

def smoke_test():
    return {'ok': agent_skill_manifest()['ok'] and chatbot_interface_contract()['ok'] and document_instruction_plan('doc','create')['ok'] and campaign_brief_preview({'brief': {'objective': 'Acquire signups', 'offer': 'Trial', 'audience_promise': 'Show to in-market buyers', 'channels': ('search',), 'primary_kpi': 'signups', 'guardrails': ('cpa',), 'launch_dependencies': ('tracking',)}})['ok'] and launch_readiness_preview({'campaign_plan': {'brief': {'objective': 'Acquire signups', 'offer': 'Trial', 'audience_promise': 'Show to in-market buyers', 'channels': ('search',), 'primary_kpi': 'signups', 'guardrails': ('cpa',), 'launch_dependencies': ('tracking',)}}})['ok'] and datastore_crud_plan('create')['ok'] and datastore_crud_plan('update', table='foreign_table')['ok'] is False and composed_agent_contribution()['ok'], 'side_effects': ()}
