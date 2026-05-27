CREATE SCHEMA IF NOT EXISTS cdp_segmentation;

CREATE TABLE cdp_segmentation_customer_event (
  id VARCHAR(64) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  region VARCHAR(64) NOT NULL,
  properties TEXT NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE cdp_segmentation_event_identity_link (
  id VARCHAR(64) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255),
  segment_id VARCHAR(255),
  status VARCHAR(64) NOT NULL,
  attributes TEXT NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE cdp_segmentation_identity_stitch (
  id VARCHAR(64) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255),
  segment_id VARCHAR(255),
  status VARCHAR(64) NOT NULL,
  attributes TEXT NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE cdp_segmentation_profile (
  id VARCHAR(64) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  identity_hash VARCHAR(255) NOT NULL,
  region VARCHAR(64) NOT NULL,
  status VARCHAR(64) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE cdp_segmentation_profile_property (
  id VARCHAR(64) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  property_id VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  value TEXT NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE cdp_segmentation_segment_definition (
  id VARCHAR(64) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  segment_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  criteria TEXT NOT NULL,
  status VARCHAR(64) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE cdp_segmentation_segment_membership (
  id VARCHAR(64) PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  membership_id VARCHAR(255) NOT NULL,
  segment_id VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  score DECIMAL(12, 6) NOT NULL,
  status VARCHAR(64) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE cdp_segmentation_profile_consent (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_profile_enrichment (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_segment_rule (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_segment_version (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_membership_evaluation (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_activation_destination (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_activation_run (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_activation_delivery (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_audience_snapshot (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_audience_forecast (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_affinity_score (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_lifecycle_risk_score (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_merge_candidate (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_profile_exception (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_data_quality_finding (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_consent_policy_screening (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_customer_projection (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_payment_projection (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_order_projection (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_notification_projection (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_loyalty_projection (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_pricing_projection (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_profile_proof (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_profile_audit_entry (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_cdp_control_assertion (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_cdp_federation_view (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_cdp_resilience_drill (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_cdp_crypto_epoch (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_carbon_activation_window (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_segment_simulation (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_activation_allocation (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_profile_anomaly_signal (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_audience_exposure_forecast (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_identity_attestation (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_cdp_governed_model (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_cdp_seed_data (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_rule (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_parameter (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_configuration (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, record_id VARCHAR(255) NOT NULL, customer_id VARCHAR(255), segment_id VARCHAR(255), status VARCHAR(64) NOT NULL, attributes TEXT NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);

CREATE TABLE cdp_segmentation_appgen_outbox_event (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, event_id VARCHAR(255) NOT NULL, event_type VARCHAR(255) NOT NULL, idempotency_key VARCHAR(255) NOT NULL, payload TEXT NOT NULL, attempts INTEGER NOT NULL, reason TEXT, status VARCHAR(64) NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_appgen_inbox_event (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, event_id VARCHAR(255) NOT NULL, event_type VARCHAR(255) NOT NULL, idempotency_key VARCHAR(255) NOT NULL, payload TEXT NOT NULL, attempts INTEGER NOT NULL, reason TEXT, status VARCHAR(64) NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
CREATE TABLE cdp_segmentation_dead_letter_event (id VARCHAR(64) PRIMARY KEY NOT NULL, tenant VARCHAR(255) NOT NULL, event_id VARCHAR(255) NOT NULL, event_type VARCHAR(255) NOT NULL, idempotency_key VARCHAR(255) NOT NULL, payload TEXT NOT NULL, attempts INTEGER NOT NULL, reason TEXT, status VARCHAR(64) NOT NULL, audit_hash VARCHAR(255) NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL);
