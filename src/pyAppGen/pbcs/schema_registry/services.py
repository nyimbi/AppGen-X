"""Command service layer for the schema_registry PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.schema_registry.events', 'inbox_topic': 'pbc.schema_registry.inbox', 'outbox_table': 'schema_registry_appgen_outbox_event', 'inbox_table': 'schema_registry_appgen_inbox_event', 'dead_letter_table': 'schema_registry_appgen_dead_letter_event', 'emitted': ({'event_type': 'SchemaAccepted', 'schema': 'schema_registry.schema_accepted.emitted.v1', 'topic': 'pbc.schema_registry.events', 'outbox_table': 'schema_registry_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'BreakingSchemaBlocked', 'schema': 'schema_registry.breaking_schema_blocked.emitted.v1', 'topic': 'pbc.schema_registry.events', 'outbox_table': 'schema_registry_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'PbcDeployed', 'schema': 'schema_registry.pbc_deployed.consumed.v1', 'topic': 'pbc.schema_registry.inbox', 'inbox_table': 'schema_registry_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'EventContractProposed', 'schema': 'schema_registry.event_contract_proposed.consumed.v1', 'topic': 'pbc.schema_registry.inbox', 'inbox_table': 'schema_registry_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'schema_registry_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'schema_registry_appgen_inbox_event'}}


class SchemaRegistryService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'schema_registry',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_schemas(self, payload=None):
        return self._command('command_schemas', payload or {})

    def command_compatibility_checks(self, payload=None):
        return self._command('command_compatibility_checks', payload or {})

    def query_subjects(self, payload=None):
        return self._command('query_subjects', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = SchemaRegistryService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'schema_registry',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = SchemaRegistryService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
