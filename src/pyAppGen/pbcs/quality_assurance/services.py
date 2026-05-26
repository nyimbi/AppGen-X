"""Command service layer for the quality_assurance PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.quality_assurance.events', 'inbox_topic': 'pbc.quality_assurance.inbox', 'outbox_table': 'quality_assurance_appgen_outbox_event', 'inbox_table': 'quality_assurance_appgen_inbox_event', 'dead_letter_table': 'quality_assurance_appgen_dead_letter_event', 'emitted': ({'event_type': 'QualityHoldReleased', 'schema': 'quality_assurance.quality_hold_released.emitted.v1', 'topic': 'pbc.quality_assurance.events', 'outbox_table': 'quality_assurance_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'NonConformanceRaised', 'schema': 'quality_assurance.non_conformance_raised.emitted.v1', 'topic': 'pbc.quality_assurance.events', 'outbox_table': 'quality_assurance_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'ProductionCompleted', 'schema': 'quality_assurance.production_completed.consumed.v1', 'topic': 'pbc.quality_assurance.inbox', 'inbox_table': 'quality_assurance_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'GoodsReceiptPosted', 'schema': 'quality_assurance.goods_receipt_posted.consumed.v1', 'topic': 'pbc.quality_assurance.inbox', 'inbox_table': 'quality_assurance_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'quality_assurance_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'quality_assurance_appgen_inbox_event'}}


class QualityAssuranceService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'quality_assurance',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_inspections(self, payload=None):
        return self._command('command_inspections', payload or {})

    def command_non_conformances(self, payload=None):
        return self._command('command_non_conformances', payload or {})

    def command_quality_holds(self, payload=None):
        return self._command('command_quality_holds', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = QualityAssuranceService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'quality_assurance',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = QualityAssuranceService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
