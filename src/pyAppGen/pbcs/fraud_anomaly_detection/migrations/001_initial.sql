CREATE SCHEMA IF NOT EXISTS fraud_anomaly_detection;

CREATE TABLE fraud_anomaly_detection_risk_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  signal_id VARCHAR(255) NOT NULL,
  subject_key VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  region VARCHAR(64) NOT NULL,
  raw_score DOUBLE PRECISION NOT NULL,
  severity VARCHAR(64) NOT NULL,
  source_event_id VARCHAR(255) NOT NULL,
  signal_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE fraud_anomaly_detection_anomaly_score (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  anomaly_score_id VARCHAR(255) NOT NULL,
  signal_id VARCHAR(255) NOT NULL,
  subject_key VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  risk_score DOUBLE PRECISION NOT NULL,
  confidence DOUBLE PRECISION NOT NULL,
  decision VARCHAR(64) NOT NULL,
  severity VARCHAR(64) NOT NULL,
  recommended_queue VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE fraud_anomaly_detection_fraud_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  fraud_rule_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  score_adjustment DOUBLE PRECISION NOT NULL,
  decision VARCHAR(64) NOT NULL,
  status VARCHAR(64) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  trigger_payload TEXT NOT NULL
);

CREATE TABLE fraud_anomaly_detection_risk_case (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  case_id VARCHAR(255) NOT NULL,
  signal_id VARCHAR(255) NOT NULL,
  anomaly_score_id VARCHAR(255) NOT NULL,
  subject_key VARCHAR(255) NOT NULL,
  severity VARCHAR(64) NOT NULL,
  status VARCHAR(64) NOT NULL,
  queue VARCHAR(255) NOT NULL,
  recommended_action VARCHAR(64) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE fraud_anomaly_detection_identity_link (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  identity_link_id VARCHAR(255) NOT NULL,
  subject_key VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255),
  email VARCHAR(255),
  device_id VARCHAR(255),
  ip_address VARCHAR(255),
  principal_id VARCHAR(255),
  link_strength DOUBLE PRECISION NOT NULL
);

CREATE TABLE fraud_anomaly_detection_behavior_baseline (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  baseline_id VARCHAR(255) NOT NULL,
  subject_key VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  window_days INTEGER NOT NULL,
  event_count INTEGER NOT NULL,
  mean_amount DOUBLE PRECISION NOT NULL,
  risk_mean DOUBLE PRECISION NOT NULL,
  last_observed_at TIMESTAMP
);

CREATE TABLE fraud_anomaly_detection_device_fingerprint (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  device_fingerprint_id VARCHAR(255) NOT NULL,
  device_id VARCHAR(255) NOT NULL,
  subject_key VARCHAR(255) NOT NULL,
  trust_level VARCHAR(64) NOT NULL,
  first_seen_at TIMESTAMP,
  last_seen_at TIMESTAMP,
  signals TEXT NOT NULL
);

CREATE TABLE fraud_anomaly_detection_network_indicator (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  network_indicator_id VARCHAR(255) NOT NULL,
  ip_address VARCHAR(255) NOT NULL,
  asn VARCHAR(64),
  region VARCHAR(64) NOT NULL,
  risk_score DOUBLE PRECISION NOT NULL,
  vpn_detected BOOLEAN NOT NULL,
  observed_at TIMESTAMP
);

CREATE TABLE fraud_anomaly_detection_velocity_window (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  velocity_window_id VARCHAR(255) NOT NULL,
  subject_key VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  window_minutes INTEGER NOT NULL,
  event_count INTEGER NOT NULL,
  amount_total DOUBLE PRECISION NOT NULL,
  risk_score DOUBLE PRECISION NOT NULL
);

CREATE TABLE fraud_anomaly_detection_decision_explanation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  explanation_id VARCHAR(255) NOT NULL,
  anomaly_score_id VARCHAR(255) NOT NULL,
  reason_codes TEXT NOT NULL,
  feature_weights TEXT NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE fraud_anomaly_detection_loss_exposure (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  loss_exposure_id VARCHAR(255) NOT NULL,
  case_id VARCHAR(255) NOT NULL,
  amount DOUBLE PRECISION NOT NULL,
  currency VARCHAR(16) NOT NULL,
  expected_loss DOUBLE PRECISION NOT NULL,
  tail_loss DOUBLE PRECISION NOT NULL,
  status VARCHAR(64) NOT NULL
);

CREATE TABLE fraud_anomaly_detection_analyst_queue_item (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  queue_item_id VARCHAR(255) NOT NULL,
  case_id VARCHAR(255) NOT NULL,
  queue VARCHAR(255) NOT NULL,
  priority DOUBLE PRECISION NOT NULL,
  assigned_to VARCHAR(255),
  sla_due_at TIMESTAMP,
  status VARCHAR(64) NOT NULL
);

CREATE TABLE fraud_anomaly_detection_fraud_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  value TEXT NOT NULL,
  bounds TEXT NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  updated_at TIMESTAMP
);

CREATE TABLE fraud_anomaly_detection_fraud_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  configuration_id VARCHAR(255) NOT NULL,
  database_backend VARCHAR(64) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  retry_limit INTEGER NOT NULL,
  scoring_mode VARCHAR(64) NOT NULL,
  default_timezone VARCHAR(64) NOT NULL
);

CREATE TABLE fraud_anomaly_detection_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE fraud_anomaly_detection_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE fraud_anomaly_detection_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);
