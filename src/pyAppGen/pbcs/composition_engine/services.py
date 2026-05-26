"""Command service layer for the composition_engine PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.composition_engine.events', 'inbox_topic': 'pbc.composition_engine.inbox', 'outbox_table': 'composition_engine_appgen_outbox_event', 'inbox_table': 'composition_engine_appgen_inbox_event', 'dead_letter_table': 'composition_engine_appgen_dead_letter_event', 'emitted': ({'event_type': 'CompositionPublished', 'schema': 'composition_engine.composition_published.emitted.v1', 'topic': 'pbc.composition_engine.events', 'outbox_table': 'composition_engine_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PbcDeployed', 'schema': 'composition_engine.pbc_deployed.emitted.v1', 'topic': 'pbc.composition_engine.events', 'outbox_table': 'composition_engine_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'SchemaAccepted', 'schema': 'composition_engine.schema_accepted.consumed.v1', 'topic': 'pbc.composition_engine.inbox', 'inbox_table': 'composition_engine_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'RoutePublished', 'schema': 'composition_engine.route_published.consumed.v1', 'topic': 'pbc.composition_engine.inbox', 'inbox_table': 'composition_engine_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'composition_engine_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'composition_engine_appgen_inbox_event'}}


class CompositionEngineService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'composition_engine',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_compositions(self, payload=None):
        return self._command('command_compositions', payload or {})

    def command_fragments(self, payload=None):
        return self._command('command_fragments', payload or {})

    def query_component_registry(self, payload=None):
        return self._command('query_component_registry', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = CompositionEngineService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'composition_engine',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = CompositionEngineService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
