CREATE SCHEMA IF NOT EXISTS contract_lifecycle;

CREATE TABLE contract_lifecycle_contract_record (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_type VARCHAR(128),
  jurisdiction VARCHAR(128),
  value_amount DECIMAL(18, 2),
  currency VARCHAR(16),
  counterparty_name VARCHAR(255),
  effective_date DATE,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_party (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_id TEXT NOT NULL REFERENCES contract_lifecycle_contract_record(id),
  role VARCHAR(128) NOT NULL,
  legal_name VARCHAR(255) NOT NULL,
  authority_state VARCHAR(128),
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_clause_library (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_id TEXT NOT NULL REFERENCES contract_lifecycle_contract_record(id),
  clause_family VARCHAR(255) NOT NULL,
  variant_code VARCHAR(255) NOT NULL,
  fallback_tier VARCHAR(64),
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_clause_variant (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_id TEXT NOT NULL REFERENCES contract_lifecycle_contract_record(id),
  variant_code VARCHAR(255) NOT NULL,
  fallback_tier VARCHAR(64),
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_document_packet (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_id TEXT NOT NULL REFERENCES contract_lifecycle_contract_record(id),
  packet_type VARCHAR(128) NOT NULL,
  document_hash VARCHAR(255),
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_authoring_workspace (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_id TEXT NOT NULL REFERENCES contract_lifecycle_contract_record(id),
  template_code VARCHAR(255) NOT NULL,
  workspace_owner VARCHAR(255) NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_negotiation_round (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_id TEXT NOT NULL REFERENCES contract_lifecycle_contract_record(id),
  sender VARCHAR(255) NOT NULL,
  receiver VARCHAR(255) NOT NULL,
  response_due_date DATE,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_redline_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_id TEXT NOT NULL REFERENCES contract_lifecycle_contract_record(id),
  changed_clause VARCHAR(255) NOT NULL,
  materiality_score DECIMAL(6, 4),
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_approval_policy (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_id TEXT NOT NULL REFERENCES contract_lifecycle_contract_record(id),
  policy_name VARCHAR(255) NOT NULL,
  route_hash VARCHAR(255),
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_approval_task (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_id TEXT NOT NULL REFERENCES contract_lifecycle_contract_record(id),
  approver_role VARCHAR(255) NOT NULL,
  due_date DATE,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_signature_packet (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_id TEXT NOT NULL REFERENCES contract_lifecycle_contract_record(id),
  signer_name VARCHAR(255) NOT NULL,
  authority_state VARCHAR(128) NOT NULL,
  document_hash VARCHAR(255),
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_obligation (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_id TEXT NOT NULL REFERENCES contract_lifecycle_contract_record(id),
  owner VARCHAR(255) NOT NULL,
  due_date DATE NOT NULL,
  evidence_required BOOLEAN NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_obligation_performance_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_id TEXT NOT NULL REFERENCES contract_lifecycle_contract_record(id),
  obligation_id TEXT NOT NULL,
  performed_by VARCHAR(255) NOT NULL,
  evidence_uri VARCHAR(512),
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_milestone (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_id TEXT NOT NULL REFERENCES contract_lifecycle_contract_record(id),
  milestone_date DATE NOT NULL,
  owner VARCHAR(255) NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_renewal_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_id TEXT NOT NULL REFERENCES contract_lifecycle_contract_record(id),
  notice_date DATE NOT NULL,
  renewal_decision VARCHAR(128) NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_amendment (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_id TEXT NOT NULL REFERENCES contract_lifecycle_contract_record(id),
  effective_date DATE NOT NULL,
  change_summary VARCHAR(512) NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_compliance_check (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_id TEXT NOT NULL REFERENCES contract_lifecycle_contract_record(id),
  check_name VARCHAR(255) NOT NULL,
  result VARCHAR(64) NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_risk_assessment (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_id TEXT NOT NULL REFERENCES contract_lifecycle_contract_record(id),
  risk_score DECIMAL(6, 4) NOT NULL,
  risk_level VARCHAR(64) NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_value_snapshot (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_id TEXT NOT NULL REFERENCES contract_lifecycle_contract_record(id),
  snapshot_amount DECIMAL(18, 2) NOT NULL,
  currency VARCHAR(16) NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_search_index (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_id TEXT NOT NULL REFERENCES contract_lifecycle_contract_record(id),
  index_terms TEXT NOT NULL,
  document_hash VARCHAR(255),
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_exception_case (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_id TEXT NOT NULL REFERENCES contract_lifecycle_contract_record(id),
  severity VARCHAR(64) NOT NULL,
  owner VARCHAR(255) NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_policy_rule (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  contract_id TEXT NOT NULL,
  rule_name VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_runtime_parameter (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  parameter_name VARCHAR(255) NOT NULL,
  parameter_value VARCHAR(255) NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_schema_extension (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  target_table_name VARCHAR(255) NOT NULL,
  extension_hash VARCHAR(255) NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_control_assertion (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  control_id VARCHAR(255) NOT NULL,
  assertion_result VARCHAR(64) NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_contract_governed_model (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  model_name VARCHAR(255) NOT NULL,
  governance_state VARCHAR(64) NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_appgen_outbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_appgen_inbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contract_lifecycle_appgen_dead_letter_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  version INTEGER NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  dead_letter_reason VARCHAR(255) NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
