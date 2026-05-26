"""Command service layer for the lead_opportunity PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.lead_opportunity.events', 'inbox_topic': 'pbc.lead_opportunity.inbox', 'outbox_table': 'lead_opportunity_appgen_outbox_event', 'inbox_table': 'lead_opportunity_appgen_inbox_event', 'dead_letter_table': 'lead_opportunity_appgen_dead_letter_event', 'emitted': ({'event_type': 'OpportunityWon', 'schema': 'lead_opportunity.opportunity_won.emitted.v1', 'topic': 'pbc.lead_opportunity.events', 'outbox_table': 'lead_opportunity_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'CustomerUpdated', 'schema': 'lead_opportunity.customer_updated.emitted.v1', 'topic': 'pbc.lead_opportunity.events', 'outbox_table': 'lead_opportunity_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'CustomerSegmentUpdated', 'schema': 'lead_opportunity.customer_segment_updated.consumed.v1', 'topic': 'pbc.lead_opportunity.inbox', 'inbox_table': 'lead_opportunity_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')},), 'retry_policy': {'name': 'lead_opportunity_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'lead_opportunity_appgen_inbox_event'}}


class LeadOpportunityService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'lead_opportunity',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_leads(self, payload=None):
        return self._command('command_leads', payload or {})

    def command_opportunities(self, payload=None):
        return self._command('command_opportunities', payload or {})

    def query_pipeline(self, payload=None):
        return self._command('query_pipeline', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = LeadOpportunityService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'lead_opportunity',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = LeadOpportunityService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
