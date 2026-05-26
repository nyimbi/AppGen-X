"""Command service layer for the product_catalog_pim PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.product_catalog_pim.events', 'inbox_topic': 'pbc.product_catalog_pim.inbox', 'outbox_table': 'product_catalog_pim_appgen_outbox_event', 'inbox_table': 'product_catalog_pim_appgen_inbox_event', 'dead_letter_table': 'product_catalog_pim_appgen_dead_letter_event', 'emitted': ({'event_type': 'ProductClassified', 'schema': 'product_catalog_pim.product_classified.emitted.v1', 'topic': 'pbc.product_catalog_pim.events', 'outbox_table': 'product_catalog_pim_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ProductPublished', 'schema': 'product_catalog_pim.product_published.emitted.v1', 'topic': 'pbc.product_catalog_pim.events', 'outbox_table': 'product_catalog_pim_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ForecastUpdated', 'schema': 'product_catalog_pim.forecast_updated.emitted.v1', 'topic': 'pbc.product_catalog_pim.events', 'outbox_table': 'product_catalog_pim_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'TaxCalculated', 'schema': 'product_catalog_pim.tax_calculated.consumed.v1', 'topic': 'pbc.product_catalog_pim.inbox', 'inbox_table': 'product_catalog_pim_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')},), 'retry_policy': {'name': 'product_catalog_pim_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'product_catalog_pim_appgen_inbox_event'}}


class ProductCatalogPimService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
        }

    def command_products(self, payload=None):
        return self._command('command_products', payload or {})

    def query_product_read_models(self, payload=None):
        return self._command('query_product_read_models', payload or {})

    def command_prices(self, payload=None):
        return self._command('command_prices', payload or {})
