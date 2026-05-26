"""Command service layer for the order_routing_optimization PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.order_routing_optimization.events', 'inbox_topic': 'pbc.order_routing_optimization.inbox', 'outbox_table': 'order_routing_optimization_appgen_outbox_event', 'inbox_table': 'order_routing_optimization_appgen_inbox_event', 'dead_letter_table': 'order_routing_optimization_appgen_dead_letter_event', 'emitted': ({'event_type': 'FulfillmentRouteSelected', 'schema': 'order_routing_optimization.fulfillment_route_selected.emitted.v1', 'topic': 'pbc.order_routing_optimization.events', 'outbox_table': 'order_routing_optimization_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'NodeCapacityReserved', 'schema': 'order_routing_optimization.node_capacity_reserved.emitted.v1', 'topic': 'pbc.order_routing_optimization.events', 'outbox_table': 'order_routing_optimization_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'OrderVerified', 'schema': 'order_routing_optimization.order_verified.consumed.v1', 'topic': 'pbc.order_routing_optimization.inbox', 'inbox_table': 'order_routing_optimization_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AvailabilityProjected', 'schema': 'order_routing_optimization.availability_projected.consumed.v1', 'topic': 'pbc.order_routing_optimization.inbox', 'inbox_table': 'order_routing_optimization_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'TaxCalculated', 'schema': 'order_routing_optimization.tax_calculated.consumed.v1', 'topic': 'pbc.order_routing_optimization.inbox', 'inbox_table': 'order_routing_optimization_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'order_routing_optimization_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'order_routing_optimization_appgen_inbox_event'}}


class OrderRoutingOptimizationService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'order_routing_optimization',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_route_orders(self, payload=None):
        return self._command('command_route_orders', payload or {})

    def query_route_candidates(self, payload=None):
        return self._command('query_route_candidates', payload or {})

    def command_capacity(self, payload=None):
        return self._command('command_capacity', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = OrderRoutingOptimizationService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'order_routing_optimization',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = OrderRoutingOptimizationService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
