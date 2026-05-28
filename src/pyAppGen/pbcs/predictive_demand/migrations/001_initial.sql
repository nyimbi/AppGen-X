CREATE SCHEMA IF NOT EXISTS predictive_demand;

CREATE TABLE predictive_demand_forecast_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  sku VARCHAR(255) NOT NULL,
  location VARCHAR(255) NOT NULL,
  algorithm VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE predictive_demand_forecast_run (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  sku VARCHAR(255) NOT NULL,
  location VARCHAR(255) NOT NULL,
  signal_count INTEGER NOT NULL,
  forecast_quantity VARCHAR(255) NOT NULL,
  shortage_quantity VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE predictive_demand_demand_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  signal_id VARCHAR(255) NOT NULL,
  signal_type VARCHAR(255) NOT NULL,
  sku VARCHAR(255) NOT NULL,
  location VARCHAR(255) NOT NULL,
  region VARCHAR(255) NOT NULL,
  quantity VARCHAR(255) NOT NULL,
  source VARCHAR(255) NOT NULL,
  driver_weight VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE predictive_demand_forecast_result (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  result_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  sku VARCHAR(255) NOT NULL,
  location VARCHAR(255) NOT NULL,
  forecast_quantity VARCHAR(255) NOT NULL,
  recommended_supply VARCHAR(255) NOT NULL,
  shortage_quantity VARCHAR(255) NOT NULL,
  confidence_band DECIMAL(18, 4) NOT NULL,
  planning_action VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE predictive_demand_planning_horizon (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  horizon_id VARCHAR(255) NOT NULL,
  sku VARCHAR(255) NOT NULL,
  location VARCHAR(255) NOT NULL,
  granularity VARCHAR(255) NOT NULL,
  starts_on VARCHAR(255) NOT NULL,
  ends_on VARCHAR(255) NOT NULL,
  freeze_window_days VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE predictive_demand_forecast_driver (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  driver_id VARCHAR(255) NOT NULL,
  sku VARCHAR(255) NOT NULL,
  location VARCHAR(255) NOT NULL,
  driver_type VARCHAR(255) NOT NULL,
  driver_value VARCHAR(255) NOT NULL,
  weight VARCHAR(255) NOT NULL,
  source VARCHAR(255) NOT NULL,
  effective_on VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE predictive_demand_consensus_adjustment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  adjustment_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  planner_id VARCHAR(255) NOT NULL,
  adjustment_quantity VARCHAR(255) NOT NULL,
  reason_code VARCHAR(255) NOT NULL,
  approval_status VARCHAR(255) NOT NULL,
  policy_result VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE predictive_demand_scenario_version (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  scenario_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  scenario_name VARCHAR(255) NOT NULL,
  assumption_set VARCHAR(255) NOT NULL,
  forecast_quantity VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  selected VARCHAR(255) NOT NULL,
  created_by VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE predictive_demand_shortage_risk (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  risk_id VARCHAR(255) NOT NULL,
  result_id VARCHAR(255) NOT NULL,
  sku VARCHAR(255) NOT NULL,
  location VARCHAR(255) NOT NULL,
  shortage_quantity VARCHAR(255) NOT NULL,
  risk_band VARCHAR(255) NOT NULL,
  material_constraint VARCHAR(255) NOT NULL,
  alert_due_on VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE predictive_demand_replenishment_recommendation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  recommendation_id VARCHAR(255) NOT NULL,
  result_id VARCHAR(255) NOT NULL,
  sku VARCHAR(255) NOT NULL,
  location VARCHAR(255) NOT NULL,
  recommended_quantity VARCHAR(255) NOT NULL,
  recommended_date TIMESTAMP NOT NULL,
  service_level_target VARCHAR(255) NOT NULL,
  action_status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE predictive_demand_forecast_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  exception_id VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) NOT NULL,
  exception_type VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  detected_value VARCHAR(255) NOT NULL,
  threshold DECIMAL(18, 4) NOT NULL,
  resolution_status VARCHAR(255) NOT NULL,
  assigned_to VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE predictive_demand_model_drift_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  drift_id VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  metric_name VARCHAR(255) NOT NULL,
  metric_value VARCHAR(255) NOT NULL,
  threshold DECIMAL(18, 4) NOT NULL,
  drift_band VARCHAR(255) NOT NULL,
  retrain_recommended VARCHAR(255) NOT NULL,
  observed_at TIMESTAMP NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE predictive_demand_planning_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  allowed_signal_types VARCHAR(255) NOT NULL,
  allowed_regions VARCHAR(255) NOT NULL,
  forecast_policy VARCHAR(255) NOT NULL,
  shortage_policy VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE predictive_demand_planning_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  value VARCHAR(255) NOT NULL,
  bounds VARCHAR(255) NOT NULL,
  changed_by VARCHAR(255) NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  effective_to VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE predictive_demand_governed_model_evidence (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  evidence_id TEXT NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  algorithm VARCHAR(255) NOT NULL,
  training_window VARCHAR(255) NOT NULL,
  validation_metrics VARCHAR(255) NOT NULL,
  approval_status VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255) NOT NULL,
  approved_at TIMESTAMP NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE predictive_demand_forecast_audit_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  proof_id VARCHAR(255) NOT NULL,
  entity_type VARCHAR(255) NOT NULL,
  entity_id VARCHAR(255) NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  previous_hash VARCHAR(255) NOT NULL,
  signature VARCHAR(255) NOT NULL,
  control_assertions VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
