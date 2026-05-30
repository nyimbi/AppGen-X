CREATE SCHEMA IF NOT EXISTS sustainability_esg_reporting;

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_esg_metric (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_materiality_assessment (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_reporting_framework_mapping (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  metric_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (metric_id) REFERENCES sustainability_esg_reporting_esg_metric(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_facility_profile (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_activity_data_record (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  facility_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (facility_id) REFERENCES sustainability_esg_reporting_facility_profile(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_emissions_factor (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  metric_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (metric_id) REFERENCES sustainability_esg_reporting_esg_metric(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_emissions_calculation (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  activity_record_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (activity_record_id) REFERENCES sustainability_esg_reporting_activity_data_record(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_scope_boundary (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  facility_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (facility_id) REFERENCES sustainability_esg_reporting_facility_profile(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_renewable_instrument (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  facility_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (facility_id) REFERENCES sustainability_esg_reporting_facility_profile(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_water_metric_record (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  facility_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (facility_id) REFERENCES sustainability_esg_reporting_facility_profile(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_waste_metric_record (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  facility_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (facility_id) REFERENCES sustainability_esg_reporting_facility_profile(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_social_metric_record (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  metric_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (metric_id) REFERENCES sustainability_esg_reporting_esg_metric(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_governance_metric_record (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  metric_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (metric_id) REFERENCES sustainability_esg_reporting_esg_metric(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_supplier_esg_input (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  metric_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (metric_id) REFERENCES sustainability_esg_reporting_esg_metric(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_assurance_control (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  metric_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (metric_id) REFERENCES sustainability_esg_reporting_esg_metric(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_assurance_evidence (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  metric_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (metric_id) REFERENCES sustainability_esg_reporting_esg_metric(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_assurance_exception (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  metric_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (metric_id) REFERENCES sustainability_esg_reporting_esg_metric(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_restatement_record (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  metric_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (metric_id) REFERENCES sustainability_esg_reporting_esg_metric(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_sustainability_target (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  metric_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (metric_id) REFERENCES sustainability_esg_reporting_esg_metric(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_target_progress (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  target_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (target_id) REFERENCES sustainability_esg_reporting_sustainability_target(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_climate_scenario (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  metric_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (metric_id) REFERENCES sustainability_esg_reporting_esg_metric(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_data_quality_check (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  metric_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (metric_id) REFERENCES sustainability_esg_reporting_esg_metric(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_disclosure_packet (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  metric_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (metric_id) REFERENCES sustainability_esg_reporting_esg_metric(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_board_pack (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  disclosure_packet_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (disclosure_packet_id) REFERENCES sustainability_esg_reporting_disclosure_packet(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_regulator_filing (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  disclosure_packet_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (disclosure_packet_id) REFERENCES sustainability_esg_reporting_disclosure_packet(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_governed_document (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  metric_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (metric_id) REFERENCES sustainability_esg_reporting_esg_metric(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_governed_instruction (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  document_id TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (document_id) REFERENCES sustainability_esg_reporting_governed_document(id)
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_policy_rule (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_runtime_parameter (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_schema_extension (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_control_assertion (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_governed_model (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  owner VARCHAR(255),
  period VARCHAR(64),
  score DECIMAL(18,6),
  version INTEGER NOT NULL DEFAULT 1,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_appgen_outbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  payload TEXT,
  retry_count INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_appgen_inbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  payload TEXT,
  retry_count INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sustainability_esg_reporting_appgen_dead_letter_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  status VARCHAR(64) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  payload TEXT,
  retry_count INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
