CREATE SCHEMA IF NOT EXISTS lead_opportunity;

CREATE TABLE lead_opportunity_lead (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  lead_id VARCHAR(255) NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  company VARCHAR(255) NOT NULL,
  source VARCHAR(255) NOT NULL,
  region VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  engagement_score DECIMAL(18, 4) NOT NULL,
  estimated_value VARCHAR(255) NOT NULL,
  score DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  assigned_owner VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE lead_opportunity_lead_enrichment_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  snapshot_id VARCHAR(255) NOT NULL,
  lead_id VARCHAR(255) NOT NULL,
  segment_fit_score DECIMAL(18, 4) NOT NULL,
  firmographic_fit VARCHAR(255) NOT NULL,
  intent_summary VARCHAR(255) NOT NULL,
  enriched_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE lead_opportunity_lead_dedup_case (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  case_id VARCHAR(255) NOT NULL,
  lead_id VARCHAR(255) NOT NULL,
  duplicate_lead_id VARCHAR(255) NOT NULL,
  match_hash VARCHAR(255) NOT NULL,
  resolution_status VARCHAR(255) NOT NULL,
  resolved_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE lead_opportunity_lead_score_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  snapshot_id VARCHAR(255) NOT NULL,
  lead_id VARCHAR(255) NOT NULL,
  qualification_score DECIMAL(18, 4) NOT NULL,
  lead_source_weight VARCHAR(255) NOT NULL,
  segment_fit_weight VARCHAR(255) NOT NULL,
  engagement_weight VARCHAR(255) NOT NULL,
  recorded_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE lead_opportunity_lead_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assignment_id VARCHAR(255) NOT NULL,
  lead_id VARCHAR(255) NOT NULL,
  owner VARCHAR(255) NOT NULL,
  assignment_mode VARCHAR(255) NOT NULL,
  territory_key VARCHAR(255) NOT NULL,
  assigned_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE lead_opportunity_qualification_decision (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  decision_id VARCHAR(255) NOT NULL,
  lead_id VARCHAR(255) NOT NULL,
  minimum_score DECIMAL(18, 4) NOT NULL,
  actual_score DECIMAL(18, 4) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  qualified_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE lead_opportunity_opportunity (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  opportunity_id VARCHAR(255) NOT NULL,
  lead_id VARCHAR(255) NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  stage VARCHAR(255) NOT NULL,
  close_date TIMESTAMP NOT NULL,
  win_probability VARCHAR(255) NOT NULL,
  forecast_amount DECIMAL(18, 4) NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE lead_opportunity_opportunity_stage_history (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  history_id VARCHAR(255) NOT NULL,
  opportunity_id VARCHAR(255) NOT NULL,
  from_stage VARCHAR(255) NOT NULL,
  to_stage VARCHAR(255) NOT NULL,
  changed_at TIMESTAMP NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE lead_opportunity_pipeline_forecast_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  snapshot_id VARCHAR(255) NOT NULL,
  opportunity_id VARCHAR(255) NOT NULL,
  forecast_amount DECIMAL(18, 4) NOT NULL,
  confidence_floor DECIMAL(18, 4) NOT NULL,
  slippage_risk VARCHAR(255) NOT NULL,
  captured_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE lead_opportunity_quote_proposal_handoff (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  handoff_id VARCHAR(255) NOT NULL,
  opportunity_id VARCHAR(255) NOT NULL,
  proposal_reference VARCHAR(255) NOT NULL,
  handoff_status VARCHAR(255) NOT NULL,
  handoff_owner VARCHAR(255) NOT NULL,
  handed_off_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE lead_opportunity_opportunity_outcome (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  outcome_id VARCHAR(255) NOT NULL,
  opportunity_id VARCHAR(255) NOT NULL,
  outcome VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  competitor_context VARCHAR(255) NOT NULL,
  recorded_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE lead_opportunity_account_hierarchy (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  parent_account_id VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  region VARCHAR(255) NOT NULL,
  owner VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE lead_opportunity_sales_activity (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  activity_id VARCHAR(255) NOT NULL,
  opportunity_id VARCHAR(255) NOT NULL,
  activity_type VARCHAR(255) NOT NULL,
  subject VARCHAR(255) NOT NULL,
  sentiment VARCHAR(255) NOT NULL,
  occurred_at TIMESTAMP NOT NULL,
  owner VARCHAR(255) NOT NULL,
  next_best_action VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE lead_opportunity_sales_coaching_insight (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  insight_id VARCHAR(255) NOT NULL,
  opportunity_id VARCHAR(255) NOT NULL,
  activity_id VARCHAR(255) NOT NULL,
  coaching_signal VARCHAR(255) NOT NULL,
  recommended_action VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  recorded_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE lead_opportunity_audit_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  audit_id VARCHAR(255) NOT NULL,
  entity_type VARCHAR(255) NOT NULL,
  entity_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  event_hash VARCHAR(255) NOT NULL,
  recorded_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE lead_opportunity_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  compiled_evidence TEXT NOT NULL,
  recorded_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE lead_opportunity_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_id VARCHAR(255) NOT NULL,
  parameter_name VARCHAR(255) NOT NULL,
  parameter_value VARCHAR(255) NOT NULL,
  bounds VARCHAR(255) NOT NULL,
  recorded_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE lead_opportunity_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  configuration_id VARCHAR(255) NOT NULL,
  database_backend VARCHAR(255) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  retry_limit VARCHAR(255) NOT NULL,
  default_currency VARCHAR(255) NOT NULL,
  default_timezone VARCHAR(255) NOT NULL,
  recorded_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE lead_opportunity_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  model_name VARCHAR(255) NOT NULL,
  model_scope VARCHAR(255) NOT NULL,
  feature_lineage VARCHAR(255) NOT NULL,
  governance_status VARCHAR(255) NOT NULL,
  recorded_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE lead_opportunity_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  seed_id VARCHAR(255) NOT NULL,
  seed_type VARCHAR(255) NOT NULL,
  seed_values VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  recorded_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
