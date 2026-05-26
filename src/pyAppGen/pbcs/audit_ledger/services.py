"""Command service layer for the audit_ledger PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.audit_ledger.events', 'inbox_topic': 'pbc.audit_ledger.inbox', 'outbox_table': 'audit_ledger_appgen_outbox_event', 'inbox_table': 'audit_ledger_appgen_inbox_event', 'dead_letter_table': 'audit_ledger_appgen_dead_letter_event', 'emitted': ({'event_type': 'AuditEventSealed', 'schema': 'audit_ledger.audit_event_sealed.emitted.v1', 'topic': 'pbc.audit_ledger.events', 'outbox_table': 'audit_ledger_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ForensicExportPrepared', 'schema': 'audit_ledger.forensic_export_prepared.emitted.v1', 'topic': 'pbc.audit_ledger.events', 'outbox_table': 'audit_ledger_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'AccessPolicyChanged', 'schema': 'audit_ledger.access_policy_changed.consumed.v1', 'topic': 'pbc.audit_ledger.inbox', 'inbox_table': 'audit_ledger_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'WorkflowCompleted', 'schema': 'audit_ledger.workflow_completed.consumed.v1', 'topic': 'pbc.audit_ledger.inbox', 'inbox_table': 'audit_ledger_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'RoutePublished', 'schema': 'audit_ledger.route_published.consumed.v1', 'topic': 'pbc.audit_ledger.inbox', 'inbox_table': 'audit_ledger_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'audit_ledger_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'audit_ledger_appgen_inbox_event'}}


class AuditLedgerService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'audit_ledger',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_audit_events(self, payload=None):
        return self._command('command_audit_events', payload or {})

    def query_signature_chain(self, payload=None):
        return self._command('query_signature_chain', payload or {})

    def command_exports(self, payload=None):
        return self._command('command_exports', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = AuditLedgerService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'audit_ledger',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = AuditLedgerService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
