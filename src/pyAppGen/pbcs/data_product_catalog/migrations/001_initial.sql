CREATE SCHEMA IF NOT EXISTS data_product_catalog;

CREATE TABLE IF NOT EXISTS data_product_catalog_data_product (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  product_type TEXT NOT NULL,
  value_proposition TEXT NOT NULL,
  consumer_personas TEXT
);

CREATE TABLE IF NOT EXISTS data_product_catalog_data_product_owner (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  data_product_id TEXT NOT NULL,
  owner_role TEXT NOT NULL,
  owner_email TEXT NOT NULL,
  review_cadence_days INTEGER NOT NULL,
  FOREIGN KEY (data_product_id) REFERENCES data_product_catalog_data_product(id)
);

CREATE TABLE IF NOT EXISTS data_product_catalog_data_contract (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  data_product_id TEXT NOT NULL,
  compatibility_level TEXT NOT NULL,
  clause_library TEXT,
  published_at TIMESTAMP,
  FOREIGN KEY (data_product_id) REFERENCES data_product_catalog_data_product(id)
);

CREATE TABLE IF NOT EXISTS data_product_catalog_data_schema_version (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  data_product_id TEXT NOT NULL,
  schema_version TEXT NOT NULL,
  field_semantics TEXT,
  compatibility_result TEXT NOT NULL,
  FOREIGN KEY (data_product_id) REFERENCES data_product_catalog_data_product(id)
);

CREATE TABLE IF NOT EXISTS data_product_catalog_data_quality_signal (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  data_product_id TEXT NOT NULL,
  quality_dimension TEXT NOT NULL,
  threshold DECIMAL(10, 4) NOT NULL,
  severity TEXT NOT NULL,
  observed_at TIMESTAMP NOT NULL,
  FOREIGN KEY (data_product_id) REFERENCES data_product_catalog_data_product(id)
);

CREATE TABLE IF NOT EXISTS data_product_catalog_data_lineage_edge (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  data_product_id TEXT NOT NULL,
  upstream_product_code TEXT NOT NULL,
  edge_type TEXT NOT NULL,
  freshness_minutes INTEGER,
  FOREIGN KEY (data_product_id) REFERENCES data_product_catalog_data_product(id)
);

CREATE TABLE IF NOT EXISTS data_product_catalog_data_access_request (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  data_product_id TEXT NOT NULL,
  requester TEXT NOT NULL,
  use_case TEXT NOT NULL,
  risk_score DECIMAL(10, 4) NOT NULL,
  requested_at TIMESTAMP NOT NULL,
  FOREIGN KEY (data_product_id) REFERENCES data_product_catalog_data_product(id)
);

CREATE TABLE IF NOT EXISTS data_product_catalog_data_access_grant (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  data_product_id TEXT NOT NULL,
  grantee TEXT NOT NULL,
  grant_scope TEXT NOT NULL,
  expires_at TIMESTAMP,
  approved_at TIMESTAMP NOT NULL,
  FOREIGN KEY (data_product_id) REFERENCES data_product_catalog_data_product(id)
);

CREATE TABLE IF NOT EXISTS data_product_catalog_data_subscription (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  data_product_id TEXT NOT NULL,
  consumer_name TEXT NOT NULL,
  delivery_mode TEXT NOT NULL,
  subscribed_at TIMESTAMP NOT NULL,
  FOREIGN KEY (data_product_id) REFERENCES data_product_catalog_data_product(id)
);

CREATE TABLE IF NOT EXISTS data_product_catalog_data_product_certification (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  data_product_id TEXT NOT NULL,
  certification_level TEXT NOT NULL,
  certified_at TIMESTAMP NOT NULL,
  expires_at TIMESTAMP,
  FOREIGN KEY (data_product_id) REFERENCES data_product_catalog_data_product(id)
);

CREATE TABLE IF NOT EXISTS data_product_catalog_data_product_usage (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  data_product_id TEXT NOT NULL,
  consumer_name TEXT NOT NULL,
  request_volume INTEGER NOT NULL,
  measured_at TIMESTAMP NOT NULL,
  FOREIGN KEY (data_product_id) REFERENCES data_product_catalog_data_product(id)
);

CREATE TABLE IF NOT EXISTS data_product_catalog_data_product_sla (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  data_product_id TEXT NOT NULL,
  commitment_type TEXT NOT NULL,
  threshold DECIMAL(10, 4) NOT NULL,
  measurement_window TEXT NOT NULL,
  FOREIGN KEY (data_product_id) REFERENCES data_product_catalog_data_product(id)
);

CREATE TABLE IF NOT EXISTS data_product_catalog_data_product_incident (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  data_product_id TEXT NOT NULL,
  severity TEXT NOT NULL,
  incident_state TEXT NOT NULL,
  opened_at TIMESTAMP NOT NULL,
  FOREIGN KEY (data_product_id) REFERENCES data_product_catalog_data_product(id)
);

CREATE TABLE IF NOT EXISTS data_product_catalog_data_product_change (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  data_product_id TEXT NOT NULL,
  change_type TEXT NOT NULL,
  notice_window_days INTEGER NOT NULL,
  effective_on TIMESTAMP,
  FOREIGN KEY (data_product_id) REFERENCES data_product_catalog_data_product(id)
);

CREATE TABLE IF NOT EXISTS data_product_catalog_data_product_retention_policy (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  data_product_id TEXT NOT NULL,
  retention_period_days INTEGER NOT NULL,
  legal_basis TEXT NOT NULL,
  disposition_action TEXT NOT NULL,
  FOREIGN KEY (data_product_id) REFERENCES data_product_catalog_data_product(id)
);

CREATE TABLE IF NOT EXISTS data_product_catalog_data_product_exception_case (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  data_product_id TEXT NOT NULL,
  case_type TEXT NOT NULL,
  owner_code TEXT NOT NULL,
  resolution_due_at TIMESTAMP,
  FOREIGN KEY (data_product_id) REFERENCES data_product_catalog_data_product(id)
);

CREATE TABLE IF NOT EXISTS data_product_catalog_data_product_policy_rule (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  data_product_id TEXT NOT NULL,
  rule_scope TEXT NOT NULL,
  rule_hash TEXT NOT NULL,
  compiled_at TIMESTAMP,
  FOREIGN KEY (data_product_id) REFERENCES data_product_catalog_data_product(id)
);

CREATE TABLE IF NOT EXISTS data_product_catalog_data_product_runtime_parameter (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  parameter_key TEXT NOT NULL,
  parameter_value TEXT NOT NULL,
  parameter_scope TEXT NOT NULL,
  bounded BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS data_product_catalog_data_product_schema_extension (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  data_product_id TEXT NOT NULL,
  extension_kind TEXT NOT NULL,
  applied_at TIMESTAMP NOT NULL,
  FOREIGN KEY (data_product_id) REFERENCES data_product_catalog_data_product(id)
);

CREATE TABLE IF NOT EXISTS data_product_catalog_data_product_control_assertion (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  data_product_id TEXT NOT NULL,
  control_name TEXT NOT NULL,
  assertion_outcome TEXT NOT NULL,
  asserted_at TIMESTAMP NOT NULL,
  FOREIGN KEY (data_product_id) REFERENCES data_product_catalog_data_product(id)
);

CREATE TABLE IF NOT EXISTS data_product_catalog_data_product_governed_model (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  data_product_id TEXT NOT NULL,
  model_name TEXT NOT NULL,
  model_version TEXT NOT NULL,
  approval_state TEXT NOT NULL,
  FOREIGN KEY (data_product_id) REFERENCES data_product_catalog_data_product(id)
);

CREATE TABLE IF NOT EXISTS data_product_catalog_appgen_outbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  event_type TEXT NOT NULL,
  event_topic TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  published_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS data_product_catalog_appgen_inbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  event_type TEXT NOT NULL,
  source_event_id TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  received_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS data_product_catalog_appgen_dead_letter_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  evidence_payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  event_type TEXT NOT NULL,
  source_event_id TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  retry_count INTEGER NOT NULL,
  dead_lettered_at TIMESTAMP NOT NULL
);
