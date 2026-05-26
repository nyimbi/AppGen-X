"""Command service layer for the api_gateway_mesh PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.api_gateway_mesh.events', 'inbox_topic': 'pbc.api_gateway_mesh.inbox', 'outbox_table': 'api_gateway_mesh_appgen_outbox_event', 'inbox_table': 'api_gateway_mesh_appgen_inbox_event', 'dead_letter_table': 'api_gateway_mesh_appgen_dead_letter_event', 'emitted': ({'event_type': 'RoutePublished', 'schema': 'api_gateway_mesh.route_published.emitted.v1', 'topic': 'pbc.api_gateway_mesh.events', 'outbox_table': 'api_gateway_mesh_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ServiceHealthChanged', 'schema': 'api_gateway_mesh.service_health_changed.emitted.v1', 'topic': 'pbc.api_gateway_mesh.events', 'outbox_table': 'api_gateway_mesh_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'PbcDeployed', 'schema': 'api_gateway_mesh.pbc_deployed.consumed.v1', 'topic': 'pbc.api_gateway_mesh.inbox', 'inbox_table': 'api_gateway_mesh_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AccessPolicyChanged', 'schema': 'api_gateway_mesh.access_policy_changed.consumed.v1', 'topic': 'pbc.api_gateway_mesh.inbox', 'inbox_table': 'api_gateway_mesh_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'api_gateway_mesh_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'api_gateway_mesh_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_routes', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/api_gateway_mesh/routes', 'permission': 'api_gateway_mesh.command.1', 'owned_tables': ('api_gateway_mesh_service_route', 'api_gateway_mesh_rate_limit_policy', 'api_gateway_mesh_mtls_identity', 'api_gateway_mesh_traffic_sample'), 'read_tables': (), 'emitted_event': 'RoutePublished', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_rate_limits', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/api_gateway_mesh/rate-limits', 'permission': 'api_gateway_mesh.command.2', 'owned_tables': ('api_gateway_mesh_service_route', 'api_gateway_mesh_rate_limit_policy', 'api_gateway_mesh_mtls_identity', 'api_gateway_mesh_traffic_sample'), 'read_tables': (), 'emitted_event': 'ServiceHealthChanged', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_service_map', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/api_gateway_mesh/service-map', 'permission': 'api_gateway_mesh.query.3', 'owned_tables': (), 'read_tables': ('api_gateway_mesh_service_route', 'api_gateway_mesh_rate_limit_policy', 'api_gateway_mesh_mtls_identity', 'api_gateway_mesh_traffic_sample'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item['operation'] for item in OPERATION_CONTRACTS)
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS),
        'pbc': 'api_gateway_mesh',
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
        'pbc': 'api_gateway_mesh',
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


class ApiGatewayMeshService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        plan = operation_plan(command_name, payload)
        event_type = plan.get('emitted_event') or (EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted')
        return {
            'ok': plan['ok'],
            'pbc': 'api_gateway_mesh',
            'command': command_name,
            'payload': dict(payload),
            'operation_contract': plan,
            'transaction_boundary': plan.get('transaction_boundary'),
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_routes(self, payload=None):
        return self._command('command_routes', payload or {})

    def command_rate_limits(self, payload=None):
        return self._command('command_rate_limits', payload or {})

    def query_service_map(self, payload=None):
        return self._command('query_service_map', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = ApiGatewayMeshService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'api_gateway_mesh',
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
    service = ApiGatewayMeshService()
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
