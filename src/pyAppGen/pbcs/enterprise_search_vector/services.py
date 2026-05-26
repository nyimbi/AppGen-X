"""Command service layer for the enterprise_search_vector PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.enterprise_search_vector.events', 'inbox_topic': 'pbc.enterprise_search_vector.inbox', 'outbox_table': 'enterprise_search_vector_appgen_outbox_event', 'inbox_table': 'enterprise_search_vector_appgen_inbox_event', 'dead_letter_table': 'enterprise_search_vector_appgen_dead_letter_event', 'emitted': ({'event_type': 'SearchIndexUpdated', 'schema': 'enterprise_search_vector.search_index_updated.emitted.v1', 'topic': 'pbc.enterprise_search_vector.events', 'outbox_table': 'enterprise_search_vector_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'DiscoveryInsightGenerated', 'schema': 'enterprise_search_vector.discovery_insight_generated.emitted.v1', 'topic': 'pbc.enterprise_search_vector.events', 'outbox_table': 'enterprise_search_vector_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'ProductPublished', 'schema': 'enterprise_search_vector.product_published.consumed.v1', 'topic': 'pbc.enterprise_search_vector.inbox', 'inbox_table': 'enterprise_search_vector_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'CustomerUpdated', 'schema': 'enterprise_search_vector.customer_updated.consumed.v1', 'topic': 'pbc.enterprise_search_vector.inbox', 'inbox_table': 'enterprise_search_vector_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AuditEventSealed', 'schema': 'enterprise_search_vector.audit_event_sealed.consumed.v1', 'topic': 'pbc.enterprise_search_vector.inbox', 'inbox_table': 'enterprise_search_vector_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'enterprise_search_vector_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'enterprise_search_vector_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_indexes', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_search_vector/indexes', 'permission': 'enterprise_search_vector.command.1', 'owned_tables': ('enterprise_search_vector_search_index', 'enterprise_search_vector_embedding_job', 'enterprise_search_vector_vector_document', 'enterprise_search_vector_query_trace'), 'read_tables': (), 'emitted_event': 'SearchIndexUpdated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_embeddings', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_search_vector/embeddings', 'permission': 'enterprise_search_vector.command.2', 'owned_tables': ('enterprise_search_vector_search_index', 'enterprise_search_vector_embedding_job', 'enterprise_search_vector_vector_document', 'enterprise_search_vector_query_trace'), 'read_tables': (), 'emitted_event': 'DiscoveryInsightGenerated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_search', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_search_vector/search', 'permission': 'enterprise_search_vector.command.3', 'owned_tables': ('enterprise_search_vector_search_index', 'enterprise_search_vector_embedding_job', 'enterprise_search_vector_vector_document', 'enterprise_search_vector_query_trace'), 'read_tables': (), 'emitted_event': 'SearchIndexUpdated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item['operation'] for item in OPERATION_CONTRACTS)
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS),
        'pbc': 'enterprise_search_vector',
        'operations': operations,
        'contracts': OPERATION_CONTRACTS,
        'side_effects': (),
    }


def operation_plan(operation_name, payload=None):
    """Plan one service operation without mutating state."""
    contract = next((item for item in OPERATION_CONTRACTS if item['operation'] == operation_name), None)
    if contract is None:
        return {'ok': False, 'reason': 'unknown_operation', 'operation': operation_name, 'side_effects': ()}
    supplied = dict(payload or {})
    table_scope = contract['owned_tables'] or contract['read_tables']
    return {
        'ok': bool(table_scope) and contract['event_contract'] == 'AppGen-X',
        'pbc': 'enterprise_search_vector',
        'operation': operation_name,
        'operation_kind': contract['operation_kind'],
        'route': {'method': contract['method'], 'path': contract['path']},
        'permission': contract['permission'],
        'owned_tables': contract['owned_tables'],
        'read_tables': contract['read_tables'],
        'emitted_event': contract['emitted_event'],
        'payload_keys': tuple(sorted(supplied)),
        'transaction_boundary': contract['transaction_boundary'],
        'event_contract': contract['event_contract'],
        'side_effects': (),
    }


class EnterpriseSearchVectorService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        plan = operation_plan(command_name, payload)
        event_type = plan.get('emitted_event') or (EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted')
        return {
            'ok': plan['ok'],
            'pbc': 'enterprise_search_vector',
            'command': command_name,
            'payload': dict(payload),
            'operation_contract': plan,
            'transaction_boundary': plan.get('transaction_boundary'),
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_indexes(self, payload=None):
        return self._command('command_indexes', payload or {})

    def command_embeddings(self, payload=None):
        return self._command('command_embeddings', payload or {})

    def command_search(self, payload=None):
        return self._command('command_search', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = EnterpriseSearchVectorService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'enterprise_search_vector',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'operation_contracts': service_operation_contracts()['contracts'],
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = EnterpriseSearchVectorService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok']
        and result.get('ok') is True
        and result.get('operation_contract', {}).get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
