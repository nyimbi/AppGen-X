CREATE SCHEMA IF NOT EXISTS dam_core;

CREATE TABLE dam_core_asset (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  filename VARCHAR(255) NOT NULL,
  mime_type VARCHAR(255) NOT NULL,
  fingerprint VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_version (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_binary (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_fingerprint (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_collection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_collection_member (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_rendition (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  rendition_id VARCHAR(255) NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  profile VARCHAR(255) NOT NULL,
  quality_score DECIMAL(18, 4) NOT NULL
);

CREATE TABLE dam_core_transcoding_job (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_transcode_route (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_rendition_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_metadata_tag (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  tag_id VARCHAR(255) NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  taxonomy VARCHAR(255) NOT NULL,
  value VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_metadata_taxonomy (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_metadata_enrichment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_semantic_annotation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_rights_policy (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  policy_id VARCHAR(255) NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  allowed_markets VARCHAR(255) NOT NULL,
  blocked_markets VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_rights_decision (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_license_agreement (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_usage_entitlement (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_product_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_campaign_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_channel_asset_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_workflow_case (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_review_task (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_quality_score (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_usage_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_usage_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_duplicate_candidate (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_lineage (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_audit_entry (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_federation_view (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_resilience_drill (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_crypto_epoch (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_carbon_transcode_window (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_rendition_cost_simulation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_route_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_anomaly_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_exposure_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_identity_attestation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_asset_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_dam_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_dam_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_dam_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  attributes VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL
);

CREATE TABLE dam_core_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL
);

CREATE TABLE dam_core_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  reason VARCHAR(255) NOT NULL
);
