CREATE SCHEMA IF NOT EXISTS audit_ledger;

CREATE TABLE audit_ledger_audit_event (
  tenant TEXT NOT NULL,
  audit_id TEXT NOT NULL,
  source_pbc TEXT,
  aggregate_id TEXT NOT NULL,
  actor TEXT,
  action TEXT,
  classification TEXT,
  payload_hash TEXT,
  sequence INTEGER,
  previous_hash TEXT,
  event_hash TEXT,
  signature TEXT,
  sealed BOOLEAN,
  PRIMARY KEY (audit_id, aggregate_id)
);

CREATE TABLE audit_ledger_signature_chain (
  tenant TEXT NOT NULL,
  chain_link_id TEXT NOT NULL,
  audit_id TEXT NOT NULL,
  sequence INTEGER,
  previous_hash TEXT,
  event_hash TEXT,
  signature TEXT,
  verified BOOLEAN,
  PRIMARY KEY (chain_link_id, audit_id)
);

CREATE TABLE audit_ledger_retention_policy (
  tenant TEXT NOT NULL,
  policy_id TEXT NOT NULL,
  classification TEXT,
  retention_days INTEGER,
  legal_hold BOOLEAN,
  disposal_action TEXT,
  status TEXT NOT NULL,
  PRIMARY KEY (policy_id)
);

CREATE TABLE audit_ledger_forensic_export (
  tenant TEXT NOT NULL,
  export_id TEXT NOT NULL,
  classification TEXT,
  requested_by TEXT,
  event_count INTEGER,
  checksum TEXT,
  proof_bundle TEXT,
  status TEXT NOT NULL,
  PRIMARY KEY (export_id)
);

CREATE TABLE audit_ledger_access_evidence (
  tenant TEXT NOT NULL,
  evidence_id TEXT NOT NULL,
  principal TEXT,
  resource TEXT,
  action TEXT,
  decision TEXT,
  context_hash TEXT,
  policy_source TEXT,
  PRIMARY KEY (evidence_id)
);

CREATE TABLE audit_ledger_control_assertion (
  tenant TEXT NOT NULL,
  control_id TEXT NOT NULL,
  control TEXT,
  status TEXT NOT NULL,
  severity TEXT,
  evidence_hash TEXT,
  release_blocking BOOLEAN,
  remediation TEXT,
  PRIMARY KEY (control_id)
);

CREATE TABLE audit_ledger_rule (
  tenant TEXT NOT NULL,
  rule_id TEXT NOT NULL,
  scope TEXT,
  classification TEXT,
  minimum_retention_days INTEGER,
  requires_export_approval BOOLEAN,
  severity TEXT,
  status TEXT NOT NULL,
  PRIMARY KEY (rule_id)
);

CREATE TABLE audit_ledger_parameter (
  tenant TEXT NOT NULL,
  parameter_id TEXT NOT NULL,
  name TEXT,
  value TEXT,
  bounds TEXT,
  compiled_hash TEXT,
  PRIMARY KEY (parameter_id)
);

CREATE TABLE audit_ledger_configuration (
  tenant TEXT NOT NULL,
  configuration_id TEXT NOT NULL,
  database_backend TEXT,
  event_topic TEXT,
  retry_limit INTEGER,
  signature_algorithm TEXT,
  default_timezone TEXT,
  PRIMARY KEY (configuration_id)
);

CREATE TABLE audit_ledger_projection_link (
  tenant TEXT NOT NULL,
  projection_id TEXT NOT NULL,
  audit_id TEXT NOT NULL,
  target_system TEXT,
  projection_hash TEXT,
  handoff_status TEXT,
  PRIMARY KEY (projection_id, audit_id)
);

CREATE TABLE audit_ledger_schema_extension (
  tenant TEXT NOT NULL,
  extension_id TEXT NOT NULL,
  table_name TEXT,
  field_name TEXT,
  field_type TEXT,
  version INTEGER,
  PRIMARY KEY (extension_id)
);

CREATE TABLE audit_ledger_disclosure_proof (
  tenant TEXT NOT NULL,
  proof_id TEXT NOT NULL,
  audit_id TEXT NOT NULL,
  proof_hash TEXT,
  disclosure_fields INTEGER,
  created_at TIMESTAMP,
  PRIMARY KEY (proof_id, audit_id)
);

CREATE TABLE audit_ledger_anomaly_signal (
  tenant TEXT NOT NULL,
  signal_id TEXT NOT NULL,
  audit_id TEXT NOT NULL,
  signal_type TEXT,
  entropy DECIMAL(12,4),
  detected_at TIMESTAMP,
  PRIMARY KEY (signal_id, audit_id)
);

CREATE TABLE audit_ledger_identity_credential (
  tenant TEXT NOT NULL,
  credential_id TEXT NOT NULL,
  actor_did TEXT,
  issuer TEXT,
  status TEXT NOT NULL,
  verified_at TIMESTAMP,
  PRIMARY KEY (credential_id)
);

CREATE TABLE audit_ledger_resilience_drill (
  tenant TEXT NOT NULL,
  drill_id TEXT NOT NULL,
  scenario TEXT,
  mode TEXT,
  replay_source TEXT,
  executed_at TIMESTAMP,
  PRIMARY KEY (drill_id)
);

CREATE TABLE audit_ledger_crypto_key_epoch (
  tenant TEXT NOT NULL,
  epoch_id TEXT NOT NULL,
  algorithm TEXT,
  epoch INTEGER,
  signature_policy TEXT,
  activated_at TIMESTAMP,
  PRIMARY KEY (epoch_id)
);

CREATE TABLE audit_ledger_carbon_processing_window (
  tenant TEXT NOT NULL,
  window_id TEXT NOT NULL,
  window TEXT,
  carbon_score DECIMAL(12,4),
  scheduled_load INTEGER,
  status TEXT NOT NULL,
  PRIMARY KEY (window_id)
);

CREATE TABLE audit_ledger_governed_model (
  tenant TEXT NOT NULL,
  model_id TEXT NOT NULL,
  name TEXT,
  feature_lineage TEXT,
  auc DECIMAL(12,4),
  drift_score DECIMAL(12,4),
  governance_status TEXT,
  PRIMARY KEY (model_id)
);

CREATE TABLE audit_ledger_appgen_outbox_event (
  tenant TEXT NOT NULL,
  event_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  topic TEXT,
  idempotency_key TEXT NOT NULL,
  status TEXT NOT NULL,
  audit_hash TEXT,
  PRIMARY KEY (event_id)
);

CREATE TABLE audit_ledger_appgen_inbox_event (
  tenant TEXT NOT NULL,
  event_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  attempts INTEGER,
  status TEXT NOT NULL,
  received_at TIMESTAMP,
  PRIMARY KEY (event_id)
);

CREATE TABLE audit_ledger_dead_letter_event (
  tenant TEXT NOT NULL,
  event_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  attempts INTEGER,
  reason TEXT,
  recorded_at TIMESTAMP,
  PRIMARY KEY (event_id)
);

-- Relationship: audit_ledger_signature_chain.audit_id -> audit_ledger_audit_event.audit_id (owned_hash_chain)
-- Relationship: audit_ledger_forensic_export.classification -> audit_ledger_retention_policy.classification (owned_retention_binding)
-- Relationship: audit_ledger_control_assertion.evidence_hash -> audit_ledger_audit_event.event_hash (owned_control_evidence)
-- Relationship: audit_ledger_projection_link.audit_id -> audit_ledger_audit_event.audit_id (owned_projection_handoff)
-- Relationship: audit_ledger_disclosure_proof.audit_id -> audit_ledger_audit_event.audit_id (owned_proof)
-- Relationship: audit_ledger_anomaly_signal.audit_id -> audit_ledger_audit_event.audit_id (owned_anomaly)
-- Relationship: audit_ledger_appgen_outbox_event.event_id -> audit_ledger_audit_event.audit_id (owned_outbox_evidence)
