"""Command service layer for the global_inventory_visibility PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.global_inventory_visibility.events', 'inbox_topic': 'pbc.global_inventory_visibility.inbox', 'outbox_table': 'global_inventory_visibility_appgen_outbox_event', 'inbox_table': 'global_inventory_visibility_appgen_inbox_event', 'dead_letter_table': 'global_inventory_visibility_appgen_dead_letter_event', 'emitted': ({'event_type': 'AvailabilityProjected', 'schema': 'global_inventory_visibility.availability_projected.emitted.v1', 'topic': 'pbc.global_inventory_visibility.events', 'outbox_table': 'global_inventory_visibility_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'InventoryPoolChanged', 'schema': 'global_inventory_visibility.inventory_pool_changed.emitted.v1', 'topic': 'pbc.global_inventory_visibility.events', 'outbox_table': 'global_inventory_visibility_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'GoodsReceiptPosted', 'schema': 'global_inventory_visibility.goods_receipt_posted.consumed.v1', 'topic': 'pbc.global_inventory_visibility.inbox', 'inbox_table': 'global_inventory_visibility_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'ShipmentDelivered', 'schema': 'global_inventory_visibility.shipment_delivered.consumed.v1', 'topic': 'pbc.global_inventory_visibility.inbox', 'inbox_table': 'global_inventory_visibility_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'InventoryAllocated', 'schema': 'global_inventory_visibility.inventory_allocated.consumed.v1', 'topic': 'pbc.global_inventory_visibility.inbox', 'inbox_table': 'global_inventory_visibility_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'global_inventory_visibility_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'global_inventory_visibility_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'query_global_availability', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/global_inventory_visibility/global-availability', 'permission': 'global_inventory_visibility.query.1', 'owned_tables': (), 'read_tables': ('global_inventory_visibility_inventory_pool', 'global_inventory_visibility_inventory_projection', 'global_inventory_visibility_supply_node', 'global_inventory_visibility_availability_snapshot'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_pool_rules', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/global_inventory_visibility/pool-rules', 'permission': 'global_inventory_visibility.command.2', 'owned_tables': ('global_inventory_visibility_inventory_pool', 'global_inventory_visibility_inventory_projection', 'global_inventory_visibility_supply_node', 'global_inventory_visibility_availability_snapshot'), 'read_tables': (), 'emitted_event': 'InventoryPoolChanged', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_supply_nodes', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/global_inventory_visibility/supply-nodes', 'permission': 'global_inventory_visibility.query.3', 'owned_tables': (), 'read_tables': ('global_inventory_visibility_inventory_pool', 'global_inventory_visibility_inventory_projection', 'global_inventory_visibility_supply_node', 'global_inventory_visibility_availability_snapshot'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item['operation'] for item in OPERATION_CONTRACTS)
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS),
        'pbc': 'global_inventory_visibility',
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
        'pbc': 'global_inventory_visibility',
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


class GlobalInventoryVisibilityService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        plan = operation_plan(command_name, payload)
        event_type = plan.get('emitted_event') or (EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted')
        return {
            'ok': plan['ok'],
            'pbc': 'global_inventory_visibility',
            'command': command_name,
            'payload': dict(payload),
            'operation_contract': plan,
            'transaction_boundary': plan.get('transaction_boundary'),
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def query_global_availability(self, payload=None):
        return self._command('query_global_availability', payload or {})

    def command_pool_rules(self, payload=None):
        return self._command('command_pool_rules', payload or {})

    def query_supply_nodes(self, payload=None):
        return self._command('query_supply_nodes', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = GlobalInventoryVisibilityService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'global_inventory_visibility',
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
    service = GlobalInventoryVisibilityService()
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
