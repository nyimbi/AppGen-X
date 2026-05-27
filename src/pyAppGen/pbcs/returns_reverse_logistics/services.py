"""Command service layer for the returns_reverse_logistics PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.returns_reverse_logistics.events', 'inbox_topic': 'pbc.returns_reverse_logistics.inbox', 'outbox_table': 'returns_reverse_logistics_appgen_outbox_event', 'inbox_table': 'returns_reverse_logistics_appgen_inbox_event', 'dead_letter_table': 'returns_reverse_logistics_appgen_dead_letter_event', 'emitted': ({'event_type': 'ReturnAuthorized', 'schema': 'returns_reverse_logistics.return_authorized.emitted.v1', 'topic': 'pbc.returns_reverse_logistics.events', 'outbox_table': 'returns_reverse_logistics_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'CreditAdjustmentIssued', 'schema': 'returns_reverse_logistics.credit_adjustment_issued.emitted.v1', 'topic': 'pbc.returns_reverse_logistics.events', 'outbox_table': 'returns_reverse_logistics_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'OrderShipped', 'schema': 'returns_reverse_logistics.order_shipped.consumed.v1', 'topic': 'pbc.returns_reverse_logistics.inbox', 'inbox_table': 'returns_reverse_logistics_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PaymentCaptured', 'schema': 'returns_reverse_logistics.payment_captured.consumed.v1', 'topic': 'pbc.returns_reverse_logistics.inbox', 'inbox_table': 'returns_reverse_logistics_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'returns_reverse_logistics_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'returns_reverse_logistics_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_returns', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/returns_reverse_logistics/returns', 'permission': 'returns_reverse_logistics.command.1', 'owned_tables': ('returns_reverse_logistics_return_authorization', 'returns_reverse_logistics_return_label', 'returns_reverse_logistics_inspection_grade', 'returns_reverse_logistics_credit_adjustment'), 'read_tables': (), 'emitted_event': 'ReturnAuthorized', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_labels', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/returns_reverse_logistics/labels', 'permission': 'returns_reverse_logistics.command.2', 'owned_tables': ('returns_reverse_logistics_return_authorization', 'returns_reverse_logistics_return_label', 'returns_reverse_logistics_inspection_grade', 'returns_reverse_logistics_credit_adjustment'), 'read_tables': (), 'emitted_event': 'CreditAdjustmentIssued', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_inspection_grades', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/returns_reverse_logistics/inspection-grades', 'permission': 'returns_reverse_logistics.command.3', 'owned_tables': ('returns_reverse_logistics_return_authorization', 'returns_reverse_logistics_return_label', 'returns_reverse_logistics_inspection_grade', 'returns_reverse_logistics_credit_adjustment'), 'read_tables': (), 'emitted_event': 'ReturnAuthorized', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_returns_reverse_logistics_workbench', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/returns_reverse_logistics/returns-reverse-logistics-workbench', 'permission': 'returns_reverse_logistics.query.4', 'owned_tables': (), 'read_tables': ('returns_reverse_logistics_return_authorization', 'returns_reverse_logistics_return_label', 'returns_reverse_logistics_inspection_grade', 'returns_reverse_logistics_credit_adjustment'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})

OPERATION_CONTRACTS = OPERATION_CONTRACTS + (
    {'operation': 'command_receipts', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/returns_reverse_logistics/receipts', 'permission': 'returns_reverse_logistics.inspect', 'owned_tables': ('returns_reverse_logistics_return_receipt', 'returns_reverse_logistics_return_customer_status'), 'read_tables': (), 'emitted_event': 'ReturnAuthorized', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_dispositions', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/returns_reverse_logistics/dispositions', 'permission': 'returns_reverse_logistics.adjust', 'owned_tables': ('returns_reverse_logistics_disposition_decision', 'returns_reverse_logistics_restocking_order', 'returns_reverse_logistics_repair_refurbishment_order', 'returns_reverse_logistics_carrier_claim'), 'read_tables': (), 'emitted_event': 'CreditAdjustmentIssued', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_refund_exchange', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/returns_reverse_logistics/refund-exchange', 'permission': 'returns_reverse_logistics.adjust', 'owned_tables': ('returns_reverse_logistics_refund_exchange_resolution', 'returns_reverse_logistics_return_customer_status'), 'read_tables': (), 'emitted_event': 'CreditAdjustmentIssued', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_restocking', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/returns_reverse_logistics/restocking-orders', 'permission': 'returns_reverse_logistics.adjust', 'owned_tables': ('returns_reverse_logistics_restocking_order',), 'read_tables': (), 'emitted_event': 'CreditAdjustmentIssued', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_repair_refurbishment', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/returns_reverse_logistics/repair-refurbishment-orders', 'permission': 'returns_reverse_logistics.adjust', 'owned_tables': ('returns_reverse_logistics_repair_refurbishment_order',), 'read_tables': (), 'emitted_event': 'CreditAdjustmentIssued', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_carrier_claims', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/returns_reverse_logistics/carrier-claims', 'permission': 'returns_reverse_logistics.claim', 'owned_tables': ('returns_reverse_logistics_carrier_claim', 'returns_reverse_logistics_carrier_claim_projection'), 'read_tables': (), 'emitted_event': 'CreditAdjustmentIssued', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_customer_status', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/returns_reverse_logistics/customer-status', 'permission': 'returns_reverse_logistics.audit', 'owned_tables': ('returns_reverse_logistics_return_customer_status',), 'read_tables': (), 'emitted_event': 'ReturnAuthorized', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_exception_cases', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/returns_reverse_logistics/exception-cases', 'permission': 'returns_reverse_logistics.exception', 'owned_tables': ('returns_reverse_logistics_return_exception_case', 'returns_reverse_logistics_return_exception_task'), 'read_tables': (), 'emitted_event': 'ReturnAuthorized', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
)


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
        'pbc': 'returns_reverse_logistics',
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
        'pbc': 'returns_reverse_logistics',
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


class ReturnsReverseLogisticsService:
    """Side-effect-free generated command facade."""

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get('operation_kind')
        result = {
            'ok': plan['ok'],
            'pbc': 'returns_reverse_logistics',
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

    def command_returns(self, payload=None):
        return self._command('command_returns', payload or {})

    def command_labels(self, payload=None):
        return self._command('command_labels', payload or {})

    def command_inspection_grades(self, payload=None):
        return self._command('command_inspection_grades', payload or {})

    def command_receipts(self, payload=None):
        return self._command('command_receipts', payload or {})

    def command_dispositions(self, payload=None):
        return self._command('command_dispositions', payload or {})

    def command_refund_exchange(self, payload=None):
        return self._command('command_refund_exchange', payload or {})

    def command_restocking(self, payload=None):
        return self._command('command_restocking', payload or {})

    def command_repair_refurbishment(self, payload=None):
        return self._command('command_repair_refurbishment', payload or {})

    def command_carrier_claims(self, payload=None):
        return self._command('command_carrier_claims', payload or {})

    def command_customer_status(self, payload=None):
        return self._command('command_customer_status', payload or {})

    def command_exception_cases(self, payload=None):
        return self._command('command_exception_cases', payload or {})

    def query_returns_reverse_logistics_workbench(self, payload=None):
        return self._query('query_returns_reverse_logistics_workbench', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = ReturnsReverseLogisticsService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'returns_reverse_logistics',
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
    service = ReturnsReverseLogisticsService()
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
