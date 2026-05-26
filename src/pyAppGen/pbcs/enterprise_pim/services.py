"""Command service layer for the enterprise_pim PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.enterprise_pim.events', 'inbox_topic': 'pbc.enterprise_pim.inbox', 'outbox_table': 'enterprise_pim_appgen_outbox_event', 'inbox_table': 'enterprise_pim_appgen_inbox_event', 'dead_letter_table': 'enterprise_pim_appgen_dead_letter_event', 'emitted': ({'event_type': 'TaxonomyClassified', 'schema': 'enterprise_pim.taxonomy_classified.emitted.v1', 'topic': 'pbc.enterprise_pim.events', 'outbox_table': 'enterprise_pim_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'AttributeDefined', 'schema': 'enterprise_pim.attribute_defined.emitted.v1', 'topic': 'pbc.enterprise_pim.events', 'outbox_table': 'enterprise_pim_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ContentLocalized', 'schema': 'enterprise_pim.content_localized.emitted.v1', 'topic': 'pbc.enterprise_pim.events', 'outbox_table': 'enterprise_pim_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ValidationApproved', 'schema': 'enterprise_pim.validation_approved.emitted.v1', 'topic': 'pbc.enterprise_pim.events', 'outbox_table': 'enterprise_pim_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PimMasterDataReady', 'schema': 'enterprise_pim.pim_master_data_ready.emitted.v1', 'topic': 'pbc.enterprise_pim.events', 'outbox_table': 'enterprise_pim_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'InventoryPositionUpdated', 'schema': 'enterprise_pim.inventory_position_updated.consumed.v1', 'topic': 'pbc.enterprise_pim.inbox', 'inbox_table': 'enterprise_pim_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'MediaAssetApproved', 'schema': 'enterprise_pim.media_asset_approved.consumed.v1', 'topic': 'pbc.enterprise_pim.inbox', 'inbox_table': 'enterprise_pim_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PricePromotionApproved', 'schema': 'enterprise_pim.price_promotion_approved.consumed.v1', 'topic': 'pbc.enterprise_pim.inbox', 'inbox_table': 'enterprise_pim_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'TaxCalculated', 'schema': 'enterprise_pim.tax_calculated.consumed.v1', 'topic': 'pbc.enterprise_pim.inbox', 'inbox_table': 'enterprise_pim_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'enterprise_pim_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'enterprise_pim_appgen_inbox_event'}}


class EnterprisePimService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'enterprise_pim',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_product_taxonomies(self, payload=None):
        return self._command('command_product_taxonomies', payload or {})

    def command_product_attributes(self, payload=None):
        return self._command('command_product_attributes', payload or {})

    def command_localized_content(self, payload=None):
        return self._command('command_localized_content', payload or {})

    def command_validation_workflows(self, payload=None):
        return self._command('command_validation_workflows', payload or {})

    def command_validation_workflows_id_approve(self, payload=None):
        return self._command('command_validation_workflows_id_approve', payload or {})

    def command_dependency_schemas(self, payload=None):
        return self._command('command_dependency_schemas', payload or {})

    def command_pim_events(self, payload=None):
        return self._command('command_pim_events', payload or {})

    def command_pim_publications(self, payload=None):
        return self._command('command_pim_publications', payload or {})

    def query_pim_workbench(self, payload=None):
        return self._command('query_pim_workbench', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = EnterprisePimService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'enterprise_pim',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = EnterprisePimService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
