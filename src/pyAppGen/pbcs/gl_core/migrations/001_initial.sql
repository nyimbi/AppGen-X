CREATE SCHEMA IF NOT EXISTS gl_core;

CREATE TABLE gl_core_ledger_event_log (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  valid_at TIMESTAMP NOT NULL,
  processing_time VARCHAR(255) NOT NULL,
  payload_hash TEXT NOT NULL,
  previous_hash VARCHAR(255) NOT NULL,
  signature VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_journal_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  valid_at TIMESTAMP NOT NULL,
  processing_time VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_journal_entry (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  journal_id VARCHAR(255) PRIMARY KEY NOT NULL,
  period_id VARCHAR(255) PRIMARY KEY NOT NULL,
  status VARCHAR(255) NOT NULL,
  source_document_hash VARCHAR(255) NOT NULL,
  approval_state VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (period_id) REFERENCES gl_core_accounting_period(period_id)
);

CREATE TABLE gl_core_journal_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  journal_id VARCHAR(255) PRIMARY KEY NOT NULL,
  line_id VARCHAR(255) PRIMARY KEY NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  debit DECIMAL(18, 4) NOT NULL,
  credit DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  dimensions TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (journal_id) REFERENCES gl_core_journal_entry(journal_id),
  FOREIGN KEY (account_id) REFERENCES gl_core_ledger_account(account_id)
);

CREATE TABLE gl_core_ledger_account (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  account_id VARCHAR(255) PRIMARY KEY NOT NULL,
  account_code VARCHAR(255) NOT NULL,
  account_type VARCHAR(255) NOT NULL,
  normal_balance DECIMAL(18, 4) NOT NULL,
  parent_account_id VARCHAR(255) PRIMARY KEY NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_accounting_period (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  period_id VARCHAR(255) PRIMARY KEY NOT NULL,
  fiscal_year VARCHAR(255) NOT NULL,
  period_number VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  closed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_ledger_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  projection_id VARCHAR(255) PRIMARY KEY NOT NULL,
  period_id VARCHAR(255) PRIMARY KEY NOT NULL,
  dimension_hash VARCHAR(255) NOT NULL,
  balance_hash DECIMAL(18, 4) NOT NULL,
  source_event_count INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_account_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  account_id VARCHAR(255) PRIMARY KEY NOT NULL,
  period_id VARCHAR(255) PRIMARY KEY NOT NULL,
  currency VARCHAR(255) NOT NULL,
  debit_total DECIMAL(18, 4) NOT NULL,
  credit_total DECIMAL(18, 4) NOT NULL,
  ending_balance DECIMAL(18, 4) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (account_id) REFERENCES gl_core_ledger_account(account_id)
);

CREATE TABLE gl_core_consensus_replica (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  replica_id VARCHAR(255) PRIMARY KEY NOT NULL,
  node_region VARCHAR(255) NOT NULL,
  term VARCHAR(255) NOT NULL,
  commit_index VARCHAR(255) NOT NULL,
  health_state VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  table_name VARCHAR(255) NOT NULL,
  field_name VARCHAR(255) NOT NULL,
  field_type VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  compatibility VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_tenant_ledger_partition (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  partition_id VARCHAR(255) PRIMARY KEY NOT NULL,
  encryption_key_ref VARCHAR(255) NOT NULL,
  residency_region VARCHAR(255) NOT NULL,
  retention_policy VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_probabilistic_posting (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  posting_id VARCHAR(255) PRIMARY KEY NOT NULL,
  account_id VARCHAR(255) PRIMARY KEY NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  uncertainty_exposure VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_close_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  snapshot_id VARCHAR(255) PRIMARY KEY NOT NULL,
  period_id VARCHAR(255) PRIMARY KEY NOT NULL,
  audit_ready VARCHAR(255) NOT NULL,
  control_hash VARCHAR(255) NOT NULL,
  approval_state VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (period_id) REFERENCES gl_core_accounting_period(period_id)
);

CREATE TABLE gl_core_causal_scenario (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  scenario_id VARCHAR(255) PRIMARY KEY NOT NULL,
  driver VARCHAR(255) NOT NULL,
  counterfactual_hash VARCHAR(255) NOT NULL,
  impact_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_reconciliation_case (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  case_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_id VARCHAR(255) PRIMARY KEY NOT NULL,
  ledger_event_id VARCHAR(255) NOT NULL,
  score DECIMAL(18, 4) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_id) REFERENCES gl_core_journal_event(event_id)
);

CREATE TABLE gl_core_semantic_source_document (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  document_id VARCHAR(255) PRIMARY KEY NOT NULL,
  source_hash VARCHAR(255) NOT NULL,
  derived_account VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  audit_trace VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_regulatory_rule_version (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_version_id VARCHAR(255) PRIMARY KEY NOT NULL,
  standard VARCHAR(255) NOT NULL,
  version_hash VARCHAR(255) NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  compiled_predicate TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  scope VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  predicate TEXT NOT NULL,
  decision_effect VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_predictive_validation_run (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) PRIMARY KEY NOT NULL,
  journal_id VARCHAR(255) PRIMARY KEY NOT NULL,
  decision VARCHAR(255) NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_audit_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  proof_id VARCHAR(255) PRIMARY KEY NOT NULL,
  proof_type VARCHAR(255) NOT NULL,
  public_claims_hash TEXT NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  channel VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_policy_decision (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  decision_id VARCHAR(255) PRIMARY KEY NOT NULL,
  actor VARCHAR(255) NOT NULL,
  action VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  reason_codes VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  control_id VARCHAR(255) PRIMARY KEY NOT NULL,
  assertion VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  tested_at TIMESTAMP NOT NULL,
  evidence_hash TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_ledger_federation_link (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  link_id VARCHAR(255) PRIMARY KEY NOT NULL,
  external_system VARCHAR(255) NOT NULL,
  projection_name VARCHAR(255) NOT NULL,
  api_contract VARCHAR(255) NOT NULL,
  event_contract VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_identity_credential (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  credential_id VARCHAR(255) PRIMARY KEY NOT NULL,
  did VARCHAR(255) NOT NULL,
  issuer VARCHAR(255) NOT NULL,
  subject VARCHAR(255) NOT NULL,
  credential_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_resilience_drill (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  drill_id VARCHAR(255) PRIMARY KEY NOT NULL,
  scenario VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  remaining_quorum VARCHAR(255) NOT NULL,
  executed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_crypto_key_epoch (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  key_epoch VARCHAR(255) NOT NULL,
  algorithm VARCHAR(255) NOT NULL,
  attestation VARCHAR(255) NOT NULL,
  rotated_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_carbon_execution_window (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  window_id VARCHAR(255) PRIMARY KEY NOT NULL,
  region VARCHAR(255) NOT NULL,
  carbon_intensity VARCHAR(255) NOT NULL,
  selected VARCHAR(255) NOT NULL,
  scheduled_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_financial_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) PRIMARY KEY NOT NULL,
  model_name VARCHAR(255) NOT NULL,
  feature_lineage VARCHAR(255) NOT NULL,
  drift_score DECIMAL(18, 4) NOT NULL,
  materiality_gate VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_appgen_outbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  payload_hash TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_appgen_inbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_dead_letter_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  reason VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
