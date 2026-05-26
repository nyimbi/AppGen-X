"""Command service layer for the tax_localization PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.tax_localization.events', 'inbox_topic': 'pbc.tax_localization.inbox', 'outbox_table': 'tax_localization_appgen_outbox_event', 'inbox_table': 'tax_localization_appgen_inbox_event', 'dead_letter_table': 'tax_localization_appgen_dead_letter_event', 'emitted': ({'event_type': 'TaxJurisdictionRegistered', 'schema': 'tax_localization.tax_jurisdiction_registered.emitted.v1', 'topic': 'pbc.tax_localization.events', 'outbox_table': 'tax_localization_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'TaxRuleActivated', 'schema': 'tax_localization.tax_rule_activated.emitted.v1', 'topic': 'pbc.tax_localization.events', 'outbox_table': 'tax_localization_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'TaxCalculated', 'schema': 'tax_localization.tax_calculated.emitted.v1', 'topic': 'pbc.tax_localization.events', 'outbox_table': 'tax_localization_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'InvoiceTaxRecorded', 'schema': 'tax_localization.invoice_tax_recorded.emitted.v1', 'topic': 'pbc.tax_localization.events', 'outbox_table': 'tax_localization_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'TaxFilingPrepared', 'schema': 'tax_localization.tax_filing_prepared.emitted.v1', 'topic': 'pbc.tax_localization.events', 'outbox_table': 'tax_localization_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'ProductClassified', 'schema': 'tax_localization.product_classified.consumed.v1', 'topic': 'pbc.tax_localization.inbox', 'inbox_table': 'tax_localization_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'InvoiceIssued', 'schema': 'tax_localization.invoice_issued.consumed.v1', 'topic': 'pbc.tax_localization.inbox', 'inbox_table': 'tax_localization_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'OrderPriced', 'schema': 'tax_localization.order_priced.consumed.v1', 'topic': 'pbc.tax_localization.inbox', 'inbox_table': 'tax_localization_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PaymentCollected', 'schema': 'tax_localization.payment_collected.consumed.v1', 'topic': 'pbc.tax_localization.inbox', 'inbox_table': 'tax_localization_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AccessPolicyChanged', 'schema': 'tax_localization.access_policy_changed.consumed.v1', 'topic': 'pbc.tax_localization.inbox', 'inbox_table': 'tax_localization_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'tax_localization_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'tax_localization_appgen_inbox_event'}}


class TaxLocalizationService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'tax_localization',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_tax_jurisdictions(self, payload=None):
        return self._command('command_tax_jurisdictions', payload or {})

    def command_tax_rules(self, payload=None):
        return self._command('command_tax_rules', payload or {})

    def command_tax_quotes(self, payload=None):
        return self._command('command_tax_quotes', payload or {})

    def command_tax_invoices_id_tax_records(self, payload=None):
        return self._command('command_tax_invoices_id_tax_records', payload or {})

    def command_tax_filings(self, payload=None):
        return self._command('command_tax_filings', payload or {})

    def command_tax_events_inbox(self, payload=None):
        return self._command('command_tax_events_inbox', payload or {})

    def query_tax_workbench(self, payload=None):
        return self._command('query_tax_workbench', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = TaxLocalizationService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'tax_localization',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = TaxLocalizationService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
