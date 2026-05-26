"""Command service layer for the federated_iam PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.federated_iam.events', 'inbox_topic': 'pbc.federated_iam.inbox', 'outbox_table': 'federated_iam_appgen_outbox_event', 'inbox_table': 'federated_iam_appgen_inbox_event', 'dead_letter_table': 'federated_iam_appgen_dead_letter_event', 'emitted': ({'event_type': 'AccessPolicyChanged', 'schema': 'federated_iam.access_policy_changed.emitted.v1', 'topic': 'pbc.federated_iam.events', 'outbox_table': 'federated_iam_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PrincipalVerified', 'schema': 'federated_iam.principal_verified.emitted.v1', 'topic': 'pbc.federated_iam.events', 'outbox_table': 'federated_iam_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'RoleChanged', 'schema': 'federated_iam.role_changed.consumed.v1', 'topic': 'pbc.federated_iam.inbox', 'inbox_table': 'federated_iam_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'TenantProvisioned', 'schema': 'federated_iam.tenant_provisioned.consumed.v1', 'topic': 'pbc.federated_iam.inbox', 'inbox_table': 'federated_iam_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'federated_iam_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'federated_iam_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_tokens', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/federated_iam/tokens', 'permission': 'federated_iam.command.1', 'owned_tables': ('federated_iam_tenant', 'federated_iam_principal', 'federated_iam_access_policy', 'federated_iam_token_grant'), 'read_tables': (), 'emitted_event': 'AccessPolicyChanged', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_principals', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/federated_iam/principals', 'permission': 'federated_iam.query.2', 'owned_tables': (), 'read_tables': ('federated_iam_tenant', 'federated_iam_principal', 'federated_iam_access_policy', 'federated_iam_token_grant'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_policy_decisions', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/federated_iam/policy-decisions', 'permission': 'federated_iam.command.3', 'owned_tables': ('federated_iam_tenant', 'federated_iam_principal', 'federated_iam_access_policy', 'federated_iam_token_grant'), 'read_tables': (), 'emitted_event': 'AccessPolicyChanged', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item['operation'] for item in OPERATION_CONTRACTS)
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS),
        'pbc': 'federated_iam',
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
        'pbc': 'federated_iam',
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


class FederatedIamService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        plan = operation_plan(command_name, payload)
        event_type = plan.get('emitted_event') or (EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted')
        return {
            'ok': plan['ok'],
            'pbc': 'federated_iam',
            'command': command_name,
            'payload': dict(payload),
            'operation_contract': plan,
            'transaction_boundary': plan.get('transaction_boundary'),
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
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'federated_iam',
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
    service = FederatedIamService()
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
