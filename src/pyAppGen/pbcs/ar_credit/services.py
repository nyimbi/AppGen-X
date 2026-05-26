"""Command service layer for the ar_credit PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.ar_credit.events', 'inbox_topic': 'pbc.ar_credit.inbox', 'outbox_table': 'ar_credit_appgen_outbox_event', 'inbox_table': 'ar_credit_appgen_inbox_event', 'dead_letter_table': 'ar_credit_appgen_dead_letter_event', 'emitted': ({'event_type': 'CustomerOnboarded', 'schema': 'ar_credit.customer_onboarded.emitted.v1', 'topic': 'pbc.ar_credit.events', 'outbox_table': 'ar_credit_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'InvoiceIssued', 'schema': 'ar_credit.invoice_issued.emitted.v1', 'topic': 'pbc.ar_credit.events', 'outbox_table': 'ar_credit_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'DeliveryConfirmed', 'schema': 'ar_credit.delivery_confirmed.emitted.v1', 'topic': 'pbc.ar_credit.events', 'outbox_table': 'ar_credit_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PaymentReceived', 'schema': 'ar_credit.payment_received.emitted.v1', 'topic': 'pbc.ar_credit.events', 'outbox_table': 'ar_credit_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'UnappliedCashRecorded', 'schema': 'ar_credit.unapplied_cash_recorded.emitted.v1', 'topic': 'pbc.ar_credit.events', 'outbox_table': 'ar_credit_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'CreditMemoIssued', 'schema': 'ar_credit.credit_memo_issued.emitted.v1', 'topic': 'pbc.ar_credit.events', 'outbox_table': 'ar_credit_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ReceivableWrittenOff', 'schema': 'ar_credit.receivable_written_off.emitted.v1', 'topic': 'pbc.ar_credit.events', 'outbox_table': 'ar_credit_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'CustomerRefundScheduled', 'schema': 'ar_credit.customer_refund_scheduled.emitted.v1', 'topic': 'pbc.ar_credit.events', 'outbox_table': 'ar_credit_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'CollectionActionScheduled', 'schema': 'ar_credit.collection_action_scheduled.emitted.v1', 'topic': 'pbc.ar_credit.events', 'outbox_table': 'ar_credit_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'CustomerIdentityVerified', 'schema': 'ar_credit.customer_identity_verified.consumed.v1', 'topic': 'pbc.ar_credit.inbox', 'inbox_table': 'ar_credit_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'DeliveryConfirmed', 'schema': 'ar_credit.delivery_confirmed.consumed.v1', 'topic': 'pbc.ar_credit.inbox', 'inbox_table': 'ar_credit_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'TaxPolicyChanged', 'schema': 'ar_credit.tax_policy_changed.consumed.v1', 'topic': 'pbc.ar_credit.inbox', 'inbox_table': 'ar_credit_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'CashForecastUpdated', 'schema': 'ar_credit.cash_forecast_updated.consumed.v1', 'topic': 'pbc.ar_credit.inbox', 'inbox_table': 'ar_credit_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AccessPolicyChanged', 'schema': 'ar_credit.access_policy_changed.consumed.v1', 'topic': 'pbc.ar_credit.inbox', 'inbox_table': 'ar_credit_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'CollectionPolicyChanged', 'schema': 'ar_credit.collection_policy_changed.consumed.v1', 'topic': 'pbc.ar_credit.inbox', 'inbox_table': 'ar_credit_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'ar_credit_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'ar_credit_appgen_inbox_event'}}


class ArCreditService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'ar_credit',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_ar_customers(self, payload=None):
        return self._command('command_ar_customers', payload or {})

    def command_ar_invoices(self, payload=None):
        return self._command('command_ar_invoices', payload or {})

    def command_ar_deliveries(self, payload=None):
        return self._command('command_ar_deliveries', payload or {})

    def command_ar_remittances_parse(self, payload=None):
        return self._command('command_ar_remittances_parse', payload or {})

    def command_ar_cash_applications(self, payload=None):
        return self._command('command_ar_cash_applications', payload or {})

    def command_ar_unapplied_cash(self, payload=None):
        return self._command('command_ar_unapplied_cash', payload or {})

    def command_ar_credit_memos(self, payload=None):
        return self._command('command_ar_credit_memos', payload or {})

    def command_ar_write_offs(self, payload=None):
        return self._command('command_ar_write_offs', payload or {})

    def command_ar_refunds(self, payload=None):
        return self._command('command_ar_refunds', payload or {})

    def command_ar_disputes(self, payload=None):
        return self._command('command_ar_disputes', payload or {})

    def command_ar_collections(self, payload=None):
        return self._command('command_ar_collections', payload or {})

    def command_ar_e_invoices(self, payload=None):
        return self._command('command_ar_e_invoices', payload or {})

    def query_ar_aging(self, payload=None):
        return self._command('query_ar_aging', payload or {})

    def query_ar_statements_customer_id(self, payload=None):
        return self._command('query_ar_statements_customer_id', payload or {})

    def query_ar_revenue_schedules_invoice_id(self, payload=None):
        return self._command('query_ar_revenue_schedules_invoice_id', payload or {})

    def query_ar_workbench(self, payload=None):
        return self._command('query_ar_workbench', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = ArCreditService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'ar_credit',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = ArCreditService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
