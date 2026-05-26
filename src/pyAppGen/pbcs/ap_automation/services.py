"""Command service layer for the ap_automation PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.ap_automation.events', 'inbox_topic': 'pbc.ap_automation.inbox', 'outbox_table': 'ap_automation_appgen_outbox_event', 'inbox_table': 'ap_automation_appgen_inbox_event', 'dead_letter_table': 'ap_automation_appgen_dead_letter_event', 'emitted': ({'event_type': 'VendorOnboarded', 'schema': 'ap_automation.vendor_onboarded.emitted.v1', 'topic': 'pbc.ap_automation.events', 'outbox_table': 'ap_automation_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PurchaseOrderIssued', 'schema': 'ap_automation.purchase_order_issued.emitted.v1', 'topic': 'pbc.ap_automation.events', 'outbox_table': 'ap_automation_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'GoodsReceiptRecorded', 'schema': 'ap_automation.goods_receipt_recorded.emitted.v1', 'topic': 'pbc.ap_automation.events', 'outbox_table': 'ap_automation_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'InvoiceCaptured', 'schema': 'ap_automation.invoice_captured.emitted.v1', 'topic': 'pbc.ap_automation.events', 'outbox_table': 'ap_automation_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PaymentScheduled', 'schema': 'ap_automation.payment_scheduled.emitted.v1', 'topic': 'pbc.ap_automation.events', 'outbox_table': 'ap_automation_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PaymentExecuted', 'schema': 'ap_automation.payment_executed.emitted.v1', 'topic': 'pbc.ap_automation.events', 'outbox_table': 'ap_automation_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'InvoiceExceptionResolved', 'schema': 'ap_automation.invoice_exception_resolved.emitted.v1', 'topic': 'pbc.ap_automation.events', 'outbox_table': 'ap_automation_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'VendorRiskChanged', 'schema': 'ap_automation.vendor_risk_changed.emitted.v1', 'topic': 'pbc.ap_automation.events', 'outbox_table': 'ap_automation_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'DiscountOpportunityCaptured', 'schema': 'ap_automation.discount_opportunity_captured.emitted.v1', 'topic': 'pbc.ap_automation.events', 'outbox_table': 'ap_automation_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'VendorApproved', 'schema': 'ap_automation.vendor_approved.consumed.v1', 'topic': 'pbc.ap_automation.inbox', 'inbox_table': 'ap_automation_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PurchaseOrderApproved', 'schema': 'ap_automation.purchase_order_approved.consumed.v1', 'topic': 'pbc.ap_automation.inbox', 'inbox_table': 'ap_automation_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'GoodsReceiptPosted', 'schema': 'ap_automation.goods_receipt_posted.consumed.v1', 'topic': 'pbc.ap_automation.inbox', 'inbox_table': 'ap_automation_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'TaxPolicyChanged', 'schema': 'ap_automation.tax_policy_changed.consumed.v1', 'topic': 'pbc.ap_automation.inbox', 'inbox_table': 'ap_automation_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'CashForecastUpdated', 'schema': 'ap_automation.cash_forecast_updated.consumed.v1', 'topic': 'pbc.ap_automation.inbox', 'inbox_table': 'ap_automation_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AccessPolicyChanged', 'schema': 'ap_automation.access_policy_changed.consumed.v1', 'topic': 'pbc.ap_automation.inbox', 'inbox_table': 'ap_automation_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'ap_automation_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'ap_automation_appgen_inbox_event'}}


class ApAutomationService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'ap_automation',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_ap_vendors(self, payload=None):
        return self._command('command_ap_vendors', payload or {})

    def command_ap_vendor_bank_accounts(self, payload=None):
        return self._command('command_ap_vendor_bank_accounts', payload or {})

    def command_ap_vendor_tax_profiles(self, payload=None):
        return self._command('command_ap_vendor_tax_profiles', payload or {})

    def command_ap_purchase_orders(self, payload=None):
        return self._command('command_ap_purchase_orders', payload or {})

    def command_ap_goods_receipts(self, payload=None):
        return self._command('command_ap_goods_receipts', payload or {})

    def command_ap_invoices(self, payload=None):
        return self._command('command_ap_invoices', payload or {})

    def command_ap_invoices_invoice_id_match(self, payload=None):
        return self._command('command_ap_invoices_invoice_id_match', payload or {})

    def command_ap_exceptions(self, payload=None):
        return self._command('command_ap_exceptions', payload or {})

    def command_ap_approval_tasks(self, payload=None):
        return self._command('command_ap_approval_tasks', payload or {})

    def command_ap_payment_schedules(self, payload=None):
        return self._command('command_ap_payment_schedules', payload or {})

    def command_ap_payment_batches(self, payload=None):
        return self._command('command_ap_payment_batches', payload or {})

    def command_ap_payments(self, payload=None):
        return self._command('command_ap_payments', payload or {})

    def command_ap_e_invoices(self, payload=None):
        return self._command('command_ap_e_invoices', payload or {})

    def command_ap_vendor_statements_reconcile(self, payload=None):
        return self._command('command_ap_vendor_statements_reconcile', payload or {})

    def query_ap_workbench(self, payload=None):
        return self._command('query_ap_workbench', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = ApAutomationService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'ap_automation',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = ApAutomationService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
