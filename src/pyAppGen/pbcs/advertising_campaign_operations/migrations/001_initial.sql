CREATE SCHEMA IF NOT EXISTS advertising_campaign_operations;

CREATE TABLE advertising_campaign_operations_ad_campaign (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  ad_campaign_id VARCHAR(255) NOT NULL,
  campaign_name VARCHAR(255) NOT NULL,
  objective VARCHAR(255) NOT NULL,
  offer VARCHAR(255) NOT NULL,
  audience_promise TEXT NOT NULL,
  primary_kpi VARCHAR(255) NOT NULL,
  channel_mix VARCHAR(255) NOT NULL,
  flight_start TIMESTAMP NOT NULL,
  flight_end TIMESTAMP NOT NULL,
  budget_amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  pacing_state VARCHAR(255) NOT NULL,
  launch_gate_state VARCHAR(255) NOT NULL,
  brief_fingerprint VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE advertising_campaign_operations_audience_segment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  audience_segment_id VARCHAR(255) NOT NULL,
  ad_campaign_id VARCHAR(255) NOT NULL,
  segment_name VARCHAR(255) NOT NULL,
  inclusion_criteria TEXT NOT NULL,
  suppression_list TEXT NOT NULL,
  recency_window_days INTEGER NOT NULL,
  exclusion_precedence INTEGER NOT NULL,
  estimated_reach INTEGER NOT NULL,
  overlap_percent DECIMAL(18, 4) NOT NULL,
  consent_status VARCHAR(255) NOT NULL,
  sensitive_category VARCHAR(255) NOT NULL,
  freshness_at TIMESTAMP NOT NULL,
  risk_level VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ad_campaign_id) REFERENCES advertising_campaign_operations_ad_campaign(ad_campaign_id)
);

CREATE TABLE advertising_campaign_operations_media_placement (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  media_placement_id VARCHAR(255) NOT NULL,
  ad_campaign_id VARCHAR(255) NOT NULL,
  publisher_name VARCHAR(255) NOT NULL,
  placement_environment VARCHAR(255) NOT NULL,
  ad_size VARCHAR(255) NOT NULL,
  package_rate DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  hold_expires_at TIMESTAMP,
  geo_targets VARCHAR(255) NOT NULL,
  daypart_window VARCHAR(255) NOT NULL,
  device_preference VARCHAR(255) NOT NULL,
  frequency_cap INTEGER NOT NULL,
  trafficking_state VARCHAR(255) NOT NULL,
  tracking_ready BOOLEAN NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ad_campaign_id) REFERENCES advertising_campaign_operations_ad_campaign(ad_campaign_id)
);

CREATE TABLE advertising_campaign_operations_creative_asset (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  creative_asset_id VARCHAR(255) NOT NULL,
  ad_campaign_id VARCHAR(255) NOT NULL,
  asset_name VARCHAR(255) NOT NULL,
  asset_format VARCHAR(255) NOT NULL,
  message_angle VARCHAR(255) NOT NULL,
  required_disclosures TEXT NOT NULL,
  revision_number INTEGER NOT NULL,
  approval_stage VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255) NOT NULL,
  approved_at TIMESTAMP,
  asset_hash VARCHAR(255) NOT NULL,
  superseded BOOLEAN NOT NULL,
  delivery_destination VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ad_campaign_id) REFERENCES advertising_campaign_operations_ad_campaign(ad_campaign_id)
);

CREATE TABLE advertising_campaign_operations_campaign_budget (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  campaign_budget_id VARCHAR(255) NOT NULL,
  ad_campaign_id VARCHAR(255) NOT NULL,
  working_budget DECIMAL(18, 4) NOT NULL,
  approved_budget DECIMAL(18, 4) NOT NULL,
  committed_budget DECIMAL(18, 4) NOT NULL,
  held_reserve DECIMAL(18, 4) NOT NULL,
  contingency_reserve DECIMAL(18, 4) NOT NULL,
  released_reserve DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  budget_version VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255) NOT NULL,
  approved_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ad_campaign_id) REFERENCES advertising_campaign_operations_ad_campaign(ad_campaign_id)
);

CREATE TABLE advertising_campaign_operations_performance_result (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  performance_result_id VARCHAR(255) NOT NULL,
  ad_campaign_id VARCHAR(255) NOT NULL,
  media_placement_id VARCHAR(255) NOT NULL,
  metric_grain VARCHAR(255) NOT NULL,
  metric_name VARCHAR(255) NOT NULL,
  metric_value DECIMAL(18, 4) NOT NULL,
  impressions INTEGER NOT NULL,
  clicks INTEGER NOT NULL,
  conversions INTEGER NOT NULL,
  spend DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  attribution_model VARCHAR(255) NOT NULL,
  attribution_window_days INTEGER NOT NULL,
  reporting_delay_hours INTEGER NOT NULL,
  source_name VARCHAR(255) NOT NULL,
  confidence_score DECIMAL(18, 4) NOT NULL,
  deduplicated BOOLEAN NOT NULL,
  reported_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ad_campaign_id) REFERENCES advertising_campaign_operations_ad_campaign(ad_campaign_id)
);

CREATE TABLE advertising_campaign_operations_billing_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  billing_event_id VARCHAR(255) NOT NULL,
  ad_campaign_id VARCHAR(255) NOT NULL,
  media_placement_id VARCHAR(255) NOT NULL,
  invoice_reference VARCHAR(255) NOT NULL,
  billed_amount DECIMAL(18, 4) NOT NULL,
  delivered_value DECIMAL(18, 4) NOT NULL,
  variance_amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  reconciliation_state VARCHAR(255) NOT NULL,
  period_start TIMESTAMP NOT NULL,
  period_end TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ad_campaign_id) REFERENCES advertising_campaign_operations_ad_campaign(ad_campaign_id)
);

CREATE TABLE advertising_campaign_operations_advertising_campaign_operations_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  policy_rule_id VARCHAR(255) NOT NULL,
  ad_campaign_id VARCHAR(255) NOT NULL,
  rule_name VARCHAR(255) NOT NULL,
  predicate_text TEXT NOT NULL,
  policy_version VARCHAR(255) NOT NULL,
  approver_role VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  effective_to TIMESTAMP,
  compiled_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE advertising_campaign_operations_advertising_campaign_operations_runtime_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  runtime_parameter_id VARCHAR(255) NOT NULL,
  parameter_name VARCHAR(255) NOT NULL,
  parameter_value DECIMAL(18, 4) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  bounded BOOLEAN NOT NULL,
  quality_score_floor DECIMAL(18, 4) NOT NULL,
  materiality_threshold DECIMAL(18, 4) NOT NULL,
  approval_sla_hours INTEGER NOT NULL,
  risk_threshold DECIMAL(18, 4) NOT NULL,
  forecast_horizon_days INTEGER NOT NULL,
  workbench_limit INTEGER NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE advertising_campaign_operations_advertising_campaign_operations_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  schema_extension_id VARCHAR(255) NOT NULL,
  target_table VARCHAR(255) NOT NULL,
  field_name VARCHAR(255) NOT NULL,
  field_type VARCHAR(255) NOT NULL,
  channel_name VARCHAR(255) NOT NULL,
  owner_role VARCHAR(255) NOT NULL,
  rollout_state VARCHAR(255) NOT NULL,
  projection_impact TEXT NOT NULL,
  registered_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE advertising_campaign_operations_advertising_campaign_operations_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  control_assertion_id VARCHAR(255) NOT NULL,
  ad_campaign_id VARCHAR(255) NOT NULL,
  control_name VARCHAR(255) NOT NULL,
  assertion_result VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  remediation_task VARCHAR(255) NOT NULL,
  evaluated_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE advertising_campaign_operations_advertising_campaign_operations_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  governed_model_id VARCHAR(255) NOT NULL,
  model_name VARCHAR(255) NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  governance_state VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255) NOT NULL,
  approved_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE advertising_campaign_operations_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE advertising_campaign_operations_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE advertising_campaign_operations_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  reason VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
