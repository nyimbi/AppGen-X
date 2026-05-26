"""Command service layer for the customer_360 PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.customer_360.events', 'inbox_topic': 'pbc.customer_360.inbox', 'outbox_table': 'customer_360_appgen_outbox_event', 'inbox_table': 'customer_360_appgen_inbox_event', 'dead_letter_table': 'customer_360_appgen_dead_letter_event', 'emitted': ({'event_type': 'CustomerUpdated', 'schema': 'customer_360.customer_updated.emitted.v1', 'topic': 'pbc.customer_360.events', 'outbox_table': 'customer_360_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PreferenceChanged', 'schema': 'customer_360.preference_changed.emitted.v1', 'topic': 'pbc.customer_360.events', 'outbox_table': 'customer_360_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'InvoiceIssued', 'schema': 'customer_360.invoice_issued.consumed.v1', 'topic': 'pbc.customer_360.inbox', 'inbox_table': 'customer_360_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PaymentCaptured', 'schema': 'customer_360.payment_captured.consumed.v1', 'topic': 'pbc.customer_360.inbox', 'inbox_table': 'customer_360_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'CandidateHired', 'schema': 'customer_360.candidate_hired.consumed.v1', 'topic': 'pbc.customer_360.inbox', 'inbox_table': 'customer_360_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'customer_360_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'customer_360_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_profiles', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/customer_360/profiles', 'permission': 'customer_360.command.1', 'owned_tables': ('customer_360_customer_profile', 'customer_360_engagement_event', 'customer_360_communication_preference', 'customer_360_touchpoint'), 'read_tables': (), 'emitted_event': 'CustomerUpdated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_touchpoints', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/customer_360/touchpoints', 'permission': 'customer_360.command.2', 'owned_tables': ('customer_360_customer_profile', 'customer_360_engagement_event', 'customer_360_communication_preference', 'customer_360_touchpoint'), 'read_tables': (), 'emitted_event': 'PreferenceChanged', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_customer_timeline', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/customer_360/customer-timeline', 'permission': 'customer_360.query.3', 'owned_tables': (), 'read_tables': ('customer_360_customer_profile', 'customer_360_engagement_event', 'customer_360_communication_preference', 'customer_360_touchpoint'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item['operation'] for item in OPERATION_CONTRACTS)
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS),
        'pbc': 'customer_360',
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
        'pbc': 'customer_360',
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


class Customer360Service:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        plan = operation_plan(command_name, payload)
        event_type = plan.get('emitted_event') or (EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted')
        return {
            'ok': plan['ok'],
            'pbc': 'customer_360',
            'command': command_name,
            'payload': dict(payload),
            'operation_contract': plan,
            'transaction_boundary': plan.get('transaction_boundary'),
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_profiles(self, payload=None):
        return self._command('command_profiles', payload or {})

    def command_touchpoints(self, payload=None):
        return self._command('command_touchpoints', payload or {})

    def query_customer_timeline(self, payload=None):
        return self._command('query_customer_timeline', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = Customer360Service()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'customer_360',
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
    service = Customer360Service()
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
