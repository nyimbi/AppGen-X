"""Command service layer for the api_gateway_mesh PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.api_gateway_mesh.events', 'inbox_topic': 'pbc.api_gateway_mesh.inbox', 'outbox_table': 'api_gateway_mesh_appgen_outbox_event', 'inbox_table': 'api_gateway_mesh_appgen_inbox_event', 'dead_letter_table': 'api_gateway_mesh_appgen_dead_letter_event', 'emitted': ({'event_type': 'RoutePublished', 'schema': 'api_gateway_mesh.route_published.emitted.v1', 'topic': 'pbc.api_gateway_mesh.events', 'outbox_table': 'api_gateway_mesh_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ServiceHealthChanged', 'schema': 'api_gateway_mesh.service_health_changed.emitted.v1', 'topic': 'pbc.api_gateway_mesh.events', 'outbox_table': 'api_gateway_mesh_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'PbcDeployed', 'schema': 'api_gateway_mesh.pbc_deployed.consumed.v1', 'topic': 'pbc.api_gateway_mesh.inbox', 'inbox_table': 'api_gateway_mesh_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AccessPolicyChanged', 'schema': 'api_gateway_mesh.access_policy_changed.consumed.v1', 'topic': 'pbc.api_gateway_mesh.inbox', 'inbox_table': 'api_gateway_mesh_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'api_gateway_mesh_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'api_gateway_mesh_appgen_inbox_event'}}


class ApiGatewayMeshService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'api_gateway_mesh',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
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
        'ok': bool(operations),
        'pbc': 'api_gateway_mesh',
        'service_class': service.__class__.__name__,
        'operations': operations,
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
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
