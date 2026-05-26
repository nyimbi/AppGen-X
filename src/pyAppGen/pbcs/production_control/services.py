"""Command service layer for the production_control PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.production_control.events', 'inbox_topic': 'pbc.production_control.inbox', 'outbox_table': 'production_control_appgen_outbox_event', 'inbox_table': 'production_control_appgen_inbox_event', 'dead_letter_table': 'production_control_appgen_dead_letter_event', 'emitted': ({'event_type': 'ProductionCompleted', 'schema': 'production_control.production_completed.emitted.v1', 'topic': 'pbc.production_control.events', 'outbox_table': 'production_control_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'AssetPlacedInService', 'schema': 'production_control.asset_placed_in_service.emitted.v1', 'topic': 'pbc.production_control.events', 'outbox_table': 'production_control_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'DowntimeCaptured', 'schema': 'production_control.downtime_captured.emitted.v1', 'topic': 'pbc.production_control.events', 'outbox_table': 'production_control_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'PlannedOrderReleased', 'schema': 'production_control.planned_order_released.consumed.v1', 'topic': 'pbc.production_control.inbox', 'inbox_table': 'production_control_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'MaintenanceCompleted', 'schema': 'production_control.maintenance_completed.consumed.v1', 'topic': 'pbc.production_control.inbox', 'inbox_table': 'production_control_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'production_control_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'production_control_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_production_orders', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/production_control/production-orders', 'permission': 'production_control.command.1', 'owned_tables': ('production_control_work_center', 'production_control_production_order', 'production_control_routing_step', 'production_control_downtime_event'), 'read_tables': (), 'emitted_event': 'ProductionCompleted', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_downtime', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/production_control/downtime', 'permission': 'production_control.command.2', 'owned_tables': ('production_control_work_center', 'production_control_production_order', 'production_control_routing_step', 'production_control_downtime_event'), 'read_tables': (), 'emitted_event': 'AssetPlacedInService', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_schedule', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/production_control/schedule', 'permission': 'production_control.query.3', 'owned_tables': (), 'read_tables': ('production_control_work_center', 'production_control_production_order', 'production_control_routing_step', 'production_control_downtime_event'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item['operation'] for item in OPERATION_CONTRACTS)
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS),
        'pbc': 'production_control',
        'operations': operations,
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
        'pbc': 'production_control',
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


class ProductionControlService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        plan = operation_plan(command_name, payload)
        event_type = plan.get('emitted_event') or (EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted')
        return {
            'ok': plan['ok'],
            'pbc': 'production_control',
            'command': command_name,
            'payload': dict(payload),
            'operation_contract': plan,
            'transaction_boundary': plan.get('transaction_boundary'),
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_production_orders(self, payload=None):
        return self._command('command_production_orders', payload or {})

    def command_downtime(self, payload=None):
        return self._command('command_downtime', payload or {})

    def query_schedule(self, payload=None):
        return self._command('query_schedule', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = ProductionControlService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'production_control',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'operation_contracts': service_operation_contracts()['contracts'],
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = ProductionControlService()
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
