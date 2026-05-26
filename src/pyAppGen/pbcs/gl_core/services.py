"""Command service layer for the gl_core PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.gl_core.events', 'inbox_topic': 'pbc.gl_core.inbox', 'outbox_table': 'gl_core_appgen_outbox_event', 'inbox_table': 'gl_core_appgen_inbox_event', 'dead_letter_table': 'gl_core_appgen_dead_letter_event', 'emitted': ({'event_type': 'JournalPosted', 'schema': 'gl_core.journal_posted.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PeriodClosed', 'schema': 'gl_core.period_closed.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'TrialBalanceCalculated', 'schema': 'gl_core.trial_balance_calculated.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'LedgerEventAppended', 'schema': 'gl_core.ledger_event_appended.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ConsensusCommitted', 'schema': 'gl_core.consensus_committed.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'LedgerProjectionRebuilt', 'schema': 'gl_core.ledger_projection_rebuilt.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ContinuousCloseSnapshotCreated', 'schema': 'gl_core.continuous_close_snapshot_created.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ReconciliationSuggested', 'schema': 'gl_core.reconciliation_suggested.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'AuditProofGenerated', 'schema': 'gl_core.audit_proof_generated.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'RegulatoryRuleCompiled', 'schema': 'gl_core.regulatory_rule_compiled.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PostingValidationPredicted', 'schema': 'gl_core.posting_validation_predicted.emitted.v1', 'topic': 'pbc.gl_core.events', 'outbox_table': 'gl_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'InvoiceApproved', 'schema': 'gl_core.invoice_approved.consumed.v1', 'topic': 'pbc.gl_core.inbox', 'inbox_table': 'gl_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PaymentCaptured', 'schema': 'gl_core.payment_captured.consumed.v1', 'topic': 'pbc.gl_core.inbox', 'inbox_table': 'gl_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'DepreciationCalculated', 'schema': 'gl_core.depreciation_calculated.consumed.v1', 'topic': 'pbc.gl_core.inbox', 'inbox_table': 'gl_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'OrderShipped', 'schema': 'gl_core.order_shipped.consumed.v1', 'topic': 'pbc.gl_core.inbox', 'inbox_table': 'gl_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'gl_core_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'gl_core_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_journals', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/gl_core/journals', 'permission': 'gl_core.command.1', 'owned_tables': ('gl_core_ledger_event_log', 'gl_core_journal_entry', 'gl_core_journal_line', 'gl_core_ledger_account', 'gl_core_accounting_period', 'gl_core_ledger_projection', 'gl_core_consensus_replica', 'gl_core_schema_extension', 'gl_core_tenant_ledger_partition', 'gl_core_probabilistic_posting', 'gl_core_close_snapshot', 'gl_core_causal_scenario', 'gl_core_reconciliation_case', 'gl_core_semantic_source_document', 'gl_core_regulatory_rule_version', 'gl_core_predictive_validation_run', 'gl_core_audit_proof', 'gl_core_policy_decision', 'gl_core_control_assertion', 'gl_core_ledger_federation_link', 'gl_core_identity_credential', 'gl_core_resilience_drill', 'gl_core_crypto_key_epoch', 'gl_core_carbon_execution_window'), 'read_tables': (), 'emitted_event': 'JournalPosted', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_trial_balance', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/gl_core/trial-balance', 'permission': 'gl_core.query.2', 'owned_tables': (), 'read_tables': ('gl_core_ledger_event_log', 'gl_core_journal_entry', 'gl_core_journal_line', 'gl_core_ledger_account', 'gl_core_accounting_period', 'gl_core_ledger_projection', 'gl_core_consensus_replica', 'gl_core_schema_extension', 'gl_core_tenant_ledger_partition', 'gl_core_probabilistic_posting', 'gl_core_close_snapshot', 'gl_core_causal_scenario', 'gl_core_reconciliation_case', 'gl_core_semantic_source_document', 'gl_core_regulatory_rule_version', 'gl_core_predictive_validation_run', 'gl_core_audit_proof', 'gl_core_policy_decision', 'gl_core_control_assertion', 'gl_core_ledger_federation_link', 'gl_core_identity_credential', 'gl_core_resilience_drill', 'gl_core_crypto_key_epoch', 'gl_core_carbon_execution_window'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_chart_of_accounts', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/gl_core/chart-of-accounts', 'permission': 'gl_core.query.3', 'owned_tables': (), 'read_tables': ('gl_core_ledger_event_log', 'gl_core_journal_entry', 'gl_core_journal_line', 'gl_core_ledger_account', 'gl_core_accounting_period', 'gl_core_ledger_projection', 'gl_core_consensus_replica', 'gl_core_schema_extension', 'gl_core_tenant_ledger_partition', 'gl_core_probabilistic_posting', 'gl_core_close_snapshot', 'gl_core_causal_scenario', 'gl_core_reconciliation_case', 'gl_core_semantic_source_document', 'gl_core_regulatory_rule_version', 'gl_core_predictive_validation_run', 'gl_core_audit_proof', 'gl_core_policy_decision', 'gl_core_control_assertion', 'gl_core_ledger_federation_link', 'gl_core_identity_credential', 'gl_core_resilience_drill', 'gl_core_crypto_key_epoch', 'gl_core_carbon_execution_window'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_ledger_events', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/gl_core/ledger-events', 'permission': 'gl_core.query.4', 'owned_tables': (), 'read_tables': ('gl_core_ledger_event_log', 'gl_core_journal_entry', 'gl_core_journal_line', 'gl_core_ledger_account', 'gl_core_accounting_period', 'gl_core_ledger_projection', 'gl_core_consensus_replica', 'gl_core_schema_extension', 'gl_core_tenant_ledger_partition', 'gl_core_probabilistic_posting', 'gl_core_close_snapshot', 'gl_core_causal_scenario', 'gl_core_reconciliation_case', 'gl_core_semantic_source_document', 'gl_core_regulatory_rule_version', 'gl_core_predictive_validation_run', 'gl_core_audit_proof', 'gl_core_policy_decision', 'gl_core_control_assertion', 'gl_core_ledger_federation_link', 'gl_core_identity_credential', 'gl_core_resilience_drill', 'gl_core_crypto_key_epoch', 'gl_core_carbon_execution_window'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ledger_projections', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/gl_core/ledger-projections', 'permission': 'gl_core.command.5', 'owned_tables': ('gl_core_ledger_event_log', 'gl_core_journal_entry', 'gl_core_journal_line', 'gl_core_ledger_account', 'gl_core_accounting_period', 'gl_core_ledger_projection', 'gl_core_consensus_replica', 'gl_core_schema_extension', 'gl_core_tenant_ledger_partition', 'gl_core_probabilistic_posting', 'gl_core_close_snapshot', 'gl_core_causal_scenario', 'gl_core_reconciliation_case', 'gl_core_semantic_source_document', 'gl_core_regulatory_rule_version', 'gl_core_predictive_validation_run', 'gl_core_audit_proof', 'gl_core_policy_decision', 'gl_core_control_assertion', 'gl_core_ledger_federation_link', 'gl_core_identity_credential', 'gl_core_resilience_drill', 'gl_core_crypto_key_epoch', 'gl_core_carbon_execution_window'), 'read_tables': (), 'emitted_event': 'ConsensusCommitted', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_consensus_commits', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/gl_core/consensus-commits', 'permission': 'gl_core.command.6', 'owned_tables': ('gl_core_ledger_event_log', 'gl_core_journal_entry', 'gl_core_journal_line', 'gl_core_ledger_account', 'gl_core_accounting_period', 'gl_core_ledger_projection', 'gl_core_consensus_replica', 'gl_core_schema_extension', 'gl_core_tenant_ledger_partition', 'gl_core_probabilistic_posting', 'gl_core_close_snapshot', 'gl_core_causal_scenario', 'gl_core_reconciliation_case', 'gl_core_semantic_source_document', 'gl_core_regulatory_rule_version', 'gl_core_predictive_validation_run', 'gl_core_audit_proof', 'gl_core_policy_decision', 'gl_core_control_assertion', 'gl_core_ledger_federation_link', 'gl_core_identity_credential', 'gl_core_resilience_drill', 'gl_core_crypto_key_epoch', 'gl_core_carbon_execution_window'), 'read_tables': (), 'emitted_event': 'LedgerProjectionRebuilt', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_schema_extensions', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/gl_core/schema-extensions', 'permission': 'gl_core.command.7', 'owned_tables': ('gl_core_ledger_event_log', 'gl_core_journal_entry', 'gl_core_journal_line', 'gl_core_ledger_account', 'gl_core_accounting_period', 'gl_core_ledger_projection', 'gl_core_consensus_replica', 'gl_core_schema_extension', 'gl_core_tenant_ledger_partition', 'gl_core_probabilistic_posting', 'gl_core_close_snapshot', 'gl_core_causal_scenario', 'gl_core_reconciliation_case', 'gl_core_semantic_source_document', 'gl_core_regulatory_rule_version', 'gl_core_predictive_validation_run', 'gl_core_audit_proof', 'gl_core_policy_decision', 'gl_core_control_assertion', 'gl_core_ledger_federation_link', 'gl_core_identity_credential', 'gl_core_resilience_drill', 'gl_core_crypto_key_epoch', 'gl_core_carbon_execution_window'), 'read_tables': (), 'emitted_event': 'ContinuousCloseSnapshotCreated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_temporal_ledger', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/gl_core/temporal-ledger', 'permission': 'gl_core.query.8', 'owned_tables': (), 'read_tables': ('gl_core_ledger_event_log', 'gl_core_journal_entry', 'gl_core_journal_line', 'gl_core_ledger_account', 'gl_core_accounting_period', 'gl_core_ledger_projection', 'gl_core_consensus_replica', 'gl_core_schema_extension', 'gl_core_tenant_ledger_partition', 'gl_core_probabilistic_posting', 'gl_core_close_snapshot', 'gl_core_causal_scenario', 'gl_core_reconciliation_case', 'gl_core_semantic_source_document', 'gl_core_regulatory_rule_version', 'gl_core_predictive_validation_run', 'gl_core_audit_proof', 'gl_core_policy_decision', 'gl_core_control_assertion', 'gl_core_ledger_federation_link', 'gl_core_identity_credential', 'gl_core_resilience_drill', 'gl_core_crypto_key_epoch', 'gl_core_carbon_execution_window'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_probabilistic_postings', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/gl_core/probabilistic-postings', 'permission': 'gl_core.command.9', 'owned_tables': ('gl_core_ledger_event_log', 'gl_core_journal_entry', 'gl_core_journal_line', 'gl_core_ledger_account', 'gl_core_accounting_period', 'gl_core_ledger_projection', 'gl_core_consensus_replica', 'gl_core_schema_extension', 'gl_core_tenant_ledger_partition', 'gl_core_probabilistic_posting', 'gl_core_close_snapshot', 'gl_core_causal_scenario', 'gl_core_reconciliation_case', 'gl_core_semantic_source_document', 'gl_core_regulatory_rule_version', 'gl_core_predictive_validation_run', 'gl_core_audit_proof', 'gl_core_policy_decision', 'gl_core_control_assertion', 'gl_core_ledger_federation_link', 'gl_core_identity_credential', 'gl_core_resilience_drill', 'gl_core_crypto_key_epoch', 'gl_core_carbon_execution_window'), 'read_tables': (), 'emitted_event': 'AuditProofGenerated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_continuous_close_snapshots', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/gl_core/continuous-close-snapshots', 'permission': 'gl_core.command.10', 'owned_tables': ('gl_core_ledger_event_log', 'gl_core_journal_entry', 'gl_core_journal_line', 'gl_core_ledger_account', 'gl_core_accounting_period', 'gl_core_ledger_projection', 'gl_core_consensus_replica', 'gl_core_schema_extension', 'gl_core_tenant_ledger_partition', 'gl_core_probabilistic_posting', 'gl_core_close_snapshot', 'gl_core_causal_scenario', 'gl_core_reconciliation_case', 'gl_core_semantic_source_document', 'gl_core_regulatory_rule_version', 'gl_core_predictive_validation_run', 'gl_core_audit_proof', 'gl_core_policy_decision', 'gl_core_control_assertion', 'gl_core_ledger_federation_link', 'gl_core_identity_credential', 'gl_core_resilience_drill', 'gl_core_crypto_key_epoch', 'gl_core_carbon_execution_window'), 'read_tables': (), 'emitted_event': 'RegulatoryRuleCompiled', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_causal_scenarios', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/gl_core/causal-scenarios', 'permission': 'gl_core.command.11', 'owned_tables': ('gl_core_ledger_event_log', 'gl_core_journal_entry', 'gl_core_journal_line', 'gl_core_ledger_account', 'gl_core_accounting_period', 'gl_core_ledger_projection', 'gl_core_consensus_replica', 'gl_core_schema_extension', 'gl_core_tenant_ledger_partition', 'gl_core_probabilistic_posting', 'gl_core_close_snapshot', 'gl_core_causal_scenario', 'gl_core_reconciliation_case', 'gl_core_semantic_source_document', 'gl_core_regulatory_rule_version', 'gl_core_predictive_validation_run', 'gl_core_audit_proof', 'gl_core_policy_decision', 'gl_core_control_assertion', 'gl_core_ledger_federation_link', 'gl_core_identity_credential', 'gl_core_resilience_drill', 'gl_core_crypto_key_epoch', 'gl_core_carbon_execution_window'), 'read_tables': (), 'emitted_event': 'PostingValidationPredicted', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_reconciliation_cases', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/gl_core/reconciliation-cases', 'permission': 'gl_core.command.12', 'owned_tables': ('gl_core_ledger_event_log', 'gl_core_journal_entry', 'gl_core_journal_line', 'gl_core_ledger_account', 'gl_core_accounting_period', 'gl_core_ledger_projection', 'gl_core_consensus_replica', 'gl_core_schema_extension', 'gl_core_tenant_ledger_partition', 'gl_core_probabilistic_posting', 'gl_core_close_snapshot', 'gl_core_causal_scenario', 'gl_core_reconciliation_case', 'gl_core_semantic_source_document', 'gl_core_regulatory_rule_version', 'gl_core_predictive_validation_run', 'gl_core_audit_proof', 'gl_core_policy_decision', 'gl_core_control_assertion', 'gl_core_ledger_federation_link', 'gl_core_identity_credential', 'gl_core_resilience_drill', 'gl_core_crypto_key_epoch', 'gl_core_carbon_execution_window'), 'read_tables': (), 'emitted_event': 'JournalPosted', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_semantic_documents', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/gl_core/semantic-documents', 'permission': 'gl_core.command.13', 'owned_tables': ('gl_core_ledger_event_log', 'gl_core_journal_entry', 'gl_core_journal_line', 'gl_core_ledger_account', 'gl_core_accounting_period', 'gl_core_ledger_projection', 'gl_core_consensus_replica', 'gl_core_schema_extension', 'gl_core_tenant_ledger_partition', 'gl_core_probabilistic_posting', 'gl_core_close_snapshot', 'gl_core_causal_scenario', 'gl_core_reconciliation_case', 'gl_core_semantic_source_document', 'gl_core_regulatory_rule_version', 'gl_core_predictive_validation_run', 'gl_core_audit_proof', 'gl_core_policy_decision', 'gl_core_control_assertion', 'gl_core_ledger_federation_link', 'gl_core_identity_credential', 'gl_core_resilience_drill', 'gl_core_crypto_key_epoch', 'gl_core_carbon_execution_window'), 'read_tables': (), 'emitted_event': 'PeriodClosed', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_regulatory_rules', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/gl_core/regulatory-rules', 'permission': 'gl_core.command.14', 'owned_tables': ('gl_core_ledger_event_log', 'gl_core_journal_entry', 'gl_core_journal_line', 'gl_core_ledger_account', 'gl_core_accounting_period', 'gl_core_ledger_projection', 'gl_core_consensus_replica', 'gl_core_schema_extension', 'gl_core_tenant_ledger_partition', 'gl_core_probabilistic_posting', 'gl_core_close_snapshot', 'gl_core_causal_scenario', 'gl_core_reconciliation_case', 'gl_core_semantic_source_document', 'gl_core_regulatory_rule_version', 'gl_core_predictive_validation_run', 'gl_core_audit_proof', 'gl_core_policy_decision', 'gl_core_control_assertion', 'gl_core_ledger_federation_link', 'gl_core_identity_credential', 'gl_core_resilience_drill', 'gl_core_crypto_key_epoch', 'gl_core_carbon_execution_window'), 'read_tables': (), 'emitted_event': 'TrialBalanceCalculated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_predictive_validations', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/gl_core/predictive-validations', 'permission': 'gl_core.command.15', 'owned_tables': ('gl_core_ledger_event_log', 'gl_core_journal_entry', 'gl_core_journal_line', 'gl_core_ledger_account', 'gl_core_accounting_period', 'gl_core_ledger_projection', 'gl_core_consensus_replica', 'gl_core_schema_extension', 'gl_core_tenant_ledger_partition', 'gl_core_probabilistic_posting', 'gl_core_close_snapshot', 'gl_core_causal_scenario', 'gl_core_reconciliation_case', 'gl_core_semantic_source_document', 'gl_core_regulatory_rule_version', 'gl_core_predictive_validation_run', 'gl_core_audit_proof', 'gl_core_policy_decision', 'gl_core_control_assertion', 'gl_core_ledger_federation_link', 'gl_core_identity_credential', 'gl_core_resilience_drill', 'gl_core_crypto_key_epoch', 'gl_core_carbon_execution_window'), 'read_tables': (), 'emitted_event': 'LedgerEventAppended', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_audit_proofs', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/gl_core/audit-proofs', 'permission': 'gl_core.command.16', 'owned_tables': ('gl_core_ledger_event_log', 'gl_core_journal_entry', 'gl_core_journal_line', 'gl_core_ledger_account', 'gl_core_accounting_period', 'gl_core_ledger_projection', 'gl_core_consensus_replica', 'gl_core_schema_extension', 'gl_core_tenant_ledger_partition', 'gl_core_probabilistic_posting', 'gl_core_close_snapshot', 'gl_core_causal_scenario', 'gl_core_reconciliation_case', 'gl_core_semantic_source_document', 'gl_core_regulatory_rule_version', 'gl_core_predictive_validation_run', 'gl_core_audit_proof', 'gl_core_policy_decision', 'gl_core_control_assertion', 'gl_core_ledger_federation_link', 'gl_core_identity_credential', 'gl_core_resilience_drill', 'gl_core_crypto_key_epoch', 'gl_core_carbon_execution_window'), 'read_tables': (), 'emitted_event': 'ConsensusCommitted', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_control_tests', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/gl_core/control-tests', 'permission': 'gl_core.command.17', 'owned_tables': ('gl_core_ledger_event_log', 'gl_core_journal_entry', 'gl_core_journal_line', 'gl_core_ledger_account', 'gl_core_accounting_period', 'gl_core_ledger_projection', 'gl_core_consensus_replica', 'gl_core_schema_extension', 'gl_core_tenant_ledger_partition', 'gl_core_probabilistic_posting', 'gl_core_close_snapshot', 'gl_core_causal_scenario', 'gl_core_reconciliation_case', 'gl_core_semantic_source_document', 'gl_core_regulatory_rule_version', 'gl_core_predictive_validation_run', 'gl_core_audit_proof', 'gl_core_policy_decision', 'gl_core_control_assertion', 'gl_core_ledger_federation_link', 'gl_core_identity_credential', 'gl_core_resilience_drill', 'gl_core_crypto_key_epoch', 'gl_core_carbon_execution_window'), 'read_tables': (), 'emitted_event': 'LedgerProjectionRebuilt', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_ledger_federation_links', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/gl_core/ledger-federation-links', 'permission': 'gl_core.command.18', 'owned_tables': ('gl_core_ledger_event_log', 'gl_core_journal_entry', 'gl_core_journal_line', 'gl_core_ledger_account', 'gl_core_accounting_period', 'gl_core_ledger_projection', 'gl_core_consensus_replica', 'gl_core_schema_extension', 'gl_core_tenant_ledger_partition', 'gl_core_probabilistic_posting', 'gl_core_close_snapshot', 'gl_core_causal_scenario', 'gl_core_reconciliation_case', 'gl_core_semantic_source_document', 'gl_core_regulatory_rule_version', 'gl_core_predictive_validation_run', 'gl_core_audit_proof', 'gl_core_policy_decision', 'gl_core_control_assertion', 'gl_core_ledger_federation_link', 'gl_core_identity_credential', 'gl_core_resilience_drill', 'gl_core_crypto_key_epoch', 'gl_core_carbon_execution_window'), 'read_tables': (), 'emitted_event': 'ContinuousCloseSnapshotCreated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_resilience_drills', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/gl_core/resilience-drills', 'permission': 'gl_core.command.19', 'owned_tables': ('gl_core_ledger_event_log', 'gl_core_journal_entry', 'gl_core_journal_line', 'gl_core_ledger_account', 'gl_core_accounting_period', 'gl_core_ledger_projection', 'gl_core_consensus_replica', 'gl_core_schema_extension', 'gl_core_tenant_ledger_partition', 'gl_core_probabilistic_posting', 'gl_core_close_snapshot', 'gl_core_causal_scenario', 'gl_core_reconciliation_case', 'gl_core_semantic_source_document', 'gl_core_regulatory_rule_version', 'gl_core_predictive_validation_run', 'gl_core_audit_proof', 'gl_core_policy_decision', 'gl_core_control_assertion', 'gl_core_ledger_federation_link', 'gl_core_identity_credential', 'gl_core_resilience_drill', 'gl_core_crypto_key_epoch', 'gl_core_carbon_execution_window'), 'read_tables': (), 'emitted_event': 'ReconciliationSuggested', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_carbon_execution_windows', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/gl_core/carbon-execution-windows', 'permission': 'gl_core.command.20', 'owned_tables': ('gl_core_ledger_event_log', 'gl_core_journal_entry', 'gl_core_journal_line', 'gl_core_ledger_account', 'gl_core_accounting_period', 'gl_core_ledger_projection', 'gl_core_consensus_replica', 'gl_core_schema_extension', 'gl_core_tenant_ledger_partition', 'gl_core_probabilistic_posting', 'gl_core_close_snapshot', 'gl_core_causal_scenario', 'gl_core_reconciliation_case', 'gl_core_semantic_source_document', 'gl_core_regulatory_rule_version', 'gl_core_predictive_validation_run', 'gl_core_audit_proof', 'gl_core_policy_decision', 'gl_core_control_assertion', 'gl_core_ledger_federation_link', 'gl_core_identity_credential', 'gl_core_resilience_drill', 'gl_core_crypto_key_epoch', 'gl_core_carbon_execution_window'), 'read_tables': (), 'emitted_event': 'AuditProofGenerated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item['operation'] for item in OPERATION_CONTRACTS)
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS),
        'pbc': 'gl_core',
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
        'pbc': 'gl_core',
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


class GlCoreService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        plan = operation_plan(command_name, payload)
        event_type = plan.get('emitted_event') or (EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted')
        return {
            'ok': plan['ok'],
            'pbc': 'gl_core',
            'command': command_name,
            'payload': dict(payload),
            'operation_contract': plan,
            'transaction_boundary': plan.get('transaction_boundary'),
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
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'gl_core',
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
    service = GlCoreService()
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
