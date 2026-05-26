CREATE SCHEMA IF NOT EXISTS gl_core;

CREATE TABLE gl_core_ledger_event_log (
  id INTEGER PRIMARY KEY NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gl_core_journal_entry (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_journal_line (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_ledger_account (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_accounting_period (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_ledger_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_consensus_replica (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_tenant_ledger_partition (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_probabilistic_posting (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_close_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_causal_scenario (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_reconciliation_case (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_semantic_source_document (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_regulatory_rule_version (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_predictive_validation_run (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_audit_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_policy_decision (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_ledger_federation_link (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_identity_credential (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_resilience_drill (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_crypto_key_epoch (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_carbon_execution_window (
  id INTEGER PRIMARY KEY NOT NULL,
  ledger_event_log_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ledger_event_log_id) REFERENCES gl_core_ledger_event_log(id)
);

CREATE TABLE gl_core_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE gl_core_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE gl_core_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);
