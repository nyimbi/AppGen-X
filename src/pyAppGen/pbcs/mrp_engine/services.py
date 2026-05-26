"""Command service layer for the mrp_engine PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.mrp_engine.events', 'inbox_topic': 'pbc.mrp_engine.inbox', 'outbox_table': 'mrp_engine_appgen_outbox_event', 'inbox_table': 'mrp_engine_appgen_inbox_event', 'dead_letter_table': 'mrp_engine_appgen_dead_letter_event', 'emitted': ({'event_type': 'BomRegistered', 'schema': 'mrp_engine.bom_registered.emitted.v1', 'topic': 'pbc.mrp_engine.events', 'outbox_table': 'mrp_engine_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'DemandProjectionIngested', 'schema': 'mrp_engine.demand_projection_ingested.emitted.v1', 'topic': 'pbc.mrp_engine.events', 'outbox_table': 'mrp_engine_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'InventoryProjectionIngested', 'schema': 'mrp_engine.inventory_projection_ingested.emitted.v1', 'topic': 'pbc.mrp_engine.events', 'outbox_table': 'mrp_engine_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'MrpRunStarted', 'schema': 'mrp_engine.mrp_run_started.emitted.v1', 'topic': 'pbc.mrp_engine.events', 'outbox_table': 'mrp_engine_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'MaterialShortageDetected', 'schema': 'mrp_engine.material_shortage_detected.emitted.v1', 'topic': 'pbc.mrp_engine.events', 'outbox_table': 'mrp_engine_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PlannedOrderReleased', 'schema': 'mrp_engine.planned_order_released.emitted.v1', 'topic': 'pbc.mrp_engine.events', 'outbox_table': 'mrp_engine_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'InventoryReleased', 'schema': 'mrp_engine.inventory_released.consumed.v1', 'topic': 'pbc.mrp_engine.inbox', 'inbox_table': 'mrp_engine_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'OrderVerified', 'schema': 'mrp_engine.order_verified.consumed.v1', 'topic': 'pbc.mrp_engine.inbox', 'inbox_table': 'mrp_engine_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'ForecastUpdated', 'schema': 'mrp_engine.forecast_updated.consumed.v1', 'topic': 'pbc.mrp_engine.inbox', 'inbox_table': 'mrp_engine_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'ProductionCapacityChanged', 'schema': 'mrp_engine.production_capacity_changed.consumed.v1', 'topic': 'pbc.mrp_engine.inbox', 'inbox_table': 'mrp_engine_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'QualityHoldReleased', 'schema': 'mrp_engine.quality_hold_released.consumed.v1', 'topic': 'pbc.mrp_engine.inbox', 'inbox_table': 'mrp_engine_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'SupplierLeadTimeUpdated', 'schema': 'mrp_engine.supplier_lead_time_updated.consumed.v1', 'topic': 'pbc.mrp_engine.inbox', 'inbox_table': 'mrp_engine_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'mrp_engine_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'mrp_engine_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_mrp_boms', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/boms', 'permission': 'mrp_engine.command.1', 'owned_tables': ('mrp_engine_bill_of_material', 'mrp_engine_bom_revision', 'mrp_engine_bom_component', 'mrp_engine_item_planning_profile', 'mrp_engine_material_demand', 'mrp_engine_inventory_projection', 'mrp_engine_capacity_projection', 'mrp_engine_mrp_run', 'mrp_engine_mrp_run_item', 'mrp_engine_planned_order', 'mrp_engine_planned_purchase_suggestion', 'mrp_engine_planned_production_order', 'mrp_engine_material_shortage', 'mrp_engine_shortage_pegging', 'mrp_engine_planning_exception', 'mrp_engine_mrp_rule', 'mrp_engine_mrp_parameter', 'mrp_engine_mrp_configuration'), 'read_tables': (), 'emitted_event': 'BomRegistered', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_mrp_demand_projections', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/demand-projections', 'permission': 'mrp_engine.command.2', 'owned_tables': ('mrp_engine_bill_of_material', 'mrp_engine_bom_revision', 'mrp_engine_bom_component', 'mrp_engine_item_planning_profile', 'mrp_engine_material_demand', 'mrp_engine_inventory_projection', 'mrp_engine_capacity_projection', 'mrp_engine_mrp_run', 'mrp_engine_mrp_run_item', 'mrp_engine_planned_order', 'mrp_engine_planned_purchase_suggestion', 'mrp_engine_planned_production_order', 'mrp_engine_material_shortage', 'mrp_engine_shortage_pegging', 'mrp_engine_planning_exception', 'mrp_engine_mrp_rule', 'mrp_engine_mrp_parameter', 'mrp_engine_mrp_configuration'), 'read_tables': (), 'emitted_event': 'DemandProjectionIngested', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_mrp_inventory_projections', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/inventory-projections', 'permission': 'mrp_engine.command.3', 'owned_tables': ('mrp_engine_bill_of_material', 'mrp_engine_bom_revision', 'mrp_engine_bom_component', 'mrp_engine_item_planning_profile', 'mrp_engine_material_demand', 'mrp_engine_inventory_projection', 'mrp_engine_capacity_projection', 'mrp_engine_mrp_run', 'mrp_engine_mrp_run_item', 'mrp_engine_planned_order', 'mrp_engine_planned_purchase_suggestion', 'mrp_engine_planned_production_order', 'mrp_engine_material_shortage', 'mrp_engine_shortage_pegging', 'mrp_engine_planning_exception', 'mrp_engine_mrp_rule', 'mrp_engine_mrp_parameter', 'mrp_engine_mrp_configuration'), 'read_tables': (), 'emitted_event': 'InventoryProjectionIngested', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_mrp_runs', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/runs', 'permission': 'mrp_engine.command.4', 'owned_tables': ('mrp_engine_bill_of_material', 'mrp_engine_bom_revision', 'mrp_engine_bom_component', 'mrp_engine_item_planning_profile', 'mrp_engine_material_demand', 'mrp_engine_inventory_projection', 'mrp_engine_capacity_projection', 'mrp_engine_mrp_run', 'mrp_engine_mrp_run_item', 'mrp_engine_planned_order', 'mrp_engine_planned_purchase_suggestion', 'mrp_engine_planned_production_order', 'mrp_engine_material_shortage', 'mrp_engine_shortage_pegging', 'mrp_engine_planning_exception', 'mrp_engine_mrp_rule', 'mrp_engine_mrp_parameter', 'mrp_engine_mrp_configuration'), 'read_tables': (), 'emitted_event': 'MrpRunStarted', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_mrp_runs_id_calculate', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/runs/{id}/calculate', 'permission': 'mrp_engine.command.5', 'owned_tables': ('mrp_engine_bill_of_material', 'mrp_engine_bom_revision', 'mrp_engine_bom_component', 'mrp_engine_item_planning_profile', 'mrp_engine_material_demand', 'mrp_engine_inventory_projection', 'mrp_engine_capacity_projection', 'mrp_engine_mrp_run', 'mrp_engine_mrp_run_item', 'mrp_engine_planned_order', 'mrp_engine_planned_purchase_suggestion', 'mrp_engine_planned_production_order', 'mrp_engine_material_shortage', 'mrp_engine_shortage_pegging', 'mrp_engine_planning_exception', 'mrp_engine_mrp_rule', 'mrp_engine_mrp_parameter', 'mrp_engine_mrp_configuration'), 'read_tables': (), 'emitted_event': 'MaterialShortageDetected', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_mrp_planned_orders_id_release', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/planned-orders/{id}/release', 'permission': 'mrp_engine.command.6', 'owned_tables': ('mrp_engine_bill_of_material', 'mrp_engine_bom_revision', 'mrp_engine_bom_component', 'mrp_engine_item_planning_profile', 'mrp_engine_material_demand', 'mrp_engine_inventory_projection', 'mrp_engine_capacity_projection', 'mrp_engine_mrp_run', 'mrp_engine_mrp_run_item', 'mrp_engine_planned_order', 'mrp_engine_planned_purchase_suggestion', 'mrp_engine_planned_production_order', 'mrp_engine_material_shortage', 'mrp_engine_shortage_pegging', 'mrp_engine_planning_exception', 'mrp_engine_mrp_rule', 'mrp_engine_mrp_parameter', 'mrp_engine_mrp_configuration'), 'read_tables': (), 'emitted_event': 'PlannedOrderReleased', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_mrp_events_inbox', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/events/inbox', 'permission': 'mrp_engine.command.7', 'owned_tables': ('mrp_engine_bill_of_material', 'mrp_engine_bom_revision', 'mrp_engine_bom_component', 'mrp_engine_item_planning_profile', 'mrp_engine_material_demand', 'mrp_engine_inventory_projection', 'mrp_engine_capacity_projection', 'mrp_engine_mrp_run', 'mrp_engine_mrp_run_item', 'mrp_engine_planned_order', 'mrp_engine_planned_purchase_suggestion', 'mrp_engine_planned_production_order', 'mrp_engine_material_shortage', 'mrp_engine_shortage_pegging', 'mrp_engine_planning_exception', 'mrp_engine_mrp_rule', 'mrp_engine_mrp_parameter', 'mrp_engine_mrp_configuration'), 'read_tables': (), 'emitted_event': 'BomRegistered', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_mrp_workbench', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/mrp_engine/mrp/workbench', 'permission': 'mrp_engine.query.8', 'owned_tables': (), 'read_tables': ('mrp_engine_bill_of_material', 'mrp_engine_bom_revision', 'mrp_engine_bom_component', 'mrp_engine_item_planning_profile', 'mrp_engine_material_demand', 'mrp_engine_inventory_projection', 'mrp_engine_capacity_projection', 'mrp_engine_mrp_run', 'mrp_engine_mrp_run_item', 'mrp_engine_planned_order', 'mrp_engine_planned_purchase_suggestion', 'mrp_engine_planned_production_order', 'mrp_engine_material_shortage', 'mrp_engine_shortage_pegging', 'mrp_engine_planning_exception', 'mrp_engine_mrp_rule', 'mrp_engine_mrp_parameter', 'mrp_engine_mrp_configuration'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


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
        'pbc': 'mrp_engine',
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
        'pbc': 'mrp_engine',
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


class MrpEngineService:
    """Side-effect-free generated command facade."""

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get('operation_kind')
        result = {
            'ok': plan['ok'],
            'pbc': 'mrp_engine',
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
        return self._query('query_mrp_workbench', payload or {})


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
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'mrp_engine',
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
    service = MrpEngineService()
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
