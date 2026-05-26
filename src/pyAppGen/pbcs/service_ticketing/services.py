"""Command service layer for the service_ticketing PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.service_ticketing.events', 'inbox_topic': 'pbc.service_ticketing.inbox', 'outbox_table': 'service_ticketing_appgen_outbox_event', 'inbox_table': 'service_ticketing_appgen_inbox_event', 'dead_letter_table': 'service_ticketing_appgen_dead_letter_event', 'emitted': ({'event_type': 'SupportCaseOpened', 'schema': 'service_ticketing.support_case_opened.emitted.v1', 'topic': 'pbc.service_ticketing.events', 'outbox_table': 'service_ticketing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'SlaBreached', 'schema': 'service_ticketing.sla_breached.emitted.v1', 'topic': 'pbc.service_ticketing.events', 'outbox_table': 'service_ticketing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'CustomerUpdated', 'schema': 'service_ticketing.customer_updated.consumed.v1', 'topic': 'pbc.service_ticketing.inbox', 'inbox_table': 'service_ticketing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PreferenceChanged', 'schema': 'service_ticketing.preference_changed.consumed.v1', 'topic': 'pbc.service_ticketing.inbox', 'inbox_table': 'service_ticketing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'service_ticketing_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'service_ticketing_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_tickets', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/service_ticketing/tickets', 'permission': 'service_ticketing.command.1', 'owned_tables': ('service_ticketing_support_ticket', 'service_ticketing_sla_policy', 'service_ticketing_case_assignment', 'service_ticketing_escalation_event'), 'read_tables': (), 'emitted_event': 'SupportCaseOpened', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_assignments', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/service_ticketing/assignments', 'permission': 'service_ticketing.command.2', 'owned_tables': ('service_ticketing_support_ticket', 'service_ticketing_sla_policy', 'service_ticketing_case_assignment', 'service_ticketing_escalation_event'), 'read_tables': (), 'emitted_event': 'SlaBreached', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_sla_status', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/service_ticketing/sla-status', 'permission': 'service_ticketing.query.3', 'owned_tables': (), 'read_tables': ('service_ticketing_support_ticket', 'service_ticketing_sla_policy', 'service_ticketing_case_assignment', 'service_ticketing_escalation_event'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item['operation'] for item in OPERATION_CONTRACTS)
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item['operation_kind'] == 'command')
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item['operation_kind'] == 'query')
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS)
        and all(item['emitted_event'] for item in command_contracts)
        and all(item['owned_tables'] and not item['read_tables'] for item in command_contracts)
        and all(item['emitted_event'] is None for item in query_contracts)
        and all(item['read_tables'] and not item['owned_tables'] for item in query_contracts),
        'pbc': 'service_ticketing',
        'operations': operations,
        'command_operations': tuple(item['operation'] for item in command_contracts),
        'query_operations': tuple(item['operation'] for item in query_contracts),
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
        'pbc': 'service_ticketing',
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


class ServiceTicketingService:
    """Side-effect-free generated command facade."""

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get('operation_kind')
        result = {
            'ok': plan['ok'],
            'pbc': 'service_ticketing',
            'operation': operation_name,
            'operation_kind': operation_kind,
            'payload': dict(payload),
            'operation_contract': plan,
            'transaction_boundary': plan.get('transaction_boundary'),
            'side_effects': (),
        }
        if operation_kind == 'command':
            event_type = plan.get('emitted_event')
            result.update({
                'command': operation_name,
                'read_only': False,
                'outbox_table': EVENT_CONTRACT['outbox_table'],
                'emits': (event_type,) if event_type else (),
            })
        elif operation_kind == 'query':
            result.update({
                'query': operation_name,
                'read_only': True,
                'outbox_table': None,
                'emits': (),
            })
        return result

    def _command(self, command_name, payload):
        return self._execute(command_name, payload)

    def _query(self, query_name, payload):
        return self._execute(query_name, payload)

    def command_tickets(self, payload=None):
        return self._command('command_tickets', payload or {})

    def command_assignments(self, payload=None):
        return self._command('command_assignments', payload or {})

    def query_sla_status(self, payload=None):
        return self._query('query_sla_status', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = ServiceTicketingService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'service_ticketing',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'command_operations': service_operation_contracts()['command_operations'],
        'query_operations': service_operation_contracts()['query_operations'],
        'operation_contracts': service_operation_contracts()['contracts'],
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = ServiceTicketingService()
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
