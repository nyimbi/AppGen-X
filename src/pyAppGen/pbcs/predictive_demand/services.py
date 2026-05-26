"""Command service layer for the predictive_demand PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.predictive_demand.events', 'inbox_topic': 'pbc.predictive_demand.inbox', 'outbox_table': 'predictive_demand_appgen_outbox_event', 'inbox_table': 'predictive_demand_appgen_inbox_event', 'dead_letter_table': 'predictive_demand_appgen_dead_letter_event', 'emitted': ({'event_type': 'ForecastUpdated', 'schema': 'predictive_demand.forecast_updated.emitted.v1', 'topic': 'pbc.predictive_demand.events', 'outbox_table': 'predictive_demand_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'MaterialShortageDetected', 'schema': 'predictive_demand.material_shortage_detected.emitted.v1', 'topic': 'pbc.predictive_demand.events', 'outbox_table': 'predictive_demand_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'OperationalKpiChanged', 'schema': 'predictive_demand.operational_kpi_changed.consumed.v1', 'topic': 'pbc.predictive_demand.inbox', 'inbox_table': 'predictive_demand_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'OrderShipped', 'schema': 'predictive_demand.order_shipped.consumed.v1', 'topic': 'pbc.predictive_demand.inbox', 'inbox_table': 'predictive_demand_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'InventoryPoolChanged', 'schema': 'predictive_demand.inventory_pool_changed.consumed.v1', 'topic': 'pbc.predictive_demand.inbox', 'inbox_table': 'predictive_demand_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'predictive_demand_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'predictive_demand_appgen_inbox_event'}}


class PredictiveDemandService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'predictive_demand',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_forecast_runs(self, payload=None):
        return self._command('command_forecast_runs', payload or {})

    def query_forecast_results(self, payload=None):
        return self._command('query_forecast_results', payload or {})

    def command_signals(self, payload=None):
        return self._command('command_signals', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = PredictiveDemandService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'predictive_demand',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = PredictiveDemandService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
