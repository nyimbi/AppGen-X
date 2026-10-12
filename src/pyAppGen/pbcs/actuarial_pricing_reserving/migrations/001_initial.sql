CREATE SCHEMA IF NOT EXISTS actuarial_pricing_reserving;

CREATE TABLE actuarial_pricing_reserving_rating_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rating_model_id VARCHAR(255) NOT NULL,
  model_name VARCHAR(255) NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  product_scope VARCHAR(255) NOT NULL,
  jurisdiction VARCHAR(255) NOT NULL,
  segment VARCHAR(255) NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  effective_to TIMESTAMP,
  data_vintage VARCHAR(255) NOT NULL,
  model_owner VARCHAR(255) NOT NULL,
  approval_state VARCHAR(255) NOT NULL,
  rollback_evidence TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
,
  UNIQUE (rating_model_id));

CREATE TABLE actuarial_pricing_reserving_actuarial_assumption (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  actuarial_assumption_id VARCHAR(255) NOT NULL,
  assumption_type VARCHAR(255) NOT NULL,
  source_study VARCHAR(255) NOT NULL,
  selected_value DECIMAL(18, 4) NOT NULL,
  value_low DECIMAL(18, 4),
  value_high DECIMAL(18, 4),
  rationale TEXT,
  sensitivity DECIMAL(18, 4),
  effective_from TIMESTAMP NOT NULL,
  effective_to TIMESTAMP,
  approval_state VARCHAR(255) NOT NULL,
  retirement_state VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE actuarial_pricing_reserving_experience_study (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  experience_study_id VARCHAR(255) NOT NULL,
  cohort_definition TEXT NOT NULL,
  exposure_measure VARCHAR(255) NOT NULL,
  experience_period VARCHAR(255) NOT NULL,
  claim_filter TEXT,
  exclusions TEXT,
  credibility_method VARCHAR(255) NOT NULL,
  data_vintage VARCHAR(255) NOT NULL,
  completeness_score DECIMAL(18, 4),
  outlier_rate DECIMAL(18, 4),
  reconciliation_variance DECIMAL(18, 4),
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE actuarial_pricing_reserving_loss_triangle (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  loss_triangle_id VARCHAR(255) NOT NULL,
  triangle_type VARCHAR(255) NOT NULL,
  valuation_date TIMESTAMP NOT NULL,
  origin_period VARCHAR(255) NOT NULL,
  development_age INTEGER NOT NULL,
  measure VARCHAR(255) NOT NULL,
  incremental_flag BOOLEAN NOT NULL,
  source VARCHAR(255) NOT NULL,
  reconciliation_status VARCHAR(255) NOT NULL,
  observed_factor DECIMAL(18, 4),
  selected_factor DECIMAL(18, 4),
  tail_factor DECIMAL(18, 4),
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
,
  UNIQUE (loss_triangle_id));

CREATE TABLE actuarial_pricing_reserving_reserve_estimate (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  reserve_estimate_id VARCHAR(255) NOT NULL,
  loss_triangle_id VARCHAR(255) NOT NULL,
  reserve_method VARCHAR(255) NOT NULL,
  valuation_date TIMESTAMP NOT NULL,
  method_weight DECIMAL(18, 4) NOT NULL,
  ultimate_loss DECIMAL(18, 4) NOT NULL,
  unpaid_loss DECIMAL(18, 4) NOT NULL,
  ibnr_amount DECIMAL(18, 4) NOT NULL,
  range_low DECIMAL(18, 4),
  range_high DECIMAL(18, 4),
  confidence_level DECIMAL(18, 4),
  discount_basis VARCHAR(255) NOT NULL,
  inflation_curve VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  selected_reserve DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (loss_triangle_id) REFERENCES actuarial_pricing_reserving_loss_triangle(loss_triangle_id)
);

CREATE TABLE actuarial_pricing_reserving_capital_scenario (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  capital_scenario_id VARCHAR(255) NOT NULL,
  scenario_type VARCHAR(255) NOT NULL,
  shock_set TEXT NOT NULL,
  probability DECIMAL(18, 4) NOT NULL,
  correlation DECIMAL(18, 4),
  time_horizon_days INTEGER NOT NULL,
  balance_sheet_basis VARCHAR(255) NOT NULL,
  affected_products TEXT,
  required_capital DECIMAL(18, 4) NOT NULL,
  available_capital DECIMAL(18, 4) NOT NULL,
  solvency_ratio DECIMAL(18, 4),
  breach_threshold DECIMAL(18, 4),
  management_action VARCHAR(255),
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE actuarial_pricing_reserving_model_validation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_validation_id VARCHAR(255) NOT NULL,
  rating_model_id VARCHAR(255) NOT NULL,
  validation_scope TEXT NOT NULL,
  challenger_model VARCHAR(255),
  backtest_period VARCHAR(255) NOT NULL,
  sensitivity_result DECIMAL(18, 4),
  limitation TEXT,
  reviewer_independence VARCHAR(255) NOT NULL,
  finding VARCHAR(255),
  remediation VARCHAR(255),
  validation_state VARCHAR(255) NOT NULL,
  expires_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (rating_model_id) REFERENCES actuarial_pricing_reserving_rating_model(rating_model_id)
);

CREATE TABLE actuarial_pricing_reserving_actuarial_pricing_reserving_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  policy_rule_id VARCHAR(255) NOT NULL,
  rule_name VARCHAR(255) NOT NULL,
  predicate_text TEXT NOT NULL,
  ambiguity_flag BOOLEAN NOT NULL,
  example_text TEXT,
  approver_role VARCHAR(255) NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  effective_to TIMESTAMP,
  compiled_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE actuarial_pricing_reserving_actuarial_pricing_reserving_runtime_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  runtime_parameter_id VARCHAR(255) NOT NULL,
  parameter_name VARCHAR(255) NOT NULL,
  parameter_value VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  bounded BOOLEAN NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE actuarial_pricing_reserving_actuarial_pricing_reserving_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  schema_extension_id VARCHAR(255) NOT NULL,
  target_table VARCHAR(255) NOT NULL,
  field_name VARCHAR(255) NOT NULL,
  field_type VARCHAR(255) NOT NULL,
  registered_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE actuarial_pricing_reserving_actuarial_pricing_reserving_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  control_assertion_id VARCHAR(255) NOT NULL,
  control_name VARCHAR(255) NOT NULL,
  population_size INTEGER NOT NULL,
  threshold DECIMAL(18, 4) NOT NULL,
  owner_id VARCHAR(255) NOT NULL,
  frequency VARCHAR(255) NOT NULL,
  failing_record_count INTEGER NOT NULL,
  assertion_result VARCHAR(255) NOT NULL,
  remediation_task VARCHAR(255),
  closure_evidence TEXT,
  evaluated_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE actuarial_pricing_reserving_actuarial_pricing_reserving_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  governed_model_id VARCHAR(255) NOT NULL,
  model_name VARCHAR(255) NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  method_type VARCHAR(255) NOT NULL,
  training_data_vintage VARCHAR(255) NOT NULL,
  feature_list TEXT,
  validation_evidence TEXT,
  limitation TEXT,
  monitoring_threshold DECIMAL(18, 4),
  owner_id VARCHAR(255) NOT NULL,
  governance_state VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255),
  approved_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE actuarial_pricing_reserving_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE actuarial_pricing_reserving_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE actuarial_pricing_reserving_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT,
  reason VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
