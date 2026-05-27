"""Command service layer for the subscription_billing PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.subscription_billing.events', 'inbox_topic': 'pbc.subscription_billing.inbox', 'outbox_table': 'subscription_billing_appgen_outbox_event', 'inbox_table': 'subscription_billing_appgen_inbox_event', 'dead_letter_table': 'subscription_billing_appgen_dead_letter_event', 'emitted': ({'event_type': 'SubscriptionRenewed', 'schema': 'subscription_billing.subscription_renewed.emitted.v1', 'topic': 'pbc.subscription_billing.events', 'outbox_table': 'subscription_billing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'UsageRated', 'schema': 'subscription_billing.usage_rated.emitted.v1', 'topic': 'pbc.subscription_billing.events', 'outbox_table': 'subscription_billing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'InvoiceApproved', 'schema': 'subscription_billing.invoice_approved.emitted.v1', 'topic': 'pbc.subscription_billing.events', 'outbox_table': 'subscription_billing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'PaymentCaptured', 'schema': 'subscription_billing.payment_captured.consumed.v1', 'topic': 'pbc.subscription_billing.inbox', 'inbox_table': 'subscription_billing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PriceOptimized', 'schema': 'subscription_billing.price_optimized.consumed.v1', 'topic': 'pbc.subscription_billing.inbox', 'inbox_table': 'subscription_billing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'subscription_billing_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'subscription_billing_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_subscriptions', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/subscription_billing/subscriptions', 'permission': 'subscription_billing.command.1', 'owned_tables': ('subscription_billing_subscription', 'subscription_billing_usage_meter', 'subscription_billing_billing_schedule', 'subscription_billing_dunning_notice'), 'read_tables': (), 'emitted_event': 'SubscriptionRenewed', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_usage', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/subscription_billing/usage', 'permission': 'subscription_billing.command.2', 'owned_tables': ('subscription_billing_subscription', 'subscription_billing_usage_meter', 'subscription_billing_billing_schedule', 'subscription_billing_dunning_notice'), 'read_tables': (), 'emitted_event': 'UsageRated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_renewals', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/subscription_billing/renewals', 'permission': 'subscription_billing.command.3', 'owned_tables': ('subscription_billing_subscription', 'subscription_billing_usage_meter', 'subscription_billing_billing_schedule', 'subscription_billing_dunning_notice'), 'read_tables': (), 'emitted_event': 'InvoiceApproved', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_subscription_billing_workbench', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/subscription_billing/subscription-billing-workbench', 'permission': 'subscription_billing.query.4', 'owned_tables': (), 'read_tables': ('subscription_billing_subscription', 'subscription_billing_usage_meter', 'subscription_billing_billing_schedule', 'subscription_billing_dunning_notice'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})

OPERATION_CONTRACTS = OPERATION_CONTRACTS + (
    {'operation': 'command_trials', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/subscription_billing/trials', 'permission': 'subscription_billing.subscription', 'owned_tables': ('subscription_billing_trial_period',), 'read_tables': (), 'emitted_event': 'SubscriptionActivated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_change_orders', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/subscription_billing/change-orders', 'permission': 'subscription_billing.subscription', 'owned_tables': ('subscription_billing_subscription_change_order', 'subscription_billing_subscription', 'subscription_billing_subscription_phase'), 'read_tables': (), 'emitted_event': 'SubscriptionChanged', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_cancellations', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/subscription_billing/cancellations', 'permission': 'subscription_billing.subscription', 'owned_tables': ('subscription_billing_subscription', 'subscription_billing_billing_schedule'), 'read_tables': (), 'emitted_event': 'SubscriptionCancelled', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_addons', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/subscription_billing/addons', 'permission': 'subscription_billing.subscription', 'owned_tables': ('subscription_billing_subscription_addon', 'subscription_billing_subscription'), 'read_tables': (), 'emitted_event': 'SubscriptionChanged', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_credit_memos', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/subscription_billing/credit-memos', 'permission': 'subscription_billing.invoice', 'owned_tables': ('subscription_billing_credit_memo', 'subscription_billing_invoice'), 'read_tables': (), 'emitted_event': 'CreditMemoIssued', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_payment_applications', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/subscription_billing/payment-applications', 'permission': 'subscription_billing.invoice', 'owned_tables': ('subscription_billing_payment_application', 'subscription_billing_invoice'), 'read_tables': (), 'emitted_event': 'PaymentApplied', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_entitlements', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/subscription_billing/entitlements', 'permission': 'subscription_billing.entitlement', 'owned_tables': ('subscription_billing_entitlement_grant',), 'read_tables': (), 'emitted_event': 'EntitlementGranted', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_revenue', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/subscription_billing/revenue-recognition', 'permission': 'subscription_billing.revenue', 'owned_tables': ('subscription_billing_revenue_schedule',), 'read_tables': (), 'emitted_event': 'RevenueRecognized', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_billing_exceptions', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/subscription_billing/billing-exceptions', 'permission': 'subscription_billing.audit', 'owned_tables': ('subscription_billing_billing_exception',), 'read_tables': (), 'emitted_event': 'DunningNoticeCreated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
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
        'pbc': 'subscription_billing',
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
        'pbc': 'subscription_billing',
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


class SubscriptionBillingService:
    """Side-effect-free generated command facade."""

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get('operation_kind')
        result = {
            'ok': plan['ok'],
            'pbc': 'subscription_billing',
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

    def command_subscriptions(self, payload=None):
        return self._command('command_subscriptions', payload or {})

    def command_usage(self, payload=None):
        return self._command('command_usage', payload or {})

    def command_renewals(self, payload=None):
        return self._command('command_renewals', payload or {})

    def command_trials(self, payload=None):
        return self._command('command_trials', payload or {})

    def command_change_orders(self, payload=None):
        return self._command('command_change_orders', payload or {})

    def command_cancellations(self, payload=None):
        return self._command('command_cancellations', payload or {})

    def command_addons(self, payload=None):
        return self._command('command_addons', payload or {})

    def command_credit_memos(self, payload=None):
        return self._command('command_credit_memos', payload or {})

    def command_payment_applications(self, payload=None):
        return self._command('command_payment_applications', payload or {})

    def command_entitlements(self, payload=None):
        return self._command('command_entitlements', payload or {})

    def command_revenue(self, payload=None):
        return self._command('command_revenue', payload or {})

    def command_billing_exceptions(self, payload=None):
        return self._command('command_billing_exceptions', payload or {})

    def query_subscription_billing_workbench(self, payload=None):
        return self._query('query_subscription_billing_workbench', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = SubscriptionBillingService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'subscription_billing',
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
    service = SubscriptionBillingService()
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
