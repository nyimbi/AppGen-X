"""Command service layer for the federated_iam PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.federated_iam.events', 'inbox_topic': 'pbc.federated_iam.inbox', 'outbox_table': 'federated_iam_appgen_outbox_event', 'inbox_table': 'federated_iam_appgen_inbox_event', 'dead_letter_table': 'federated_iam_appgen_dead_letter_event', 'emitted': ({'event_type': 'AccessPolicyChanged', 'schema': 'federated_iam.access_policy_changed.emitted.v1', 'topic': 'pbc.federated_iam.events', 'outbox_table': 'federated_iam_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PrincipalVerified', 'schema': 'federated_iam.principal_verified.emitted.v1', 'topic': 'pbc.federated_iam.events', 'outbox_table': 'federated_iam_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'RoleChanged', 'schema': 'federated_iam.role_changed.consumed.v1', 'topic': 'pbc.federated_iam.inbox', 'inbox_table': 'federated_iam_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'TenantProvisioned', 'schema': 'federated_iam.tenant_provisioned.consumed.v1', 'topic': 'pbc.federated_iam.inbox', 'inbox_table': 'federated_iam_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'federated_iam_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'federated_iam_appgen_inbox_event'}}


class FederatedIamService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'federated_iam',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_tokens(self, payload=None):
        return self._command('command_tokens', payload or {})

    def query_principals(self, payload=None):
        return self._command('query_principals', payload or {})

    def command_policy_decisions(self, payload=None):
        return self._command('command_policy_decisions', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = FederatedIamService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'federated_iam',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = FederatedIamService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
