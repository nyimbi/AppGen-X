"""Command service layer for the gl_core PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.gl_core.events', 'inbox_topic': 'pbc.gl_core.inbox', 'outbox_table': 'gl_core_appgen_outbox_event', 'inbox_table': 'gl_core_appgen_inbox_event', 'dead_letter_table': 'gl_core_appgen_dead_letter_event', 'emitted': ({'event_type': 'JournalPosted', 'schema': 'gl_core.journal_posted.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PeriodClosed', 'schema': 'gl_core.period_closed.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'TrialBalanceCalculated', 'schema': 'gl_core.trial_balance_calculated.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'LedgerEventAppended', 'schema': 'gl_core.ledger_event_appended.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ConsensusCommitted', 'schema': 'gl_core.consensus_committed.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'LedgerProjectionRebuilt', 'schema': 'gl_core.ledger_projection_rebuilt.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ContinuousCloseSnapshotCreated', 'schema': 'gl_core.continuous_close_snapshot_created.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ReconciliationSuggested', 'schema': 'gl_core.reconciliation_suggested.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'AuditProofGenerated', 'schema': 'gl_core.audit_proof_generated.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'RegulatoryRuleCompiled', 'schema': 'gl_core.regulatory_rule_compiled.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PostingValidationPredicted', 'schema': 'gl_core.posting_validation_predicted.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'InvoiceApproved', 'schema': 'gl_core.invoice_approved.consumed.v1', 'topic': 'pbc.gl_core.inbox', 'inbox_table': 'gl_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PaymentCaptured', 'schema': 'gl_core.payment_captured.consumed.v1', 'topic': 'pbc.gl_core.inbox', 'inbox_table': 'gl_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'DepreciationCalculated', 'schema': 'gl_core.depreciation_calculated.consumed.v1', 'topic': 'pbc.gl_core.inbox', 'inbox_table': 'gl_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'OrderShipped', 'schema': 'gl_core.order_shipped.consumed.v1', 'topic': 'pbc.gl_core.inbox', 'inbox_table': 'gl_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'gl_core_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'gl_core_appgen_inbox_event'}}


class GlCoreService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'gl_core',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_journals(self, payload=None):
        return self._command('command_journals', payload or {})

    def query_trial_balance(self, payload=None):
        return self._command('query_trial_balance', payload or {})

    def query_chart_of_accounts(self, payload=None):
        return self._command('query_chart_of_accounts', payload or {})

    def query_ledger_events(self, payload=None):
        return self._command('query_ledger_events', payload or {})

    def command_ledger_projections(self, payload=None):
        return self._command('command_ledger_projections', payload or {})

    def command_consensus_commits(self, payload=None):
        return self._command('command_consensus_commits', payload or {})

    def command_schema_extensions(self, payload=None):
        return self._command('command_schema_extensions', payload or {})

    def query_temporal_ledger(self, payload=None):
        return self._command('query_temporal_ledger', payload or {})

    def command_probabilistic_postings(self, payload=None):
        return self._command('command_probabilistic_postings', payload or {})

    def command_continuous_close_snapshots(self, payload=None):
        return self._command('command_continuous_close_snapshots', payload or {})

    def command_causal_scenarios(self, payload=None):
        return self._command('command_causal_scenarios', payload or {})

    def command_reconciliation_cases(self, payload=None):
        return self._command('command_reconciliation_cases', payload or {})

    def command_semantic_documents(self, payload=None):
        return self._command('command_semantic_documents', payload or {})

    def command_regulatory_rules(self, payload=None):
        return self._command('command_regulatory_rules', payload or {})

    def command_predictive_validations(self, payload=None):
        return self._command('command_predictive_validations', payload or {})

    def command_audit_proofs(self, payload=None):
        return self._command('command_audit_proofs', payload or {})

    def command_control_tests(self, payload=None):
        return self._command('command_control_tests', payload or {})

    def command_ledger_federation_links(self, payload=None):
        return self._command('command_ledger_federation_links', payload or {})

    def command_resilience_drills(self, payload=None):
        return self._command('command_resilience_drills', payload or {})

    def command_carbon_execution_windows(self, payload=None):
        return self._command('command_carbon_execution_windows', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = GlCoreService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'gl_core',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = GlCoreService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
