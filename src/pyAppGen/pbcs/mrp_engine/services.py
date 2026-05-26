"""Command service layer for the mrp_engine PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.mrp_engine.events', 'inbox_topic': 'pbc.mrp_engine.inbox', 'outbox_table': 'mrp_engine_appgen_outbox_event', 'inbox_table': 'mrp_engine_appgen_inbox_event', 'dead_letter_table': 'mrp_engine_appgen_dead_letter_event', 'emitted': ({'event_type': 'BomRegistered', 'schema': 'mrp_engine.bom_registered.emitted.v1', 'topic': 'pbc.mrp_engine.events', 'outbox_table': 'mrp_engine_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'DemandProjectionIngested', 'schema': 'mrp_engine.demand_projection_ingested.emitted.v1', 'topic': 'pbc.mrp_engine.events', 'outbox_table': 'mrp_engine_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'InventoryProjectionIngested', 'schema': 'mrp_engine.inventory_projection_ingested.emitted.v1', 'topic': 'pbc.mrp_engine.events', 'outbox_table': 'mrp_engine_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'MrpRunStarted', 'schema': 'mrp_engine.mrp_run_started.emitted.v1', 'topic': 'pbc.mrp_engine.events', 'outbox_table': 'mrp_engine_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'MaterialShortageDetected', 'schema': 'mrp_engine.material_shortage_detected.emitted.v1', 'topic': 'pbc.mrp_engine.events', 'outbox_table': 'mrp_engine_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PlannedOrderReleased', 'schema': 'mrp_engine.planned_order_released.emitted.v1', 'topic': 'pbc.mrp_engine.events', 'outbox_table': 'mrp_engine_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'InventoryReleased', 'schema': 'mrp_engine.inventory_released.consumed.v1', 'topic': 'pbc.mrp_engine.inbox', 'inbox_table': 'mrp_engine_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'OrderVerified', 'schema': 'mrp_engine.order_verified.consumed.v1', 'topic': 'pbc.mrp_engine.inbox', 'inbox_table': 'mrp_engine_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'ForecastUpdated', 'schema': 'mrp_engine.forecast_updated.consumed.v1', 'topic': 'pbc.mrp_engine.inbox', 'inbox_table': 'mrp_engine_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'ProductionCapacityChanged', 'schema': 'mrp_engine.production_capacity_changed.consumed.v1', 'topic': 'pbc.mrp_engine.inbox', 'inbox_table': 'mrp_engine_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'QualityHoldReleased', 'schema': 'mrp_engine.quality_hold_released.consumed.v1', 'topic': 'pbc.mrp_engine.inbox', 'inbox_table': 'mrp_engine_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'SupplierLeadTimeUpdated', 'schema': 'mrp_engine.supplier_lead_time_updated.consumed.v1', 'topic': 'pbc.mrp_engine.inbox', 'inbox_table': 'mrp_engine_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'mrp_engine_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'mrp_engine_appgen_inbox_event'}}


class MrpEngineService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'mrp_engine',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_mrp_boms(self, payload=None):
        return self._command('command_mrp_boms', payload or {})

    def command_mrp_demand_projections(self, payload=None):
        return self._command('command_mrp_demand_projections', payload or {})

    def command_mrp_inventory_projections(self, payload=None):
        return self._command('command_mrp_inventory_projections', payload or {})

    def command_mrp_runs(self, payload=None):
        return self._command('command_mrp_runs', payload or {})

    def command_mrp_runs_id_calculate(self, payload=None):
        return self._command('command_mrp_runs_id_calculate', payload or {})

    def command_mrp_planned_orders_id_release(self, payload=None):
        return self._command('command_mrp_planned_orders_id_release', payload or {})

    def command_mrp_events_inbox(self, payload=None):
        return self._command('command_mrp_events_inbox', payload or {})

    def query_mrp_workbench(self, payload=None):
        return self._command('query_mrp_workbench', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = MrpEngineService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'mrp_engine',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = MrpEngineService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
