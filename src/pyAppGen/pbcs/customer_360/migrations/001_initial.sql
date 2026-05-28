CREATE SCHEMA IF NOT EXISTS customer_360;

CREATE TABLE customer_360_customer_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  display_name VARCHAR(255) NOT NULL,
  region VARCHAR(255) NOT NULL,
  lifecycle_state VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_profile_version (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_profile_attribute (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_identity (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  identity_type VARCHAR(255) NOT NULL,
  identity_value_hash VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL
);

CREATE TABLE customer_360_customer_identity_evidence (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_identity_match_candidate (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_identity_survivorship_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_relationship (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_household (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_household_member (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_engagement_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  channel VARCHAR(255) NOT NULL,
  value VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_engagement_score (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_communication_preference (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_preference_history (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_touchpoint (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_channel_interaction (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_consent_record (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  purpose VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL
);

CREATE TABLE customer_360_consent_policy (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_privacy_request (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_timeline (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_timeline_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_segment_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_segment_membership (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_value_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_health_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_churn_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_profile_merge_case (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_profile_merge_decision (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_exception_case (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_remediation_task (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_commerce_customer_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_billing_account_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_service_timeline_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_loyalty_profile_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_notification_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_api_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_federation_view (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_resilience_drill (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_crypto_epoch (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_carbon_customer_window (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_segment_optimization (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_channel_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_anomaly_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_exposure_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_identity_attestation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_customer_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL
);

CREATE TABLE customer_360_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL
);

CREATE TABLE customer_360_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  reason VARCHAR(255) NOT NULL
);
