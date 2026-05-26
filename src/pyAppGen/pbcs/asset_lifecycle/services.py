"""Command service layer for the asset_lifecycle PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.asset_lifecycle.events', 'inbox_topic': 'pbc.asset_lifecycle.inbox', 'outbox_table': 'asset_lifecycle_appgen_outbox_event', 'inbox_table': 'asset_lifecycle_appgen_inbox_event', 'dead_letter_table': 'asset_lifecycle_appgen_dead_letter_event', 'emitted': ({'event_type': 'AssetRegistered', 'schema': 'asset_lifecycle.asset_registered.emitted.v1', 'topic': 'pbc.asset_lifecycle.events', 'outbox_table': 'asset_lifecycle_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'AssetPlacedInService', 'schema': 'asset_lifecycle.asset_placed_in_service.emitted.v1', 'topic': 'pbc.asset_lifecycle.events', 'outbox_table': 'asset_lifecycle_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'DepreciationCalculated', 'schema': 'asset_lifecycle.depreciation_calculated.emitted.v1', 'topic': 'pbc.asset_lifecycle.events', 'outbox_table': 'asset_lifecycle_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'AssetTransferred', 'schema': 'asset_lifecycle.asset_transferred.emitted.v1', 'topic': 'pbc.asset_lifecycle.events', 'outbox_table': 'asset_lifecycle_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'AssetRevalued', 'schema': 'asset_lifecycle.asset_revalued.emitted.v1', 'topic': 'pbc.asset_lifecycle.events', 'outbox_table': 'asset_lifecycle_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'AssetImpaired', 'schema': 'asset_lifecycle.asset_impaired.emitted.v1', 'topic': 'pbc.asset_lifecycle.events', 'outbox_table': 'asset_lifecycle_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'MaintenanceAdjustedAssetLife', 'schema': 'asset_lifecycle.maintenance_adjusted_asset_life.emitted.v1', 'topic': 'pbc.asset_lifecycle.events', 'outbox_table': 'asset_lifecycle_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'AssetRetired', 'schema': 'asset_lifecycle.asset_retired.emitted.v1', 'topic': 'pbc.asset_lifecycle.events', 'outbox_table': 'asset_lifecycle_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'PurchaseReceiptCapitalized', 'schema': 'asset_lifecycle.purchase_receipt_capitalized.consumed.v1', 'topic': 'pbc.asset_lifecycle.inbox', 'inbox_table': 'asset_lifecycle_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'MaintenanceCompleted', 'schema': 'asset_lifecycle.maintenance_completed.consumed.v1', 'topic': 'pbc.asset_lifecycle.inbox', 'inbox_table': 'asset_lifecycle_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'InsurancePolicyChanged', 'schema': 'asset_lifecycle.insurance_policy_changed.consumed.v1', 'topic': 'pbc.asset_lifecycle.inbox', 'inbox_table': 'asset_lifecycle_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'TaxBookChanged', 'schema': 'asset_lifecycle.tax_book_changed.consumed.v1', 'topic': 'pbc.asset_lifecycle.inbox', 'inbox_table': 'asset_lifecycle_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AccessPolicyChanged', 'schema': 'asset_lifecycle.access_policy_changed.consumed.v1', 'topic': 'pbc.asset_lifecycle.inbox', 'inbox_table': 'asset_lifecycle_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'asset_lifecycle_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'asset_lifecycle_appgen_inbox_event'}}


class AssetLifecycleService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'asset_lifecycle',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_assets(self, payload=None):
        return self._command('command_assets', payload or {})

    def command_assets_asset_id_service(self, payload=None):
        return self._command('command_assets_asset_id_service', payload or {})

    def command_assets_asset_id_depreciation_schedules(self, payload=None):
        return self._command('command_assets_asset_id_depreciation_schedules', payload or {})

    def command_depreciation_runs(self, payload=None):
        return self._command('command_depreciation_runs', payload or {})

    def command_assets_asset_id_transfers(self, payload=None):
        return self._command('command_assets_asset_id_transfers', payload or {})

    def command_assets_asset_id_revaluations(self, payload=None):
        return self._command('command_assets_asset_id_revaluations', payload or {})

    def command_assets_asset_id_impairments(self, payload=None):
        return self._command('command_assets_asset_id_impairments', payload or {})

    def command_assets_asset_id_maintenance_adjustments(self, payload=None):
        return self._command('command_assets_asset_id_maintenance_adjustments', payload or {})

    def command_assets_asset_id_retirements(self, payload=None):
        return self._command('command_assets_asset_id_retirements', payload or {})

    def command_assets_events_inbox(self, payload=None):
        return self._command('command_assets_events_inbox', payload or {})

    def query_assets(self, payload=None):
        return self._command('query_assets', payload or {})

    def query_assets_asset_id_risk(self, payload=None):
        return self._command('query_assets_asset_id_risk', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = AssetLifecycleService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'asset_lifecycle',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = AssetLifecycleService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
