"""Command service layer for the payment_orchestration PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.payment_orchestration.events', 'inbox_topic': 'pbc.payment_orchestration.inbox', 'outbox_table': 'payment_orchestration_appgen_outbox_event', 'inbox_table': 'payment_orchestration_appgen_inbox_event', 'dead_letter_table': 'payment_orchestration_appgen_dead_letter_event', 'emitted': ({'event_type': 'PaymentCaptured', 'schema': 'payment_orchestration.payment_captured.emitted.v1', 'topic': 'pbc.payment_orchestration.events', 'outbox_table': 'payment_orchestration_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PaymentFailed', 'schema': 'payment_orchestration.payment_failed.emitted.v1', 'topic': 'pbc.payment_orchestration.events', 'outbox_table': 'payment_orchestration_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'FraudCheckRequested', 'schema': 'payment_orchestration.fraud_check_requested.emitted.v1', 'topic': 'pbc.payment_orchestration.events', 'outbox_table': 'payment_orchestration_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'CheckoutCompleted', 'schema': 'payment_orchestration.checkout_completed.consumed.v1', 'topic': 'pbc.payment_orchestration.inbox', 'inbox_table': 'payment_orchestration_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'FraudRiskScored', 'schema': 'payment_orchestration.fraud_risk_scored.consumed.v1', 'topic': 'pbc.payment_orchestration.inbox', 'inbox_table': 'payment_orchestration_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'payment_orchestration_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'payment_orchestration_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_payment_intents', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/payment_orchestration/payment-intents', 'permission': 'payment_orchestration.command.1', 'owned_tables': ('payment_orchestration_payment_gateway', 'payment_orchestration_payment_intent', 'payment_orchestration_payment_token', 'payment_orchestration_fraud_check'), 'read_tables': (), 'emitted_event': 'PaymentCaptured', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_gateway_routes', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/payment_orchestration/gateway-routes', 'permission': 'payment_orchestration.command.2', 'owned_tables': ('payment_orchestration_payment_gateway', 'payment_orchestration_payment_intent', 'payment_orchestration_payment_token', 'payment_orchestration_fraud_check'), 'read_tables': (), 'emitted_event': 'PaymentFailed', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_tokens', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/payment_orchestration/tokens', 'permission': 'payment_orchestration.command.3', 'owned_tables': ('payment_orchestration_payment_gateway', 'payment_orchestration_payment_intent', 'payment_orchestration_payment_token', 'payment_orchestration_fraud_check'), 'read_tables': (), 'emitted_event': 'FraudCheckRequested', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_payment_orchestration_workbench', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/payment_orchestration/payment-orchestration-workbench', 'permission': 'payment_orchestration.query.4', 'owned_tables': (), 'read_tables': ('payment_orchestration_payment_gateway', 'payment_orchestration_payment_intent', 'payment_orchestration_payment_token', 'payment_orchestration_fraud_check'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})

OPERATION_CONTRACTS = OPERATION_CONTRACTS + (
    {'operation': 'command_authorizations', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/payment_orchestration/authorizations', 'permission': 'payment_orchestration.capture', 'owned_tables': ('payment_orchestration_payment_authorization', 'payment_orchestration_payment_intent'), 'read_tables': (), 'emitted_event': 'PaymentAuthorized', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_captures', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/payment_orchestration/captures', 'permission': 'payment_orchestration.capture', 'owned_tables': ('payment_orchestration_payment_authorization', 'payment_orchestration_payment_capture', 'payment_orchestration_payment_settlement'), 'read_tables': (), 'emitted_event': 'PaymentCaptured', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_settlements', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/payment_orchestration/settlements', 'permission': 'payment_orchestration.settlement', 'owned_tables': ('payment_orchestration_payment_settlement', 'payment_orchestration_payment_reconciliation_handoff'), 'read_tables': (), 'emitted_event': 'PaymentSettled', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_payouts', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/payment_orchestration/payouts', 'permission': 'payment_orchestration.settlement', 'owned_tables': ('payment_orchestration_payment_payout',), 'read_tables': (), 'emitted_event': 'PaymentPayoutScheduled', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_refunds', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/payment_orchestration/refunds', 'permission': 'payment_orchestration.refund', 'owned_tables': ('payment_orchestration_payment_refund', 'payment_orchestration_payment_reconciliation_handoff'), 'read_tables': (), 'emitted_event': 'PaymentRefunded', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_disputes', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/payment_orchestration/disputes', 'permission': 'payment_orchestration.dispute', 'owned_tables': ('payment_orchestration_payment_dispute', 'payment_orchestration_payment_reconciliation_handoff'), 'read_tables': (), 'emitted_event': 'PaymentDisputeResolved', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
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
        'pbc': 'payment_orchestration',
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
        'pbc': 'payment_orchestration',
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


class PaymentOrchestrationService:
    """Side-effect-free generated command facade."""

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get('operation_kind')
        result = {
            'ok': plan['ok'],
            'pbc': 'payment_orchestration',
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

    def command_payment_intents(self, payload=None):
        return self._command('command_payment_intents', payload or {})

    def command_gateway_routes(self, payload=None):
        return self._command('command_gateway_routes', payload or {})

    def command_tokens(self, payload=None):
        return self._command('command_tokens', payload or {})

    def command_authorizations(self, payload=None):
        return self._command('command_authorizations', payload or {})

    def command_captures(self, payload=None):
        return self._command('command_captures', payload or {})

    def command_settlements(self, payload=None):
        return self._command('command_settlements', payload or {})

    def command_payouts(self, payload=None):
        return self._command('command_payouts', payload or {})

    def command_refunds(self, payload=None):
        return self._command('command_refunds', payload or {})

    def command_disputes(self, payload=None):
        return self._command('command_disputes', payload or {})

    def query_payment_orchestration_workbench(self, payload=None):
        return self._query('query_payment_orchestration_workbench', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = PaymentOrchestrationService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'payment_orchestration',
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
    service = PaymentOrchestrationService()
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
